import json
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class UserModelContractTests(SimpleTestCase):
    def test_email_is_the_login_identifier(self):
        user_model = get_user_model()

        self.assertEqual(user_model.USERNAME_FIELD, "email")
        self.assertTrue(user_model._meta.get_field("email").unique)

    def test_public_user_identifier_is_a_uuid(self):
        user_model = get_user_model()

        self.assertEqual(user_model._meta.pk.get_internal_type(), "UUIDField")

    def test_email_normalization_is_case_insensitive(self):
        manager = get_user_model().objects

        self.assertEqual(manager.normalize_email("  Pessoa@Exemplo.COM "), "pessoa@exemplo.com")


class AccountWebFlowTests(TestCase):
    password = "T7!wQ4#nV8$kP2x"

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="cliente@example.com", name="Cliente BICO", password=self.password
        )

    def test_registration_creates_a_normalized_user_and_starts_a_session(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "name": "  Ana Cliente  ",
                "email": "  Ana@Example.COM ",
                "password1": "N8!tZ5#qM3$kL7p",
                "password2": "N8!tZ5#qM3$kL7p",
            },
        )

        self.assertRedirects(response, reverse("accounts:account"))
        user = get_user_model().objects.get(email="ana@example.com")
        self.assertEqual(user.name, "Ana Cliente")
        self.assertTrue(user.check_password("N8!tZ5#qM3$kL7p"))
        self.assertNotEqual(user.password, "N8!tZ5#qM3$kL7p")
        self.assertEqual(str(self.client.session.get("_auth_user_id")), str(user.pk))

    def test_duplicate_registration_email_is_normalized_and_rejected(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "name": "Outra pessoa",
                "email": "CLIENTE@EXAMPLE.COM",
                "password1": "N8!tZ5#qM3$kL7p",
                "password2": "N8!tZ5#qM3$kL7p",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "j\u00e1 possui uma conta", status_code=400)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_weak_password_is_rejected_by_django_validators(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "name": "Ana Cliente",
                "email": "ana@example.com",
                "password1": "12345678",
                "password2": "12345678",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "senha", status_code=400)
        self.assertFalse(get_user_model().objects.filter(email="ana@example.com").exists())

    def test_login_success_and_generic_invalid_credentials(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "  CLIENTE@EXAMPLE.COM ", "password": self.password},
        )

        self.assertRedirects(response, reverse("accounts:account"))
        self.client.post(reverse("accounts:logout"))
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "unknown@example.com", "password": self.password},
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "E-mail ou senha", status_code=400)

    def test_login_returns_only_a_safe_next_destination(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": self.user.email,
                "password": self.password,
                "next": "/servicos/?q=jardim",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/servicos/?q=jardim")

        self.client.post(reverse("accounts:logout"))
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": self.user.email,
                "password": self.password,
                "next": "https://attacker.example/",
            },
        )
        self.assertEqual(response["Location"], reverse("accounts:account"))

    def test_logout_is_post_only_and_invalidates_the_session(self):
        self.client.force_login(self.user)
        get_response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(get_response.status_code, 405)

        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("core:home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_home_is_public_and_account_requires_authentication(self):
        self.assertEqual(self.client.get(reverse("core:home")).status_code, 200)
        response = self.client.get(reverse("accounts:account"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["Location"].startswith(reverse("accounts:login")))

        self.client.force_login(self.user)
        response = self.client.get(reverse("accounts:account"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.email)
        self.assertContains(response, "confirma\u00e7\u00e3o de e-mail ainda n\u00e3o est\u00e1")

    def test_profile_update_accepts_only_name_and_ignores_privilege_fields(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("accounts:account_edit"),
            {"name": "Novo nome", "is_staff": "true", "is_superuser": "true"},
        )

        self.assertRedirects(response, reverse("accounts:account"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Novo nome")
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_profile_rejects_blank_name(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("accounts:account_edit"), {"name": "   "})
        self.assertEqual(response.status_code, 400)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Cliente BICO")

    def test_password_change_requires_current_password_and_updates_hash(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("accounts:password_change"),
            {
                "old_password": "incorreta",
                "new_password1": "Y2!rV7#pC5$zM9q",
                "new_password2": "Y2!rV7#pC5$zM9q",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "senha atual", status_code=200)

        response = self.client.post(
            reverse("accounts:password_change"),
            {
                "old_password": self.password,
                "new_password1": "Y2!rV7#pC5$zM9q",
                "new_password2": "Y2!rV7#pC5$zM9q",
            },
        )
        self.assertRedirects(response, reverse("accounts:password_change_done"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Y2!rV7#pC5$zM9q"))

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_is_neutral_and_native_token_changes_password(self):
        response = self.client.post(
            reverse("accounts:password_reset"), {"email": "missing@example.com"}
        )
        self.assertRedirects(response, reverse("accounts:password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(
            reverse("accounts:password_reset"), {"email": self.user.email.upper()}
        )
        self.assertRedirects(response, reverse("accounts:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        match = re.search(r"/redefinir-senha/(?P<uid>[^/]+)/(?P<token>[^/]+)/", mail.outbox[0].body)
        self.assertIsNotNone(match)
        url = reverse(
            "accounts:password_reset_confirm",
            kwargs={"uidb64": match.group("uid"), "token": match.group("token")},
        )
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(
            url,
            {
                "new_password1": "Y2!rV7#pC5$zM9q",
                "new_password2": "Y2!rV7#pC5$zM9q",
            },
        )
        self.assertRedirects(response, reverse("accounts:password_reset_complete"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Y2!rV7#pC5$zM9q"))

    def test_password_reset_rejects_an_invalid_or_expired_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        invalid_url = reverse(
            "accounts:password_reset_confirm", kwargs={"uidb64": uid, "token": "invalid"}
        )
        self.assertContains(self.client.get(invalid_url), "Link inv\u00e1lido ou expirado")

        token = default_token_generator.make_token(self.user)
        expired_url = reverse(
            "accounts:password_reset_confirm", kwargs={"uidb64": uid, "token": token}
        )
        with override_settings(PASSWORD_RESET_TIMEOUT=-1):
            self.assertContains(self.client.get(expired_url), "Link inv\u00e1lido ou expirado")

    def test_registration_is_rate_limited(self):
        data = {
            "name": "Outra pessoa",
            "email": "outra@example.com",
            "password1": "N8!tZ5#qM3$kL7p",
            "password2": "N8!tZ5#qM3$kL7p",
        }
        # Invalid data still consumes the shared IP bucket before validation.
        for _ in range(5):
            self.client.post(reverse("accounts:register"), {**data, "password2": "different"})
        response = self.client.post(reverse("accounts:register"), data)
        self.assertEqual(response.status_code, 429)
        self.assertIn("Retry-After", response.headers)


class UserMeApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="cliente@example.com", name="Cliente BICO", password="T7!wQ4#nV8$kP2x"
        )
        self.url = reverse("api_v1:user-me")

    def test_anonymous_user_cannot_access_me_endpoint(self):
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_authenticated_get_returns_only_publicly_permitted_profile_fields(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json()), {"name", "email", "created_at"})
        self.assertEqual(response.json()["email"], self.user.email)

    def test_patch_changes_name_and_ignores_forbidden_fields(self):
        self.client.force_login(self.user)
        response = self.client.patch(
            self.url,
            data=json.dumps(
                {
                    "name": "Nome pela API",
                    "is_staff": True,
                    "is_superuser": True,
                    "id": "00000000-0000-0000-0000-000000000000",
                    "groups": [1],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Nome pela API")
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertNotIn("id", response.json())

    def test_patch_validates_name_and_put_is_disabled(self):
        self.client.force_login(self.user)
        response = self.client.patch(self.url, {"name": "   "}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.put(self.url).status_code, 405)

    def test_session_api_mutations_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.get(reverse("accounts:login"))
        client.force_login(self.user)
        payload = json.dumps({"name": "Nome com CSRF"})
        response = client.patch(self.url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        token = client.cookies["csrftoken"].value
        response = client.patch(
            self.url,
            data=payload,
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, 200)
