import hashlib
import hmac
from dataclasses import dataclass
from datetime import timedelta

from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.audit.models import AuditEvent

from .models import AuthThrottleBucket


@dataclass(frozen=True)
class ThrottleDecision:
    allowed: bool
    retry_after: int


def _bucket_key(scope: str, identity: str) -> str:
    value = f"{scope}:{identity.strip().casefold()}".encode()
    return hmac.new(settings.SECRET_KEY.encode(), value, hashlib.sha256).hexdigest()


def consume_attempt(
    *, scope: str, identity: str, limit: int, window_seconds: int
) -> ThrottleDecision:
    """Atomically consume a shared MySQL counter without persisting identity data."""
    now = timezone.now()
    window = timedelta(seconds=window_seconds)
    key = _bucket_key(scope, identity or "unknown")

    with transaction.atomic():
        try:
            bucket = AuthThrottleBucket.objects.select_for_update().get(pk=key)
        except AuthThrottleBucket.DoesNotExist:
            try:
                with transaction.atomic():
                    AuthThrottleBucket.objects.create(key=key, window_started_at=now, attempts=1)
                return ThrottleDecision(True, 0)
            except IntegrityError:
                bucket = AuthThrottleBucket.objects.select_for_update().get(pk=key)

        if now - bucket.window_started_at >= window:
            bucket.window_started_at = now
            bucket.attempts = 0

        if bucket.attempts >= limit:
            retry_after = max(1, int((bucket.window_started_at + window - now).total_seconds()))
            return ThrottleDecision(False, retry_after)

        bucket.attempts += 1
        bucket.save(update_fields=("window_started_at", "attempts"))
        return ThrottleDecision(True, 0)


def request_ip(request) -> str:
    """Use the socket peer only; forwarded headers are not trusted by default."""
    return request.META.get("REMOTE_ADDR", "unknown")[:64] or "unknown"


def audit_auth_event(
    *, action: str, request, actor=None, outcome=AuditEvent.Outcome.SUCCESS
) -> None:
    AuditEvent.objects.create(
        actor=actor,
        action=action,
        outcome=outcome,
        metadata={"channel": "web"},
    )


def authentication_throttle(
    request, *, scope: str, identity: str = "", limit: int, window_seconds: int
):
    ip_decision = consume_attempt(
        scope=f"{scope}:ip",
        identity=request_ip(request),
        limit=limit,
        window_seconds=window_seconds,
    )
    identity_decision = (
        consume_attempt(
            scope=f"{scope}:identity",
            identity=identity,
            limit=limit,
            window_seconds=window_seconds,
        )
        if identity
        else ThrottleDecision(True, 0)
    )
    return ThrottleDecision(
        allowed=ip_decision.allowed and identity_decision.allowed,
        retry_after=max(ip_decision.retry_after, identity_decision.retry_after),
    )


def clear_authentication_throttle(request, *, scope: str, identity: str = "") -> None:
    """Clear successful login counters without retaining the underlying identity."""
    keys = [_bucket_key(f"{scope}:ip", request_ip(request))]
    if identity:
        keys.append(_bucket_key(f"{scope}:identity", identity))
    AuthThrottleBucket.objects.filter(key__in=keys).delete()
