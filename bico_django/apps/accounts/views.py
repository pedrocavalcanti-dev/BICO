from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
)
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods

from .forms import (
    AccountCreationForm,
    AccountProfileForm,
    BicoAuthenticationForm,
    BicoPasswordChangeForm,
    BicoPasswordResetForm,
    BicoSetPasswordForm,
)
from .models import User
from .services import (
    ThrottleDecision,
    audit_auth_event,
    authentication_throttle,
    clear_authentication_throttle,
)


def _safe_next_url(request, value: str | None) -> str | None:
    if not value or not url_has_allowed_host_and_scheme(
        value,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return None
    return value


def _form_with_throttle(form, decision: ThrottleDecision):
    form.add_error(None, "Muitas tentativas. Aguarde alguns minutos e tente novamente.")
    return decision


@require_http_methods(["GET", "POST"])
def login_view(request):
    next_url = _safe_next_url(request, request.POST.get("next") or request.GET.get("next"))
    if request.user.is_authenticated:
        return redirect(next_url or "accounts:account")

    form = BicoAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        identity = request.POST.get("username", "")[:254]
        try:
            identity = User.objects.normalize_email(identity)
        except (AttributeError, TypeError):
            identity = "unknown"
        decision = authentication_throttle(
            request,
            scope="login",
            identity=identity,
            limit=12,
            window_seconds=15 * 60,
        )
        if not decision.allowed:
            _form_with_throttle(form, decision)
            response = render(
                request,
                "accounts/login.html",
                {"form": form, "next_url": next_url},
                status=429,
            )
            response["Retry-After"] = str(decision.retry_after)
            return response

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            clear_authentication_throttle(request, scope="login", identity=identity)
            remember = request.POST.get("remember_me") == "on"
            request.session.set_expiry(60 * 60 * 24 * 30 if remember else 0)
            audit_auth_event(action="auth.login.succeeded", request=request, actor=user)
            return redirect(next_url or "accounts:account")

        audit_auth_event(
            action="auth.login.denied",
            request=request,
            outcome="FAILURE",
        )
        return render(
            request,
            "accounts/login.html",
            {"form": form, "next_url": next_url},
            status=400,
        )

    return render(request, "accounts/login.html", {"form": form, "next_url": next_url})


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:account")

    form = AccountCreationForm(request.POST or None)
    if request.method == "POST":
        identity = request.POST.get("email", "")[:254]
        identity = User.objects.normalize_email(identity) if identity else ""
        decision = authentication_throttle(
            request,
            scope="register",
            identity=identity,
            limit=5,
            window_seconds=60 * 60,
        )
        if not decision.allowed:
            _form_with_throttle(form, decision)
            response = render(request, "accounts/register.html", {"form": form}, status=429)
            response["Retry-After"] = str(decision.retry_after)
            return response

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
            except IntegrityError:
                form.add_error(
                    "email",
                    "Este e-mail já possui uma conta. Entre ou recupere sua senha.",
                )
                return render(request, "accounts/register.html", {"form": form}, status=400)
            auth_login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            request.session.set_expiry(0)
            audit_auth_event(action="account.registered", request=request, actor=user)
            messages.success(request, "Sua conta BICO foi criada. Boas-vindas!")
            return redirect("accounts:account")
        return render(request, "accounts/register.html", {"form": form}, status=400)

    return render(request, "accounts/register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def password_reset_request(request):
    if request.user.is_authenticated:
        return redirect("accounts:account")

    form = BicoPasswordResetForm(request.POST or None)
    if request.method == "POST":
        email = request.POST.get("email", "")[:254]
        email = User.objects.normalize_email(email) if email else ""
        decision = authentication_throttle(
            request,
            scope="password-reset",
            identity=email,
            limit=5,
            window_seconds=60 * 60,
        )
        if not decision.allowed:
            _form_with_throttle(form, decision)
            response = render(request, "accounts/password_reset.html", {"form": form}, status=429)
            response["Retry-After"] = str(decision.retry_after)
            return response

        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                email_template_name="accounts/password_reset_email.html",
                subject_template_name="accounts/password_reset_subject.txt",
            )
            audit_auth_event(action="auth.password_reset.requested", request=request)
            return redirect("accounts:password_reset_done")
        return render(request, "accounts/password_reset.html", {"form": form}, status=400)

    return render(request, "accounts/password_reset.html", {"form": form})


class BicoPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = BicoSetPasswordForm
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")
    post_reset_login = False

    def form_valid(self, form):
        response = super().form_valid(form)
        audit_auth_event(
            action="auth.password_reset.completed",
            request=self.request,
            actor=self.user,
        )
        return response


class BicoPasswordChangeView(PasswordChangeView):
    form_class = BicoPasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")

    def form_valid(self, form):
        response = super().form_valid(form)
        audit_auth_event(
            action="auth.password.changed",
            request=self.request,
            actor=self.request.user,
        )
        messages.success(self.request, "Sua senha foi alterada.")
        return response


@login_required
def account_view(request):
    from apps.providers.models import ProviderApplication, ProviderProfile

    try:
        provider_application = request.user.provider_application
    except ProviderApplication.DoesNotExist:
        provider_application = None
    provider_profile = ProviderProfile.objects.filter(
        user=request.user, status=ProviderProfile.Status.APPROVED
    ).first()
    return render(
        request,
        "accounts/account.html",
        {
            "account_user": request.user,
            "provider_application": provider_application,
            "provider_profile": provider_profile,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def account_edit(request):
    form = AccountProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        audit_auth_event(action="account.profile.updated", request=request, actor=user)
        messages.success(request, "Seu perfil foi atualizado.")
        return redirect("accounts:account")
    return render(
        request,
        "accounts/account_edit.html",
        {"form": form},
        status=400 if request.method == "POST" else 200,
    )


@require_http_methods(["POST"])
def logout_view(request):
    actor = request.user if request.user.is_authenticated else None
    if actor:
        audit_auth_event(action="auth.logout", request=request, actor=actor)
    auth_logout(request)
    messages.success(request, "Você saiu da sua conta.")
    return redirect("core:home")


@login_required
def conversations_placeholder(request):
    return render(
        request,
        "accounts/feature_unavailable.html",
        {"title": "Conversas", "message": "O chat ainda não está disponível na BICO."},
    )


@login_required
def notifications_placeholder(request):
    return render(
        request,
        "accounts/feature_unavailable.html",
        {
            "title": "Notificações",
            "message": "As notificações serão disponibilizadas em uma próxima etapa.",
        },
    )
