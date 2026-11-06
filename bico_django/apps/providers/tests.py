from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image, ImageDraw

from apps.audit.models import AuditEvent
from apps.catalog.models import ServiceCategory

from .document_validation import validate_document_file
from .models import ProviderApplication, ProviderDocument
from .services import replace_identity_document, submit_application
from .storage import private_document_storage

User = get_user_model()


def make_document_image(*, size=(1200, 800), image_format="JPEG"):
    image = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(image)
    for x in range(0, size[0], 24):
        draw.line((x, 0, x, size[1]), fill=(30, 70, 120), width=3)
    for y in range(0, size[1], 24):
        draw.line((0, y, size[0], y), fill=(190, 80, 30), width=2)
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp", "GIF": "gif"}[image_format]
    return SimpleUploadedFile(
        f"private-name.{extension}", buffer.getvalue(), content_type="application/octet-stream"
    )


@override_settings(
    PROVIDER_ONBOARDING_ENABLED=True,
    PROVIDER_DOCUMENT_UPLOAD_ENABLED=True,
)
class ProviderDocumentUploadTests(TestCase):
    def setUp(self):
        self.temp_storage = TemporaryDirectory()
        self.addCleanup(self.temp_storage.cleanup)
        self.original_location = private_document_storage._location
        private_document_storage._location = self.temp_storage.name
        self.addCleanup(setattr, private_document_storage, "_location", self.original_location)

        self.user = User.objects.create_user(
            email="provider@example.test", name="Provider Test", password="StrongPass123!"
        )
        self.application = ProviderApplication.objects.create(
            user=self.user,
            provider_type=ProviderApplication.ProviderType.INDIVIDUAL,
            legal_name="Provider Test",
            cpf="52998224725",
            birth_date="1990-01-01",
            phone="19999999999",
            document_type=ProviderApplication.DocumentType.CIN,
            public_name="Serviços do Provider",
            professional_description="Descrição do trabalho e serviços prestados.",
            current_step=5,
            service_modes=["HOME"],
            city="Campinas",
            state="SP",
            service_region="Região central",
            service_radius_km=20,
        )
        self.category = ServiceCategory.objects.create(
            name="Especialidade de teste",
            slug="especialidade-de-teste",
            is_active=True,
            is_specialty=True,
        )
        self.application.main_category = self.category
        self.application.save(update_fields=["main_category"])
        self.application.categories.add(self.category)

    def test_real_image_format_and_quality_are_validated(self):
        upload = make_document_image(image_format="PNG")
        validate_document_file(upload)
        self.assertEqual(upload.detected_format, "PNG")

        corrupt = SimpleUploadedFile("photo.jpg", b"not an image", content_type="image/jpeg")
        with self.assertRaises(ValidationError):
            validate_document_file(corrupt)

        small = make_document_image(size=(320, 240))
        with self.assertRaisesMessage(ValidationError, "800"):
            validate_document_file(small)

    def test_upload_is_private_and_only_the_owner_can_preview(self):
        document = replace_identity_document(
            application=self.application,
            side=ProviderDocument.Side.FRONT,
            upload=make_document_image(),
        )
        path = Path(private_document_storage.path(document.file.name))
        self.assertTrue(path.is_file())
        self.assertNotIn("static", path.parts)
        self.assertNotIn("private-name", document.file.name)
        self.assertFalse(path.read_bytes().startswith(b"\xff\xd8\xff"))
        with self.assertRaises(ValueError):
            document.file.url

        self.client.force_login(self.user)
        owner_response = self.client.get(reverse("providers:document-image", args=["FRONT"]))
        self.assertEqual(owner_response.status_code, 200)
        self.assertEqual(owner_response["Cache-Control"], "private, no-store")
        streamed_image = b"".join(owner_response.streaming_content)
        self.assertTrue(streamed_image.startswith(b"\xff\xd8\xff"))

        other_user = User.objects.create_user(
            email="other@example.test", name="Other User", password="StrongPass123!"
        )
        self.client.force_login(other_user)
        other_response = self.client.get(reverse("providers:document-image", args=["FRONT"]))
        self.assertEqual(other_response.status_code, 404)

    def test_submission_requires_both_sides_and_persists_pending_human_review(self):
        replace_identity_document(
            application=self.application,
            side=ProviderDocument.Side.FRONT,
            upload=make_document_image(),
        )
        with self.assertRaisesMessage(ValidationError, "duas fotos"):
            submit_application(application=self.application, actor=self.user)

        replace_identity_document(
            application=self.application,
            side=ProviderDocument.Side.BACK,
            upload=make_document_image(image_format="WEBP"),
        )
        submitted = submit_application(application=self.application, actor=self.user)
        submitted.refresh_from_db()

        self.assertEqual(submitted.status, ProviderApplication.Status.PENDING_REVIEW)
        self.assertEqual(submitted.review_status, ProviderApplication.ReviewStatus.NOT_REVIEWED)
        self.assertIsNone(submitted.reviewer_id)
        self.assertEqual(submitted.identity_documents.filter(prevalidation_passed=True).count(), 2)
        self.assertTrue(AuditEvent.objects.filter(action="provider.application.submitted").exists())

    def test_user_cannot_patch_review_fields_through_the_onboarding_api(self):
        self.client.force_login(self.user)
        response = self.client.patch(
            reverse("api_v1:provider-onboarding"),
            data={"step": 1, "provider_type": "INDIVIDUAL", "review_status": "APPROVED"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.application.refresh_from_db()
        self.assertEqual(
            self.application.review_status, ProviderApplication.ReviewStatus.NOT_REVIEWED
        )
