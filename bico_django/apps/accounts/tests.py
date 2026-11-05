from django.contrib.auth import get_user_model
from django.test import SimpleTestCase


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
