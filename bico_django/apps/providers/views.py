from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from apps.audit.models import AuditEvent
from apps.catalog.models import ServiceListing

from .dashboard import provider_dashboard_context, provider_listing_queryset
from .dashboard_forms import (
    ProviderManagedAreaForm,
    ProviderManagedProfileForm,
    ProviderPortfolioUploadForm,
)
from .forms import (
    SERVICE_MODE_CHOICES,
    ProviderDocumentsForm,
    ProviderIdentityForm,
    ProviderProfileForm,
    ProviderReviewForm,
    ProviderServiceAreaForm,
    ProviderTypeForm,
)
from .models import ProviderApplication, ProviderDocument, ProviderPortfolioImage, ProviderProfile
from .services import (
    get_or_create_application,
    replace_identity_document,
    submit_application,
    throttle_application_submission,
    throttle_document_upload,
)

STEPS = {
    1: (
        "Como você deseja prestar serviços?",
        "Escolha como pretende oferecer seus serviços na BICO.",
    ),
    2: (
        "Vamos conhecer você melhor",
        "Seus dados e documentos ficam privados. Eles serão usados na análise do cadastro.",
    ),
    3: (
        "O que você faz de melhor?",
        "Selecione as especialidades que pretende oferecer aos clientes da BICO.",
    ),
    4: ("Onde e como você atende?", "Defina sua região e as modalidades de atendimento."),
    5: (
        "Tudo pronto para o próximo passo?",
        "Confira seu cadastro. Depois do envio, a documentação seguirá para análise humana.",
    ),
}


def _unavailable(request):
    return render(request, "providers/unavailable.html", status=503)


@login_required
def onboarding_start(request):
    if not settings.PROVIDER_ONBOARDING_ENABLED:
        return _unavailable(request)
    application = get_or_create_application(request.user)
    if not application.can_edit:
        return redirect("providers:application-status")
    return redirect("providers:onboarding-step", step=max(1, min(application.current_step, 5)))


def _stage_form(step, request, application, *, post=False):
    data = request.POST if post else None
    if step == 1:
        return ProviderTypeForm(data, instance=application)
    if step == 2:
        if not application.provider_type:
            return None
        return ProviderIdentityForm(
            data, instance=application, provider_type=application.provider_type
        )
    if step == 3:
        return ProviderProfileForm(data, instance=application)
    if step == 4:
        return ProviderServiceAreaForm(data, instance=application)
    if step == 5:
        return ProviderReviewForm(
            data,
            request.FILES if post else None,
            application=application,
            submit=post and request.POST.get("action") == "submit",
        )
    raise Http404


