from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.exceptions import (
    PermissionDenied,
)
from rest_framework.exceptions import (
    ValidationError as APIValidationError,
)
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import (
    ProviderIdentityForm,
    ProviderProfileForm,
    ProviderServiceAreaForm,
    ProviderTypeForm,
)
from .models import ProviderDocument
from .serializers import ProviderApplicationSerializer
from .services import (
    get_or_create_application,
    replace_identity_document,
    submit_application,
    throttle_application_submission,
    throttle_document_upload,
)


class ProviderOnboardingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser]

    def _application(self, request):
        try:
            return get_or_create_application(request.user)
        except DjangoPermissionDenied as error:
            raise PermissionDenied(str(error)) from None

    def get(self, request):
        application = self._application(request)
        return Response(ProviderApplicationSerializer(application).data)

    def patch(self, request):
        application = self._application(request)
        if not application.can_edit:
            raise PermissionDenied("Esta solicitação não aceita alterações no momento.")
        try:
            step = int(request.data.get("step", ""))
        except (TypeError, ValueError):
            raise APIValidationError({"step": "Informe uma etapa de 1 a 4."}) from None
        forms = {
            1: lambda: ProviderTypeForm(request.data, instance=application),
            2: lambda: ProviderIdentityForm(
                request.data, instance=application, provider_type=application.provider_type
            ),
            3: lambda: ProviderProfileForm(request.data, instance=application),
            4: lambda: ProviderServiceAreaForm(request.data, instance=application),
        }
        if step not in forms:
            raise APIValidationError({"step": "As etapas editáveis vão de 1 a 4."})
        if step > 1 and not application.provider_type:
            raise APIValidationError(
                {"provider_type": "Conclua primeiro a etapa de tipo de prestador."}
            )
        form = forms[step]()
        if not form.is_valid():
            raise APIValidationError(form.errors)
        application = form.save(commit=False)
        application.current_step = max(application.current_step, step + 1)
        application.save()
        if step == 3:
            form.save_m2m()
        return Response(ProviderApplicationSerializer(application).data)


class ProviderDocumentUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        decision = throttle_document_upload(request)
        if not decision.allowed:
            response = Response(
                {"detail": "Muitos envios de imagem. Aguarde e tente novamente."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
            response["Retry-After"] = str(decision.retry_after)
            return response
        try:
            application = get_or_create_application(request.user)
            side = request.data.get("side")
            upload = request.FILES.get("file")
            if side not in ProviderDocument.Side.values:
                raise APIValidationError({"side": "Informe FRONT ou BACK."})
            if not upload:
                raise APIValidationError({"file": "Selecione uma imagem para enviar."})
            document = replace_identity_document(application=application, side=side, upload=upload)
        except DjangoPermissionDenied as error:
            raise PermissionDenied(str(error)) from None
        except ValidationError as error:
            raise APIValidationError({"file": error.messages}) from None
        return Response(
            {
                "side": document.side,
                "prevalidation_passed": document.prevalidation_passed,
                "message": (
                    "Imagem recebida para análise humana; autenticidade e correspondência "
                    "de identidade não foram verificadas."
                ),
            },
            status=status.HTTP_200_OK,
        )


class ProviderApplicationSubmitAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser]

    def post(self, request):
        decision = throttle_application_submission(request)
        if not decision.allowed:
            response = Response(
                {"detail": "Muitas solicitações de envio. Aguarde e tente novamente."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
            response["Retry-After"] = str(decision.retry_after)
            return response
        try:
            application = get_or_create_application(request.user)
            application = submit_application(application=application, actor=request.user)
        except DjangoPermissionDenied as error:
            raise PermissionDenied(str(error)) from None
        except ValidationError as error:
            raise APIValidationError({"detail": error.messages}) from None
        return Response(
            {
                "id": str(application.pk),
                "status": application.status,
                "message": "Aguardando verificação documental e aprovação.",
            },
            status=status.HTTP_200_OK,
        )
