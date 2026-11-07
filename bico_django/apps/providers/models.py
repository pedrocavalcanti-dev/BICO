import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from apps.core.validators import validate_public_image

from .document_validation import document_upload_path
from .storage import private_document_storage


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


class ProviderApplication(models.Model):
    class ProviderType(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Pessoa física"
        COMPANY = "COMPANY", "Pessoa jurídica"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Cadastro em andamento"
        PENDING_REVIEW = "PENDING_REVIEW", "Aguardando análise"
        NEEDS_CORRECTION = "NEEDS_CORRECTION", "Correção necessária"
        APPROVED = "APPROVED", "Aprovado"
        REJECTED = "REJECTED", "Não aprovado"
        SUSPENDED = "SUSPENDED", "Suspenso"

    class ReviewStatus(models.TextChoices):
        NOT_REVIEWED = "NOT_REVIEWED", "Não revisado"
        APPROVED = "APPROVED", "Aprovado"
        REJECTED = "REJECTED", "Rejeitado"

    class DocumentType(models.TextChoices):
        RG = "RG", "RG"
        CIN = "CIN", "CIN"
        CNH = "CNH", "CNH"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provider_application",
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    current_step = models.PositiveSmallIntegerField(default=1)
    provider_type = models.CharField(max_length=10, choices=ProviderType.choices, blank=True)

    # Private identity/contact information. Production onboarding remains disabled pending review.
    legal_name = models.CharField(max_length=150, blank=True)
    cpf = models.CharField(max_length=11, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    document_type = models.CharField(max_length=3, choices=DocumentType.choices, blank=True)
    identity_document_number = models.CharField(max_length=32, blank=True)
    issuing_authority = models.CharField(max_length=40, blank=True)
    issuer_state = models.CharField(max_length=2, blank=True)
    company_legal_name = models.CharField(max_length=180, blank=True)
    company_trade_name = models.CharField(max_length=180, blank=True)
    cnpj = models.CharField(max_length=14, blank=True)
    company_email = models.EmailField(blank=True)
    company_phone = models.CharField(max_length=20, blank=True)
    representative_name = models.CharField(max_length=150, blank=True)
    representative_cpf = models.CharField(max_length=11, blank=True)
    representative_phone = models.CharField(max_length=20, blank=True)
    representative_role = models.CharField(max_length=100, blank=True)

    public_name = models.CharField(max_length=150, blank=True)
    professional_description = models.CharField(max_length=2000, blank=True)
    experience_years = models.PositiveSmallIntegerField(blank=True, null=True)
    main_category = models.ForeignKey(
        "catalog.ServiceCategory",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="main_provider_applications",
    )
    categories = models.ManyToManyField(
        "catalog.ServiceCategory", blank=True, related_name="provider_applications"
    )

    service_modes = models.JSONField(default=list, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    service_region = models.CharField(max_length=120, blank=True)
    service_radius_km = models.PositiveSmallIntegerField(blank=True, null=True)
    remote_scope = models.CharField(max_length=20, blank=True)
    fixed_point_name = models.CharField(max_length=120, blank=True)
    fixed_point_postal_code = models.CharField(max_length=9, blank=True)
    fixed_point_street = models.CharField(max_length=180, blank=True)
    fixed_point_number = models.CharField(max_length=20, blank=True)
    fixed_point_complement = models.CharField(max_length=100, blank=True)
    fixed_point_neighborhood = models.CharField(max_length=100, blank=True)
    fixed_point_city = models.CharField(max_length=100, blank=True)
    fixed_point_state = models.CharField(max_length=2, blank=True)
    fixed_point_public = models.BooleanField(default=False)

    review_status = models.CharField(
        max_length=12, choices=ReviewStatus.choices, default=ReviewStatus.NOT_REVIEWED
    )
    decision_reason = models.TextField(blank=True)
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="provider_applications_reviewed",
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [models.Index(fields=["status", "updated_at"])]
        verbose_name = "solicitação de cadastro profissional"
        verbose_name_plural = "solicitações de cadastro profissional"

    def __str__(self):
        return f"Solicitação {self.pk} ({self.status})"

    @property
    def can_edit(self):
        return self.status in {self.Status.DRAFT, self.Status.NEEDS_CORRECTION}


class ProviderDocument(models.Model):
    class Side(models.TextChoices):
        FRONT = "FRONT", "Frente"
        BACK = "BACK", "Verso"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        ProviderApplication,
        on_delete=models.CASCADE,
        related_name="identity_documents",
    )
    side = models.CharField(max_length=5, choices=Side.choices)
    file = models.ImageField(storage=private_document_storage, upload_to=document_upload_path)
    detected_format = models.CharField(max_length=5, blank=True)
    prevalidation_passed = models.BooleanField(default=False)
    prevalidation_feedback = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["side"]
        constraints = [
            models.UniqueConstraint(
                fields=["application", "side"], name="provider_document_side_uniq"
            )
        ]
        verbose_name = "imagem privada de documento"
        verbose_name_plural = "imagens privadas de documentos"

    def __str__(self):
        return f"Documento {self.side.lower()} da solicitação {self.application_id}"


class ProviderPortfolioImage(models.Model):
    """Private work samples managed by their owner until portfolio moderation exists."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name="portfolio_images",
    )
    image = models.ImageField(
        storage=private_document_storage,
        upload_to="provider-portfolio/",
    )
    description = models.CharField(max_length=180, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "created_at"]
        indexes = [models.Index(fields=["provider", "display_order"])]
        verbose_name = "imagem de portfólio privado"
        verbose_name_plural = "imagens de portfólio privado"

    def __str__(self):
        return f"Imagem de portfólio de {self.provider.public_name}"