@login_required
@never_cache
@require_http_methods(["GET", "POST"])
def onboarding_step(request, step):
    if not settings.PROVIDER_ONBOARDING_ENABLED:
        return _unavailable(request)
    if step not in STEPS:
        raise Http404
    application = get_or_create_application(request.user)
    if not application.can_edit:
        return redirect("providers:application-status")
    if step > application.current_step:
        return redirect("providers:onboarding-step", step=application.current_step)
    if step > 1 and not application.provider_type:
        return redirect("providers:onboarding-step", step=1)
    if step in {2, 5} and not settings.PROVIDER_DOCUMENT_UPLOAD_ENABLED:
        return _unavailable(request)

    form = _stage_form(step, request, application, post=request.method == "POST")
    if form is None:
        return redirect("providers:onboarding-step", step=1)
    document_form = (
        ProviderDocumentsForm(
            request.POST if request.method == "POST" else None,
            request.FILES if request.method == "POST" else None,
            application=application,
            submit=request.method == "POST" and request.POST.get("action") != "save_exit",
        )
        if step == 2
        else form
        if step == 5
        else None
    )

    rate_limited = False
    if request.method == "POST" and step in {2, 5}:
        if request.FILES and not throttle_document_upload(request).allowed:
            document_form.add_error(None, "Muitos envios de imagem. Aguarde e tente novamente.")
            rate_limited = True
        if (
            not rate_limited
            and step == 5
            and request.POST.get("action") == "submit"
            and not throttle_application_submission(request).allowed
        ):
            form.add_error(None, "Muitas solicitações de envio. Aguarde e tente novamente.")
            rate_limited = True

    valid = False
    if request.method == "POST" and not rate_limited:
        valid = form.is_valid()
        if step == 2:
            valid = document_form.is_valid() and valid
    if valid:
        try:
            if step in {2, 5}:
                for side, field_name in (
                    (ProviderDocument.Side.FRONT, "front_image"),
                    (ProviderDocument.Side.BACK, "back_image"),
                ):
                    upload = document_form.cleaned_data.get(field_name)
                    if upload:
                        replace_identity_document(application=application, side=side, upload=upload)
                if step == 5 and request.POST.get("action") == "submit":
                    application = submit_application(application=application, actor=request.user)
                    messages.success(
                        request,
                        "Solicitação enviada. Aguardando verificação documental e aprovação.",
                    )
                    return redirect("providers:application-status")
            if step < 5:
                application = form.save(commit=False)
                application.current_step = max(application.current_step, step + 1)
                application.save()
                if step == 3:
                    form.save_m2m()
            messages.success(request, "Alterações salvas. Seu rascunho está atualizado.")
            if request.POST.get("action") == "save_exit":
                return redirect("accounts:account")
            return redirect("providers:onboarding-step", step=min(step + 1, 5))
        except (PermissionDenied, ValidationError) as error:
            form.add_error(None, error)

    saved_documents = (
        {document.side: document for document in application.identity_documents.all()}
        if step in {2, 5}
        else {}
    )
    service_mode_labels = dict(SERVICE_MODE_CHOICES)
    context = {
        "application": application,
        "form": form,
        "document_form": document_form,
        "step": step,
        "steps": STEPS,
        "step_labels": [
            {"number": number, "label": label, "available": number <= application.current_step}
            for number, label in enumerate(
                ["Seu caminho", "Identificação", "Perfil profissional", "Atendimento", "Revisão"],
                start=1,
            )
        ],
        "progress": (step - 1) * 20,
        "max_categories": settings.PROVIDER_MAX_CATEGORIES,
        "title": STEPS[step][0],
        "subtitle": STEPS[step][1],
        "previous_step": step - 1 if step > 1 else None,
        "next_step": min(step + 1, 5),
        "service_mode_labels": [
            service_mode_labels[mode]
            for mode in application.service_modes
            if mode in service_mode_labels
        ],
        "document_uploads": [
            (
                ProviderDocument.Side.FRONT,
                "front_image",
                saved_documents.get(ProviderDocument.Side.FRONT),
                "Frente do documento",
            ),
            (
                ProviderDocument.Side.BACK,
                "back_image",
                saved_documents.get(ProviderDocument.Side.BACK),
                "Verso do documento",
            ),
        ],
        "form_status": (429 if rate_limited else 400 if request.method == "POST" else 200),
    }
    return render(request, "providers/onboarding_step.html", context, status=context["form_status"])


@login_required
@never_cache
def application_status(request):
    if not settings.PROVIDER_ONBOARDING_ENABLED:
        return _unavailable(request)
    application = get_or_create_application(request.user)
    if application.status in {
        ProviderApplication.Status.DRAFT,
        ProviderApplication.Status.NEEDS_CORRECTION,
    }:
        return redirect("providers:onboarding-step", step=max(1, min(application.current_step, 5)))
    return render(request, "providers/application_status.html", {"application": application})


@login_required
def identity_document_image(request, side):
    if side not in ProviderDocument.Side.values:
        raise Http404
    application = get_object_or_404(ProviderApplication, user=request.user)
    document = get_object_or_404(
        ProviderDocument.objects.filter(application=application, prevalidation_passed=True),
        side=side,
    )
    content_type = {
        "JPEG": "image/jpeg",
        "PNG": "image/png",
        "WEBP": "image/webp",
    }.get(document.detected_format)
    if not content_type:
        raise Http404
    response = FileResponse(document.file.open("rb"), content_type=content_type)
    response["Content-Disposition"] = (
        f'inline; filename="document-{side.lower()}.{document.detected_format.lower()}"'
    )
    response["Cache-Control"] = "private, no-store"
    response["X-Content-Type-Options"] = "nosniff"
    response["Content-Security-Policy"] = "default-src 'none'; sandbox"
    return response


