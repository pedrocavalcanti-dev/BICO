from django.test import SimpleTestCase
from rest_framework.test import APIClient


class PublicApiTests(SimpleTestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_root_returns_name_and_version(self):
        response = self.client.get("/api/v1/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"name": "BICO API", "version": "v1"})

    def test_health_returns_only_liveness_status(self):
        response = self.client.get("/api/v1/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
