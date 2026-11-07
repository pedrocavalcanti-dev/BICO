from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from .forms import (
    SERVICE_MODE_CHOICES,
    ProviderDocumentsForm,
    ProviderIdentityForm,
    ProviderProfileForm,
    ProviderReviewForm,
    ProviderServiceAreaForm,
    ProviderTypeForm,
)
from .models import ProviderApplication, ProviderDocument
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