def _approved_provider(request):
    provider = ProviderProfile.objects.filter(user=request.user).first()
    if provider and provider.status == ProviderProfile.Status.APPROVED:
        return provider, None
    if provider:
        return None, render(request, "providers/area_blocked.html", status=403)

    application = ProviderApplication.objects.filter(user=request.user).first()
    if application and application.status == ProviderApplication.Status.PENDING_REVIEW:
        return None, redirect("providers:application-status")
    if application and application.can_edit:
        return None, redirect(
            "providers:onboarding-step", step=max(1, min(application.current_step, 5))
        )
    return None, render(request, "providers/area_access.html")


@login_required
@never_cache
def dashboard(request):
    provider, denied = _approved_provider(request)
    if denied:
        return denied
    return render(request, "providers/dashboard.html", provider_dashboard_context(provider))


@login_required
@never_cache
def managed_listings(request):
    provider, denied = _approved_provider(request)
    if denied:
        return denied
    status_filter = request.GET.get("status", "").upper()
    query = request.GET.get("q", "").strip()[:100]
    listings = provider_listing_queryset(provider, status=status_filter, query=query)
    page_obj = Paginator(listings, 12).get_page(request.GET.get("page"))
    status_counts = {
        row["status"]: row["total"]
        for row in ServiceListing.objects.filter(provider=provider)
        .values("status")
        .order_by()
        .annotate(total=Count("id"))
    }
    return render(
        request,
        "providers/managed_listings.html",
        {
            "provider": provider,
            "page_obj": page_obj,
            "query": query,
            "status_filter": status_filter,
            "status_counts": status_counts,
            "status_choices": [
                {"value": value, "label": label, "count": status_counts.get(value, 0)}
                for value, label in ServiceListing.Status.choices
            ],
        },
    )


@login_required
@never_cache
@require_http_methods(["GET", "POST"])
def managed_profile(request):
    provider, denied = _approved_provider(request)
    if denied:
        return denied
    form = ProviderManagedProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=provider,
    )
    if request.method == "POST" and form.is_valid():
        previous_avatar = provider.avatar.name
        with transaction.atomic():
            managed = form.save(commit=False)
            update_fields = ["public_name", "description", "updated_at"]
            if "avatar" in form.changed_data:
                update_fields.append("avatar")
            managed.save(update_fields=update_fields)
            form.save_m2m()
            if previous_avatar and previous_avatar != managed.avatar.name:
                transaction.on_commit(lambda: provider.avatar.storage.delete(previous_avatar))
            AuditEvent.objects.create(
                actor=request.user,
                action="provider.dashboard.profile_updated",
                target_type="ProviderProfile",
                target_id=str(provider.pk),
            )
        messages.success(request, "Perfil profissional atualizado.")
        return redirect("providers:profile-edit")
    return render(
        request,
        "providers/managed_profile.html",
        {
            "provider": provider,
            "form": form,
            "public_url": reverse("core:provider-detail", args=[provider.slug]),
        },
    )


@login_required
@never_cache
def profile_preview(request):
    provider, denied = _approved_provider(request)
    if denied:
        return denied
    return render(request, "providers/profile_preview.html", {"provider": provider})


@login_required
@never_cache
@require_http_methods(["GET", "POST"])
def managed_service_area(request):
    provider, denied = _approved_provider(request)
    if denied:
        return denied
    application = ProviderApplication.objects.filter(user=request.user).first()
    if not application:
        return render(request, "providers/area_unavailable.html")
    form = ProviderManagedAreaForm(request.POST or None, instance=application)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            updated_application = form.save()
            ProviderProfile.objects.filter(pk=provider.pk).update(
                city=updated_application.city,
                state=updated_application.state,
            )
            AuditEvent.objects.create(
                actor=request.user,
                action="provider.dashboard.area_updated",
                target_type="ProviderProfile",
                target_id=str(provider.pk),
            )
        messages.success(request, "Modalidades e região de atendimento atualizadas.")
        return redirect("providers:service-area")
    return render(
        request,
        "providers/managed_service_area.html",
        {"provider": provider, "form": form},
    )


