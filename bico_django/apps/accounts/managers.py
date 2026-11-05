from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email


class UserManager(BaseUserManager):
    use_in_migrations = True

    @staticmethod
    def normalize_email(email: str) -> str:
        return BaseUserManager.normalize_email(email.strip()).casefold()

    def _create_user(self, email: str, name: str, password: str | None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        if not name or not name.strip():
            raise ValueError("O nome é obrigatório.")

        email = self.normalize_email(email)
        validate_email(email)
        user = self.model(email=email, name=name.strip(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, name: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, name, password, **extra_fields)

    def create_superuser(self, email: str, name: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser deve possuir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser deve possuir is_superuser=True.")
        return self._create_user(email, name, password, **extra_fields)
