from types import SimpleNamespace
from unittest.mock import patch

from api.v1.serializers import (
    PublicListingImageSerializer,
    PublicListingSerializer,
    PublicProviderDetailSerializer,
    PublicProviderSerializer,
)
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase
from django.urls import reverse

from apps.catalog.models import ServiceListing, ServiceListingImage
from apps.core.validators import validate_internal_destination, validate_public_image
from apps.providers.models import ProviderProfile

EMPTY_HOME = {
    "banners": [],
    "featured_categories": [],
    "specialties": [],
    "popular_providers": [],
    "popular_services": [],
    "other_services": [],
    "service_companies": [],
    "recent_listings": [],
}


class PublicHomeTests(SimpleTestCase):
    @patch("apps.core.views.header_categories", return_value=[])
    @patch("apps.core.views.home_sections", return_value=EMPTY_HOME)
    def test_home_renders_the_marketplace_sections_with_empty_states(
        self, _home_sections, _header_categories
    ):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BICO")
        self.assertContains(response, "Profissionais populares")
        self.assertContains(response, "Serviços mais procurados")
        self.assertContains(response, "Seu talento tem espaço na BICO.")
        self.assertContains(response, "Profissionais perto de você")
        self.assertContains(response, "Empresas que prestam serviços")
        self.assertContains(response, "Explore por especialidade")
        self.assertContains(response, "A descoberta de profissionais por localização")

    @patch("apps.core.views.header_categories", return_value=[])
    @patch("apps.core.views.home_sections", return_value=EMPTY_HOME)
    def test_home_uses_local_styles_scripts_and_official_branding(
        self, _home_sections, _header_categories
    ):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, "css/tokens.css")
        self.assertContains(response, "css/home.css")
        self.assertContains(response, "js/home.js")
        self.assertContains(response, "branding/logos/logo-bico-sem-fundo.png")
        self.assertContains(response, "branding/logos/logo-bico-quadrada.png")

    @patch("apps.core.views.header_categories", return_value=[])
    def test_informational_routes_render_without_broken_footer_links(self, _header_categories):
        slugs = (
            "quem-somos",
            "como-funciona",
            "seguranca",
            "termos",
            "privacidade",
            "ajuda",
            "suporte",
            "perguntas-frequentes",
            "para-prestadores",
            "regras-da-comunidade",
            "contato",
            "redes-sociais",
        )
        for slug in slugs:
            with self.subTest(slug=slug):
                response = self.client.get(reverse("core:info", args=[slug]))
                self.assertEqual(response.status_code, 200)

    def test_legacy_account_links_redirect_to_current_authentication_routes(self):
        destinations = {
            "entrar": "accounts:login",
            "criar-conta": "accounts:register",
            "minha-conta": "accounts:account",
            "conversar": "accounts:conversations",
            "notificacoes": "accounts:notifications",
        }
        for slug, destination in destinations.items():
            with self.subTest(slug=slug):
                response = self.client.get(reverse("core:info", args=[slug]))
                self.assertRedirects(response, reverse(destination), fetch_redirect_response=False)

    @patch("apps.core.views.header_categories", return_value=[])
    @patch("apps.core.views.active_categories", return_value=[])
    @patch("apps.core.views.search_listings", return_value=[])
    def test_search_page_renders_for_empty_results(self, _search, _categories, _header_categories):
        response = self.client.get(
            reverse("core:search"), {"q": "jardinagem", "cidade": "Campinas"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Serviços na BICO")
        self.assertContains(response, "Não encontramos serviços")

    @patch("apps.core.views.active_categories", return_value=[])
    def test_search_rejects_unbounded_query(self, _categories):
        response = self.client.get(reverse("core:search"), {"q": "x" * 101})

        self.assertEqual(response.status_code, 400)


class PublicApiTests(SimpleTestCase):
    def test_api_root_and_health_endpoints(self):
        self.assertEqual(
            self.client.get(reverse("api_v1:root")).json(), {"name": "BICO API", "version": "v1"}
        )
        self.assertEqual(self.client.get(reverse("api_v1:health")).json(), {"status": "ok"})

    @patch("api.v1.views.home_sections", return_value=EMPTY_HOME)
    def test_home_api_contains_public_sections(self, _home_sections):
        response = self.client.get(reverse("api_v1:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.json()),
            {
                "banners",
                "popular_providers",
                "featured_categories",
                "popular_services",
                "service_companies",
                "recent_listings",
            },
        )

    @patch("api.v1.views.public_categories", return_value=[])
    @patch("api.v1.views.search_public_providers", return_value=[])
    @patch("api.v1.views.search_public_listings", return_value=[])
    def test_list_endpoints_are_public_and_paginated(self, _listings, _providers, _categories):
        for route in ("api_v1:categories", "api_v1:providers", "api_v1:listings"):
            with self.subTest(route=route):
                response = self.client.get(reverse(route))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()["count"], 0)
                self.assertEqual(response.json()["results"], [])

    def test_public_discovery_api_does_not_accept_writes_or_options(self):
        path = reverse("api_v1:listings")
        self.assertEqual(self.client.post(path, data={"title": "fake"}).status_code, 405)
        self.assertEqual(self.client.put(path, data={"title": "fake"}).status_code, 405)
        self.assertEqual(self.client.delete(path).status_code, 405)
        self.assertEqual(self.client.options(path).status_code, 405)

    def test_public_provider_serializer_excludes_user_and_private_fields(self):
        fields = set(PublicProviderSerializer().fields)

        self.assertNotIn("user", fields)
        self.assertNotIn("email", fields)
        self.assertNotIn("status", fields)
        self.assertNotIn("approved_at", fields)

    def test_public_listing_contract_exposes_gallery_without_private_fields(self):
        fields = set(PublicListingSerializer().fields)

        self.assertIn("gallery_images", fields)
        self.assertIn("provider", fields)
        self.assertNotIn("status", fields)
        self.assertNotIn("created_at", fields)
        self.assertEqual(
            set(PublicListingImageSerializer().fields),
            {"image", "alt_text", "display_order"},
        )

    def test_public_provider_contract_exposes_public_listings(self):
        fields = set(PublicProviderDetailSerializer().fields)

        self.assertIn("listings", fields)
        self.assertNotIn("user", fields)
        self.assertNotIn("email", fields)

    def test_provider_list_serializer_does_not_expand_listing_queries(self):
        fields = set(PublicProviderSerializer().fields)

        self.assertNotIn("listings", fields)

    def test_anonymous_service_request_returns_to_login_before_placeholder(self):
        response = self.client.get(
            reverse("core:service-action-unavailable", args=["demo-servico-01", "solicitar"])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/entrar/", response.headers["Location"])
        self.assertIn("next=", response.headers["Location"])


class DomainValidationTests(SimpleTestCase):
    def test_listing_gallery_has_ordered_unique_slots_and_public_image_validation(self):
        self.assertEqual(ServiceListingImage._meta.ordering, ["display_order", "id"])
        constraints = ServiceListingImage._meta.constraints
        self.assertEqual(constraints[0].name, "catalog_listing_image_order_uniq")
        validators = ServiceListingImage._meta.get_field("image").validators
        self.assertIn(validate_public_image, validators)

    def test_listing_price_type_requires_price_consistency(self):
        quote_listing = ServiceListing(price_type=ServiceListing.PriceType.QUOTE, price_start=100)
        with self.assertRaises(ValidationError):
            quote_listing.clean()

        from_listing = ServiceListing(price_type=ServiceListing.PriceType.FROM, price_start=None)
        with self.assertRaises(ValidationError):
            from_listing.clean()

    def test_public_provider_state_is_normalized_and_validated(self):
        provider = ProviderProfile(state="sp")
        provider.clean()
        self.assertEqual(provider.state, "SP")

        with self.assertRaises(ValidationError):
            ProviderProfile(state="Sao").clean()

    def test_banner_destination_must_be_internal(self):
        validate_internal_destination("/servicos/")
        for destination in (
            "https://example.com",
            "//example.com",
            "javascript:alert(1)",
            "/\\evil",
        ):
            with self.subTest(destination=destination), self.assertRaises(ValidationError):
                validate_internal_destination(destination)

    def test_upload_validator_restricts_extensions_and_size(self):
        validate_public_image(SimpleUploadedFile("sample.webp", b"placeholder"))
        with self.assertRaises(ValidationError):
            validate_public_image(SimpleUploadedFile("sample.svg", b"<svg />"))
        too_large = SimpleNamespace(name="large.jpg", size=5 * 1024 * 1024 + 1)
        with self.assertRaises(ValidationError):
            validate_public_image(too_large)


class DemoSeedGuardTests(SimpleTestCase):
    @patch("apps.catalog.management.commands.seed_bico_demo.settings.DEBUG", False)
    @patch("apps.catalog.management.commands.seed_bico_demo.connection.vendor", "mysql")
    def test_demo_seed_is_blocked_when_debug_is_off(self):
        with self.assertRaises(CommandError):
            call_command("seed_bico_demo")

    @patch("apps.catalog.management.commands.seed_bico_demo.settings.DEBUG", True)
    @patch("apps.catalog.management.commands.seed_bico_demo.connection.vendor", "sqlite")
    def test_demo_seed_is_blocked_without_mysql(self):
        with self.assertRaises(CommandError):
            call_command("seed_bico_demo")