@login_required
@never_cache
@require_http_methods(["GET", "POST"])
def portfolio(request):
    provider, denied = _approved_provider(request)
    if denied:
        return denied
    form = ProviderPortfolioUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                ProviderProfile.objects.select_for_update().get(pk=provider.pk)
                image = form.save(provider=provider)
                AuditEvent.objects.create(
                    actor=request.user,
                    action="provider.dashboard.portfolio_added",
                    target_type="ProviderPortfolioImage",
                    target_id=str(image.pk),
                )
        except ValidationError as error:
            form.add_error(None, error)
        else:
            messages.success(request, "Imagem adicionada ao seu portfólio privado.")
            return redirect("providers:portfolio")
    images = provider.portfolio_images.all()
    return render(
        request, "providers/portfolio.html", {"provider": provider, "form": form, "images": images}
    )


@login_required
@never_cache
@require_http_methods(["GET"])
def portfolio_image(request, image_id):
    provider, denied = _approved_provider(request)
    if denied:
        return denied
    image = get_object_or_404(ProviderPortfolioImage, pk=image_id, provider=provider)
    response = FileResponse(image.image.open("rb"), content_type="image/webp")
    response["Content-Disposition"] = f'inline; filename="portfolio-{image.pk}.webp"'
    response["Cache-Control"] = "private, no-store"
    response["X-Content-Type-Options"] = "nosniff"
    response["Content-Security-Policy"] = "default-src 'none'; sandbox"
    return response


@login_required
@never_cache
@require_http_methods(["POST"])
def portfolio_reorder(request, image_id, direction):
    provider, denied = _approved_provider(request)
    if denied:
        return denied
    if direction not in {"up", "down"}:
        raise Http404
    with transaction.atomic():
        ProviderProfile.objects.select_for_update().get(pk=provider.pk)
        images = list(
            ProviderPortfolioImage.objects.select_for_update()
            .filter(provider=provider)
            .order_by("display_order", "created_at")
        )
        index = next((i for i, item in enumerate(images) if item.pk == image_id), None)
        if index is None:
            raise Http404
        neighbor_index = index - 1 if direction == "up" else index + 1
        if 0 <= neighbor_index < len(images):
            current, neighbor = images[index], images[neighbor_index]
            old_order = current.display_order
            neighbor_order = neighbor.display_order
            current.display_order = max(item.display_order for item in images) + 1
            current.save(update_fields=["display_order", "updated_at"])
            neighbor.display_order = old_order
            neighbor.save(update_fields=["display_order", "updated_at"])
            current.display_order = neighbor_order
            current.save(update_fields=["display_order", "updated_at"])
            AuditEvent.objects.create(
                actor=request.user,
                action="provider.dashboard.portfolio_reordered",
                target_type="ProviderPortfolioImage",
                target_id=str(current.pk),
            )
    return redirect("providers:portfolio")


@login_required
@never_cache
@require_http_methods(["POST"])
def portfolio_delete(request, image_id):
    provider, denied = _approved_provider(request)
    if denied:
        return denied
    image = get_object_or_404(ProviderPortfolioImage, pk=image_id, provider=provider)
    stored_name = image.image.name
    with transaction.atomic():
        image.delete()
        transaction.on_commit(lambda: image.image.storage.delete(stored_name))
        AuditEvent.objects.create(
            actor=request.user,
            action="provider.dashboard.portfolio_removed",
            target_type="ProviderPortfolioImage",
            target_id=str(image_id),
        )
    messages.success(request, "Imagem removida do portfólio privado.")
    return redirect("providers:portfolio")


@login_required
@never_cache
def professional_settings(request):
    provider, denied = _approved_provider(request)
    if denied:
        return denied
    application = ProviderApplication.objects.filter(user=request.user).first()
    return render(
        request,
        "providers/professional_settings.html",
        {
            "provider": provider,
            "application": application,
            "document_status": application.get_review_status_display()
            if application
            else "Indisponível",
        },
    )
