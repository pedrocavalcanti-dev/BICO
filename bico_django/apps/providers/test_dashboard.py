from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from apps.catalog.models import ServiceCategory, ServiceListing
from apps.providers.models import (
    ProviderApplication,
    ProviderPortfolioImage,
    ProviderProfile,
)
from apps.providers.storage import private_document_storage

User = get_user_model()


def make_portfolio_image():
    image = Image.new("RGB", (720, 480), "#477a44")
    output = BytesIO()
    image.save(output, format="JPEG")
    return SimpleUploadedFile("work.jpg", output.getvalue(), content_type="image/jpeg")


class ProviderDashboardAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="provider-dashboard@example.test",
            name="Dashboard User",
            password="StrongPass123!",
        )
        self.other = User.objects.create_user(
            email="other-dashboard@example.test", name="Other User", password="StrongPass123!"
        )
        self.category = ServiceCategory.objects.create(
            name="Dashboard specialty",
            slug="dashboard-specialty",
            is_active=True,
            is_specialty=True,
        )
        self.provider = ProviderProfile.objects.create(
            user=self.user,
            public_name="Profissional Próprio",
            city="Campinas",
            state="SP",
            status=ProviderProfile.Status.APPROVED,
        )
        self.provider.categories.add(self.category)
        self.other_provider = ProviderProfile.objects.create(
            user=self.other,
            public_name="Outro Profissional",
            city="Valinhos",
            state="SP",
            status=ProviderProfile.Status.APPROVED,
        )

    def test_dashboard_requires_a_real_approved_provider(self):
        anonymous = self.client.get(reverse("providers:dashboard"))
        self.assertEqual(anonymous.status_code, 302)

        self.client.force_login(self.other)
        self.other_provider.status = ProviderProfile.Status.SUSPENDED
        self.other_provider.save(update_fields=["status"])
        suspended = self.client.get(reverse("providers:dashboard"))
        self.assertEqual(suspended.status_code, 403)

        self.client.force_login(self.user)
        response = self.client.get(reverse("providers:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profissional Próprio")
        self.assertNotContains(response, "Outro Profissional")
        self.assertContains(response, "Visualizações")
        self.assertContains(response, "não estão disponíveis")

    def test_pending_and_draft_accounts_follow_existing_onboarding_routes(self):
        self.client.force_login(self.other)
        application = ProviderApplication.objects.create(
            user=self.other,
            status=ProviderApplication.Status.PENDING_REVIEW,
        )
        response = self.client.get(reverse("providers:dashboard"))
        self.assertRedirects(response, reverse("providers:application-status"))
        application.status = ProviderApplication.Status.DRAFT
        application.save(update_fields=["status"])
        response = self.client.get(reverse("providers:dashboard"))
        self.assertRedirects(response, reverse("providers:onboarding-step", args=[1]))

    def test_provider_listing_search_is_scoped_to_authenticated_provider(self):
        own = ServiceListing.objects.create(
            provider=self.provider,
            category=self.category,
            title="Meu serviço próprio",
            description="Uma descrição de serviço suficientemente clara.",
            price_type=ServiceListing.PriceType.QUOTE,
            city="Campinas",
            state="SP",
        )
        ServiceListing.objects.create(
            provider=self.other_provider,
            category=self.category,
            title="Segredo de outro profissional",
            description="Este anúncio pertence a outra conta.",
            price_type=ServiceListing.PriceType.QUOTE,
            city="Valinhos",
            state="SP",
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("providers:managed-listings"), {"q": "Meu serviço"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, own.title)
        self.assertNotContains(response, "Segredo de outro profissional")

    def test_profile_update_uses_allowlisted_fields(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("providers:profile-edit"),
            {
                "public_name": "Novo nome público",
                "description": "Apresentação atualizada.",
                "categories": [str(self.category.pk)],
                "status": ProviderProfile.Status.SUSPENDED,
                "user": str(self.other.pk),
            },
        )
        self.assertRedirects(response, reverse("providers:profile-edit"))
        self.provider.refresh_from_db()
        self.assertEqual(self.provider.public_name, "Novo nome público")
        self.assertEqual(self.provider.user_id, self.user.pk)
        self.assertEqual(self.provider.status, ProviderProfile.Status.APPROVED)

    def test_provider_dashboard_api_is_authenticated_and_returns_real_counts(self):
        own_listing = ServiceListing.objects.create(
            provider=self.provider,
            category=self.category,
            title="Anúncio do próprio prestador",
            description="Descrição real do anúncio.",
            price_type=ServiceListing.PriceType.QUOTE,
            city="Campinas",
            state="SP",
            status=ServiceListing.Status.PUBLISHED,
        )
        ServiceListing.objects.create(
            provider=self.other_provider,
            category=self.category,
            title="Anúncio de outra conta",
            description="Não pode entrar na contagem.",
            price_type=ServiceListing.PriceType.QUOTE,
            city="Valinhos",
            state="SP",
            status=ServiceListing.Status.PUBLISHED,
        )
        url = reverse("api_v1:provider-me-dashboard")
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["listings"]["published"], 1)
        self.assertIsNone(response.json()["views"])
        self.assertTrue(own_listing.provider_id == self.provider.pk)


@override_settings(PROVIDER_ONBOARDING_ENABLED=True)
class ProviderPortfolioTests(TestCase):
    def setUp(self):
        self.temp_storage = TemporaryDirectory()
        self.addCleanup(self.temp_storage.cleanup)
        original_location = private_document_storage._location
        private_document_storage._location = self.temp_storage.name
        self.addCleanup(setattr, private_document_storage, "_location", original_location)
        self.user = User.objects.create_user(
            email="portfolio@example.test", name="Portfolio User", password="StrongPass123!"
        )
        self.other = User.objects.create_user(
            email="portfolio-other@example.test", name="Portfolio Other", password="StrongPass123!"
        )
        self.provider = ProviderProfile.objects.create(
            user=self.user,
            public_name="Portfolio User",
            city="Campinas",
            state="SP",
            status=ProviderProfile.Status.APPROVED,
        )
        self.other_provider = ProviderProfile.objects.create(
            user=self.other,
            public_name="Portfolio Other",
            city="Valinhos",
            state="SP",
            status=ProviderProfile.Status.APPROVED,
        )

    def test_portfolio_upload_is_reencoded_private_and_owner_scoped(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("providers:portfolio"),
            {"image": make_portfolio_image(), "description": "Instalação concluída"},
        )
        self.assertRedirects(response, reverse("providers:portfolio"))
        image = ProviderPortfolioImage.objects.get(provider=self.provider)
        self.assertTrue(image.image.name.endswith(".webp"))
        self.assertFalse(image.image.storage.path(image.image.name).endswith("static"))
        with self.assertRaises(ValueError):
            image.image.url

        owner_response = self.client.get(reverse("providers:portfolio-image", args=[image.pk]))
        self.assertEqual(owner_response.status_code, 200)
        self.assertEqual(owner_response["Cache-Control"], "private, no-store")
        self.assertTrue(b"RIFF" in b"".join(owner_response.streaming_content)[:12])

        self.client.force_login(self.other)
        denied_response = self.client.get(reverse("providers:portfolio-image", args=[image.pk]))
        self.assertEqual(denied_response.status_code, 404)
        delete_response = self.client.post(reverse("providers:portfolio-delete", args=[image.pk]))
        self.assertEqual(delete_response.status_code, 404)
        self.assertTrue(ProviderPortfolioImage.objects.filter(pk=image.pk).exists())

    def test_portfolio_rejects_unreadable_upload(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("providers:portfolio"),
            {"image": SimpleUploadedFile("fake.jpg", b"not an image"), "description": ""},
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(ProviderPortfolioImage.objects.exists())

    def test_portfolio_order_can_be_changed_by_its_owner(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("providers:portfolio"),
            {"image": make_portfolio_image(), "description": "Primeira"},
        )
        self.client.post(
            reverse("providers:portfolio"),
            {"image": make_portfolio_image(), "description": "Segunda"},
        )
        images = list(self.provider.portfolio_images.order_by("display_order"))
        response = self.client.post(
            reverse("providers:portfolio-reorder", args=[images[1].pk, "up"])
        )
        self.assertRedirects(response, reverse("providers:portfolio"))
        images = list(self.provider.portfolio_images.order_by("display_order"))
        self.assertEqual([image.description for image in images], ["Segunda", "Primeira"])
