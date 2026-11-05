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
