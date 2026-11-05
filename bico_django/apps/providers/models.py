import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from apps.core.validators import validate_public_image


class ProviderProfile(models.Model):
    class ProviderType(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Profissional autônomo"
        COMPANY = "COMPANY", "Empresa prestadora"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Aguardando análise"
        APPROVED = "APPROVED", "Aprovado para publicação"
        REJECTED = "REJECTED", "Não aprovado"
        SUSPENDED = "SUSPENDED", "Suspenso"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provider_profile",
    )
    provider_type = models.CharField(
        max_length=10, choices=ProviderType.choices, default=ProviderType.INDIVIDUAL
    )
    public_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    avatar = models.ImageField(
        upload_to="providers/avatars/", blank=True, validators=[validate_public_image]
    )
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    categories = models.ManyToManyField(
        "catalog.ServiceCategory", blank=True, related_name="providers"
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    is_featured = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False, editable=False)
    approved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["public_name"]
        indexes = [
            models.Index(fields=["status", "provider_type", "is_featured"]),
            models.Index(fields=["status", "city", "public_name"]),
        ]
        verbose_name = "perfil profissional"
        verbose_name_plural = "perfis profissionais"

    def __str__(self):
        return self.public_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.public_name)[:140] or "prestador"
            candidate = base
            suffix = 2
            queryset = type(self).objects.exclude(pk=self.pk)
            while queryset.filter(slug=candidate).exists():
                candidate = f"{base[:135]}-{suffix}"
                suffix += 1
            self.slug = candidate
        if self.state:
            self.state = self.state.upper()
        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.state:
            self.state = self.state.upper()
            if len(self.state) != 2:
                raise ValidationError({"state": "Informe a sigla de um estado com duas letras."})
