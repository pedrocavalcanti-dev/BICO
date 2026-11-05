import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_internal_destination, validate_public_image


class HomeBanner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=240, blank=True)
    image = models.ImageField(
        upload_to="core/banners/", blank=True, validators=[validate_public_image]
    )
    mobile_image = models.ImageField(
        upload_to="core/banners/mobile/", blank=True, validators=[validate_public_image]
    )
    image_alt = models.CharField(max_length=180, blank=True)
    action_label = models.CharField(max_length=48, blank=True)
    destination = models.CharField(
        max_length=240, default="/servicos/", validators=[validate_internal_destination]
    )
    display_order = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(99)]
    )
    is_active = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "created_at"]
        indexes = [models.Index(fields=["is_active", "display_order"])]
        verbose_name = "banner da Home"
        verbose_name_plural = "banners da Home"

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if (self.image or self.mobile_image) and not self.image_alt.strip():
            raise ValidationError({"image_alt": "Informe o texto alternativo das imagens."})
