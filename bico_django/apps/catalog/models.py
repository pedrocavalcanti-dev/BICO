import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.core.validators import validate_public_image


def _unique_slug(model, value, current_pk=None):
    base = slugify(value)[:140] or "servico"
    candidate = base
    suffix = 2
    queryset = model.objects.all()
    if current_pk:
        queryset = queryset.exclude(pk=current_pk)
    while queryset.filter(slug=candidate).exists():
        candidate = f"{base[:135]}-{suffix}"
        suffix += 1
    return candidate


class ServiceCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.CharField(max_length=240, blank=True)
    cover_image = models.ImageField(
        upload_to="catalog/categories/", blank=True, validators=[validate_public_image]
    )
    icon_path = models.CharField(max_length=180, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_specialty = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        indexes = [
            models.Index(fields=["is_active", "is_featured", "display_order"]),
            models.Index(fields=["is_active", "is_specialty", "display_order"]),
        ]
        verbose_name = "categoria de serviço"
        verbose_name_plural = "categorias de serviços"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(type(self), self.name, self.pk)
        return super().save(*args, **kwargs)


class ServiceListing(models.Model):
    MIN_PUBLICATION_IMAGE_COUNT = 2

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Rascunho"
        PUBLISHED = "PUBLISHED", "Publicado"
        PAUSED = "PAUSED", "Pausado"
        ARCHIVED = "ARCHIVED", "Arquivado"

    class PriceType(models.TextChoices):
        FROM = "FROM", "A partir de"
        QUOTE = "QUOTE", "Sob orçamento"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(
        "providers.ProviderProfile",
        on_delete=models.PROTECT,
        related_name="listings",
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name="listings",
    )
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField(max_length=3000)
    image = models.ImageField(
        upload_to="catalog/listings/", blank=True, validators=[validate_public_image]
    )
    price_start = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    price_type = models.CharField(max_length=8, choices=PriceType.choices, default=PriceType.QUOTE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False, editable=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "is_featured", "published_at"]),
            models.Index(fields=["status", "category", "published_at"]),
            models.Index(fields=["status", "city", "published_at"]),
        ]
        verbose_name = "anúncio de serviço"
        verbose_name_plural = "anúncios de serviços"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(type(self), self.title, self.pk)
        if self.state:
            self.state = self.state.upper()
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.price_type == self.PriceType.QUOTE and self.price_start is not None:
            raise ValidationError(
                {"price_start": "Anúncios sob orçamento não exibem preço inicial."}
            )
        if self.price_type == self.PriceType.FROM and self.price_start is None:
            raise ValidationError({"price_start": "Informe o preço inicial do serviço."})
        if self.state:
            self.state = self.state.upper()
            if len(self.state) != 2:
                raise ValidationError({"state": "Informe a sigla de um estado com duas letras."})

    def has_minimum_publication_images(self, gallery_images=None):
        images = [self.image]
        if gallery_images is None and self.pk and not self._state.adding:
            images.extend(self.gallery_images.values_list("image", flat=True))
        elif gallery_images is not None:
            images.extend(gallery_images)
        image_names = set()
        for image in images:
            name = image if isinstance(image, str) else getattr(image, "name", "")
            if name:
                image_names.add(name)
        return len(image_names) >= self.MIN_PUBLICATION_IMAGE_COUNT


class ServiceListingImage(models.Model):
    listing = models.ForeignKey(
        ServiceListing,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ImageField(
        upload_to="catalog/galleries/",
        validators=[validate_public_image],
    )
    alt_text = models.CharField(max_length=180)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["listing", "display_order"],
                name="catalog_listing_image_order_uniq",
            )
        ]
        verbose_name = "imagem da galeria do anúncio"
        verbose_name_plural = "imagens da galeria do anúncio"

    def __str__(self):
        return f"{self.listing.title} — {self.alt_text}"
