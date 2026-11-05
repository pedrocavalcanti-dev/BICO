from django.test import SimpleTestCase
from django.urls import reverse


class PublicHomeTests(SimpleTestCase):
    def test_home_page_renders_bico_brand(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BICO")

    def test_home_page_uses_static_stylesheet(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, "css/site.css")

    def test_home_page_uses_official_bico_logos(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, "branding/logos/logo-bico-sem-fundo.png")
        self.assertContains(response, "branding/logos/logo-bico-quadrada.png")


class PublicApiTests(SimpleTestCase):
    def test_api_root_returns_versioned_service_metadata(self):
        response = self.client.get(reverse("api_v1:root"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"name": "BICO API", "version": "v1"})

    def test_health_endpoint_returns_liveness_status(self):
        response = self.client.get(reverse("api_v1:health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
