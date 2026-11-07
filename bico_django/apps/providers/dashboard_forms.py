import io

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db.models import Max
from PIL import Image, ImageOps, UnidentifiedImageError

from apps.catalog.models import ServiceCategory
from apps.core.validators import MAX_PUBLIC_IMAGE_BYTES

from .forms import STATE_CHOICES
from .models import ProviderApplication, ProviderPortfolioImage, ProviderProfile

MAX_PORTFOLIO_IMAGES = 20
MAX_PORTFOLIO_PIXELS = 20_000_000


class ProviderManagedProfileForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=ServiceCategory.objects.filter(is_active=True, is_specialty=True),
        required=True,
        label="Especialidades",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = ProviderProfile
        fields = ["public_name", "description", "avatar", "categories"]
        widgets = {"description": forms.Textarea(attrs={"rows": 5, "maxlength": 2000})}
        labels = {
            "public_name": "Nome profissional ou empresa",
            "description": "Apresentação",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["public_name"].max_length = 150
        self.fields["categories"].queryset = ServiceCategory.objects.filter(
            is_active=True, is_specialty=True
        )

    def clean_avatar(self):
        upload = self.cleaned_data.get("avatar")
        if not upload:
            return upload
        try:
            upload.seek(0)
            source = Image.open(upload)
            if source.format not in {"JPEG", "PNG", "WEBP"}:
                raise ValidationError("Envie uma foto JPG, PNG ou WebP.")
            if source.width < 160 or source.height < 160:
                raise ValidationError("A imagem deve ter pelo menos 160 × 160 pixels.")
            if source.width * source.height > MAX_PORTFOLIO_PIXELS:
                raise ValidationError("A resolução máxima é de 20 megapixels.")
            source.verify()
            upload.seek(0)
            with Image.open(upload) as image:
                normalized = ImageOps.exif_transpose(image).convert("RGB")
                normalized.thumbnail((1200, 1200))
                buffer = io.BytesIO()
                normalized.save(buffer, format="WEBP", quality=86, method=4)
            upload.seek(0)
            return ContentFile(buffer.getvalue(), name="avatar.webp")
        except ValidationError:
            raise
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
            raise ValidationError("O arquivo está ilegível. Envie uma imagem válida.") from None
        finally:
            upload.seek(0)


class ProviderManagedAreaForm(forms.ModelForm):
    service_modes = forms.MultipleChoiceField(
        choices=(("HOME", "A domicílio"), ("FIXED", "Em ponto fixo"), ("REMOTE", "Remoto")),
        widget=forms.CheckboxSelectMultiple,
        label="Modalidades de atendimento",
    )

    class Meta:
        model = ProviderApplication
        fields = ["service_modes", "city", "state", "service_region", "service_radius_km"]
        widgets = {"service_radius_km": forms.NumberInput(attrs={"min": 1, "max": 200})}
        labels = {
            "city": "Cidade-base",
            "state": "Estado (UF)",
            "service_region": "Região de atendimento",
            "service_radius_km": "Raio aproximado (km)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial["service_modes"] = self.instance.service_modes or []
        self.fields["city"].required = True
        self.fields["state"].required = True

    def clean_state(self):
        value = self.cleaned_data["state"].strip().upper()
        if value not in STATE_CHOICES:
            raise ValidationError("Informe uma sigla de estado válida.")
        return value

    def clean_service_modes(self):
        modes = self.cleaned_data["service_modes"]
        if not modes:
            raise ValidationError("Selecione pelo menos uma modalidade.")
        return modes

    def clean(self):
        cleaned = super().clean()
        modes = cleaned.get("service_modes", [])
        if "HOME" in modes:
            if not cleaned.get("service_region"):
                self.add_error("service_region", "Informe a região principal de atendimento.")
            if not cleaned.get("service_radius_km"):
                self.add_error("service_radius_km", "Informe o raio aproximado de atendimento.")
        if "FIXED" in modes and not self.instance.fixed_point_postal_code:
            self.add_error(
                "service_modes",
                "Não é possível ativar ponto fixo sem cadastrar o endereço de atendimento.",
            )
        if "REMOTE" in modes and not self.instance.remote_scope:
            self.add_error(
                "service_modes",
                "Não é possível ativar atendimento remoto sem definir a região remota.",
            )
        return cleaned


class ProviderPortfolioUploadForm(forms.Form):
    image = forms.FileField(
        label="Fotografia do trabalho",
        widget=forms.ClearableFileInput(attrs={"accept": "image/jpeg,image/png,image/webp"}),
    )
    description = forms.CharField(label="Descrição (opcional)", max_length=180, required=False)

    def clean_image(self):
        upload = self.cleaned_data["image"]
        if upload.size > MAX_PUBLIC_IMAGE_BYTES:
            raise ValidationError("A imagem deve ter no máximo 5 MB.")
        try:
            upload.seek(0)
            image = Image.open(upload)
            if image.format not in {"JPEG", "PNG", "WEBP"}:
                raise ValidationError("Envie uma fotografia JPG, PNG ou WebP.")
            if image.width * image.height > MAX_PORTFOLIO_PIXELS:
                raise ValidationError("A resolução máxima é de 20 megapixels.")
            image.verify()
            upload.seek(0)
            with Image.open(upload) as source:
                normalized = ImageOps.exif_transpose(source).convert("RGB")
                normalized.thumbnail((2400, 2400))
                buffer = io.BytesIO()
                normalized.save(buffer, format="WEBP", quality=84, method=4)
            upload.seek(0)
            upload.normalized_content = ContentFile(buffer.getvalue(), name="portfolio.webp")
        except ValidationError:
            raise
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
            raise ValidationError("O arquivo está ilegível. Envie uma fotografia válida.") from None
        finally:
            upload.seek(0)
        return upload

    def save(self, *, provider):
        if provider.portfolio_images.count() >= MAX_PORTFOLIO_IMAGES:
            raise ValidationError(f"O portfólio aceita até {MAX_PORTFOLIO_IMAGES} imagens.")
        last_order = provider.portfolio_images.aggregate(value=Max("display_order"))["value"]
        image = ProviderPortfolioImage(
            provider=provider,
            description=self.cleaned_data["description"].strip(),
            display_order=(last_order if last_order is not None else -1) + 1,
        )
        normalized = self.cleaned_data["image"].normalized_content
        image.image.save(f"{image.pk}.webp", normalized, save=False)
        image.save()
        return image
