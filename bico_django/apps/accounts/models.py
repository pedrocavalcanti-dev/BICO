import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        ordering = ["email"]
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def clean(self):
        super().clean()
        if self.email:
            self.email = User.objects.normalize_email(self.email)
        if self.name:
            self.name = self.name.strip()

    def save(self, *args, **kwargs):
        if self.email:
            self.email = User.objects.normalize_email(self.email)
        if self.name:
            self.name = self.name.strip()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.email


class AuthThrottleBucket(models.Model):
    """Shared, privacy-preserving counter used to limit authentication attempts."""

    key = models.CharField(max_length=64, primary_key=True)
    window_started_at = models.DateTimeField(default=timezone.now, db_index=True)
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "limite de autenticação"
        verbose_name_plural = "limites de autenticação"

    def __str__(self) -> str:
        return f"Limite {self.key[:10]}"
