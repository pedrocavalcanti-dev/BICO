from io import BytesIO

from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone
from PIL import Image, ImageOps

from apps.accounts.services import authentication_throttle
from apps.audit.models import AuditEvent

from .document_validation import validate_document_file
from .models import ProviderApplication, ProviderDocument


def _provider_throttle(request, *, scope, limit):
    return authentication_throttle(
        request,
        scope=scope,
        identity=str(request.user.pk),
        limit=limit,
        window_seconds=60 * 60,
    )


def throttle_document_upload(request):
    return _provider_throttle(request, scope="provider-document-upload", limit=10)


def throttle_application_submission(request):
    return _provider_throttle(request, scope="provider-application-submit", limit=5)


def get_or_create_application(user):
    if not settings.PROVIDER_ONBOARDING_ENABLED:
        raise PermissionDenied("O cadastro profissional está temporariamente indisponível.")
    application, _created = ProviderApplication.objects.get_or_create(user=user)
    return application


def _sanitized_image(upload, side):
    validate_document_file(upload)
    image_format = upload.detected_format
    extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[image_format]
    upload.seek(0)
    with Image.open(upload) as source:
        image = ImageOps.exif_transpose(source)
        output = BytesIO()
        if image_format == "JPEG":
            image.convert("RGB").save(output, format="JPEG", quality=90, optimize=True)
        elif image_format == "PNG":
            image.save(output, format="PNG", optimize=True)
        else:
            image.convert("RGB").save(output, format="WEBP", quality=90, method=4)
    content = output.getvalue()
    if len(content) > 8 * 1024 * 1024:
        raise ValidationError("A imagem processada excede o limite de 8 MB.")
    return ContentFile(content, name=f"{side.lower()}.{extension}"), image_format


def replace_identity_document(*, application, side, upload):
    if not settings.PROVIDER_DOCUMENT_UPLOAD_ENABLED:
        raise PermissionDenied("O envio de documentos está temporariamente indisponível.")
    if not application.can_edit:
        raise ValidationError("Esta solicitação não aceita alterações no momento.")
    if side not in ProviderDocument.Side.values:
        raise ValidationError("Escolha frente ou verso do documento.")

    sanitized, image_format = _sanitized_image(upload, side)
    existing = application.identity_documents.filter(side=side).first()
    old_name = existing.file.name if existing and existing.file else ""
    document = existing or ProviderDocument(application=application, side=side)
    document.detected_format = image_format
    document.prevalidation_passed = True
    document.prevalidation_feedback = (
        "Imagem legível para análise humana; autenticidade não verificada."
    )
    document.file.save(sanitized.name, sanitized, save=False)
    new_name = document.file.name
    try:
        document.save()
    except Exception:
        document.file.storage.delete(new_name)
        raise
    if old_name and old_name != new_name:
        document.file.storage.delete(old_name)
    AuditEvent.objects.create(
        actor=application.user,
        action="provider.document.uploaded",
        outcome=AuditEvent.Outcome.SUCCESS,
        metadata={"side": side},
    )
    return document


def _application_ready(application):
    if not application.provider_type:
        return False
    if application.provider_type == ProviderApplication.ProviderType.INDIVIDUAL:
        if not all(
            (
                application.legal_name,
                application.cpf,
                application.birth_date,
                application.phone,
                application.document_type,
            )
        ):
            return False
    elif not all(
        (
            application.company_legal_name,
            application.cnpj,
            application.company_email,
            application.company_phone,
            application.representative_name,
            application.representative_cpf,
            application.representative_phone,
            application.representative_role,
            application.document_type,
        )
    ):
        return False
    if not application.public_name or not application.professional_description:
        return False
    selected_categories = set(application.categories.values_list("pk", flat=True))
    if not selected_categories or application.main_category_id not in selected_categories:
        return False
    modes = set(application.service_modes or [])
    if not modes or not application.city or not application.state:
        return False
    if "HOME" in modes and (not application.service_region or not application.service_radius_km):
        return False
    if "FIXED" in modes and not all(
        (
            application.fixed_point_name,
            application.fixed_point_street,
            application.fixed_point_number,
            application.fixed_point_city,
            application.fixed_point_state,
        )
    ):
        return False
    if "REMOTE" in modes and not application.remote_scope:
        return False
    documents = {
        document.side
        for document in application.identity_documents.filter(prevalidation_passed=True)
    }
    return documents == {ProviderDocument.Side.FRONT, ProviderDocument.Side.BACK}


@transaction.atomic
def submit_application(*, application, actor):
    if not settings.PROVIDER_ONBOARDING_ENABLED or not settings.PROVIDER_DOCUMENT_UPLOAD_ENABLED:
        raise PermissionDenied("O envio de solicitações está temporariamente indisponível.")
    locked = ProviderApplication.objects.select_for_update().get(pk=application.pk, user=actor)
    if not locked.can_edit:
        if locked.status == ProviderApplication.Status.PENDING_REVIEW:
            return locked
        raise ValidationError("Esta solicitação não pode ser enviada neste estado.")
    if locked.current_step < 5 or not _application_ready(locked):
        raise ValidationError(
            "Conclua as etapas e envie as duas fotos legíveis antes de solicitar análise."
        )

    locked.status = ProviderApplication.Status.PENDING_REVIEW
    locked.review_status = ProviderApplication.ReviewStatus.NOT_REVIEWED
    locked.submitted_at = timezone.now()
    locked.reviewed_at = None
    locked.reviewer = None
    locked.decision_reason = ""
    locked.save(
        update_fields=[
            "status",
            "review_status",
            "submitted_at",
            "reviewed_at",
            "reviewer",
            "decision_reason",
            "updated_at",
        ]
    )
    AuditEvent.objects.create(
        actor=actor,
        action="provider.application.submitted",
        outcome=AuditEvent.Outcome.SUCCESS,
    )
    return locked
