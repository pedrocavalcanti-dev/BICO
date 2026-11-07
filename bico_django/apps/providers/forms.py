import re

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.catalog.models import ServiceCategory

from .document_validation import validate_document_file
from .models import ProviderApplication

STATE_CHOICES = (
    "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split()
)
PHONE_PATTERN = re.compile(r"^\d{10,11}$")


def _valid_cpf(value):
    digits = re.sub(r"\D", "", value or "")
    if len(digits) != 11 or len(set(digits)) == 1:
        return False
    for position in (9, 10):
        checksum = sum(int(digits[index]) * (position + 1 - index) for index in range(position))
        digit = (checksum * 10) % 11
        if digit == 10:
            digit = 0
        if digit != int(digits[position]):
            return False
    return True


def _valid_cnpj(value):
    digits = re.sub(r"\D", "", value or "")
    if len(digits) != 14 or len(set(digits)) == 1:
        return False
    for position, weights in (
        (12, (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)),
        (13, (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)),
    ):
        remainder = sum(int(digits[index]) * weight for index, weight in enumerate(weights)) % 11
        digit = 0 if remainder < 2 else 11 - remainder
        if digit != int(digits[position]):
            return False
    return True


class ProviderApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "provider-field")
        for name, field in self.fields.items():
            if name in {"phone", "company_phone", "representative_phone"}:
                field.widget.attrs.update(
                    {"inputmode": "tel", "autocomplete": "tel", "placeholder": "(19) 99999-9999"}
                )
            elif name in {"legal_name", "representative_name"}:
                field.widget.attrs["autocomplete"] = "name"


class ProviderTypeForm(ProviderApplicationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["provider_type"].required = True
        self.fields["provider_type"].choices = ProviderApplication.ProviderType.choices

    class Meta:
        model = ProviderApplication
        fields = ["provider_type"]
        widgets = {"provider_type": forms.RadioSelect}


class ProviderIdentityForm(ProviderApplicationForm):
    class Meta:
        model = ProviderApplication
        fields = [
            "legal_name",
            "cpf",
            "birth_date",
            "phone",
            "document_type",
            "identity_document_number",
            "issuing_authority",
            "issuer_state",
            "company_legal_name",
            "company_trade_name",
            "cnpj",
            "company_email",
            "company_phone",
            "representative_name",
            "representative_cpf",
            "representative_phone",
            "representative_role",
        ]

    def __init__(self, *args, provider_type, **kwargs):
        self.provider_type = provider_type
        super().__init__(*args, **kwargs)
        if provider_type == ProviderApplication.ProviderType.INDIVIDUAL:
            names = [
                "legal_name",
                "cpf",
                "birth_date",
                "phone",
                "document_type",
                "identity_document_number",
                "issuing_authority",
                "issuer_state",
            ]
        else:
            names = [
                "company_legal_name",
                "company_trade_name",
                "cnpj",
                "company_email",
                "company_phone",
                "representative_name",
                "representative_cpf",
                "representative_phone",
                "representative_role",
                "document_type",
                "identity_document_number",
                "issuing_authority",
                "issuer_state",
            ]
        labels = {
            "legal_name": "Nome completo",
            "cpf": "CPF",
            "birth_date": "Data de nascimento",
            "phone": "Celular com DDD",
            "document_type": "Documento que será fotografado",
            "identity_document_number": "Número do documento (opcional)",
            "issuing_authority": "Órgão emissor (opcional)",
            "issuer_state": "UF emissora (opcional)",
            "company_legal_name": "Razão social",
            "company_trade_name": "Nome fantasia (opcional)",
            "cnpj": "CNPJ",
            "company_email": "E-mail comercial",
            "company_phone": "Telefone comercial",
            "representative_name": "Nome do responsável",
            "representative_cpf": "CPF do responsável",
            "representative_phone": "Telefone do responsável",
            "representative_role": "Função na empresa",
        }
        self.fields = {name: self.fields[name] for name in names}
        for name, field in self.fields.items():
            field.label = labels[name]
            field.required = name not in {
                "company_trade_name",
                "identity_document_number",
                "issuing_authority",
                "issuer_state",
            }
            if name in {"cpf", "representative_cpf", "cnpj"}:
                field.widget.attrs["inputmode"] = "numeric"
        for name, max_length, placeholder in (
            ("cpf", 14, "000.000.000-00"),
            ("representative_cpf", 14, "000.000.000-00"),
            ("cnpj", 18, "00.000.000/0000-00"),
        ):
            if name in self.fields:
                self.fields[name] = forms.CharField(
                    label=labels[name],
                    required=True,
                    max_length=max_length,
                    widget=forms.TextInput(
                        attrs={
                            "class": "provider-field",
                            "inputmode": "numeric",
                            "maxlength": max_length,
                            "placeholder": placeholder,
                        }
                    ),
                )
        if "birth_date" in self.fields:
            self.fields["birth_date"].widget = forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date", "class": "provider-field"}
            )
        self.fields["document_type"].label = "Tipo de documento"
        self.fields["document_type"].choices = [
            ("", "Selecione"),
            *ProviderApplication.DocumentType.choices,
        ]

    def clean(self):
        cleaned = super().clean()
        cpf_field = (
            "cpf"
            if self.provider_type == ProviderApplication.ProviderType.INDIVIDUAL
            else "representative_cpf"
        )
        cpf = cleaned.get(cpf_field)
        if cpf and not _valid_cpf(cpf):
            self.add_error(cpf_field, "Confira os números do CPF informado.")
        elif cpf:
            cleaned[cpf_field] = re.sub(r"\D", "", cpf)
        if self.provider_type == ProviderApplication.ProviderType.COMPANY:
            cnpj = cleaned.get("cnpj")
            if cnpj and not _valid_cnpj(cnpj):
                self.add_error("cnpj", "Confira os números do CNPJ informado.")
            elif cnpj:
                cleaned["cnpj"] = re.sub(r"\D", "", cnpj)
        for name in ("phone", "company_phone", "representative_phone"):
            value = cleaned.get(name)
            if value:
                digits = re.sub(r"\D", "", value)
                if not PHONE_PATTERN.fullmatch(digits):
                    self.add_error(name, "Informe um telefone brasileiro com DDD.")
                else:
                    cleaned[name] = digits
        if cleaned.get("issuer_state") and cleaned["issuer_state"].upper() not in STATE_CHOICES:
            self.add_error("issuer_state", "Informe uma sigla de estado válida.")
        if cleaned.get("issuer_state"):
            cleaned["issuer_state"] = cleaned["issuer_state"].upper()
        return cleaned


class ProviderProfileForm(ProviderApplicationForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=ServiceCategory.objects.filter(is_active=True, is_specialty=True),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label="Especialidades",
    )

    class Meta:
        model = ProviderApplication
        fields = [
            "public_name",
            "professional_description",
            "experience_years",
            "main_category",
            "categories",
        ]
        widgets = {
            "professional_description": forms.Textarea(attrs={"rows": 4, "maxlength": 2000}),
            "experience_years": forms.NumberInput(attrs={"min": 0, "max": 80}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            "public_name": "Como os clientes vão chamar você?",
            "professional_description": "Conte um pouco sobre o seu trabalho",
            "experience_years": "Anos de experiência (opcional)",
            "main_category": "Sua especialidade principal",
        }
        for name, label in labels.items():
            self.fields[name].label = label
        for name in ("public_name", "professional_description", "main_category"):
            self.fields[name].required = True
        self.fields["main_category"].queryset = self.fields["categories"].queryset
        self.fields["public_name"].widget.attrs["placeholder"] = "Seu nome profissional ou empresa"
        self.fields["professional_description"].widget.attrs.update(
            {"placeholder": "O que você faz e o que torna seu atendimento especial?", "rows": 3}
        )

    def clean(self):
        cleaned = super().clean()
        categories = cleaned.get("categories")
        main_category = cleaned.get("main_category")
        if categories and main_category and main_category not in categories:
            self.add_error("main_category", "A especialidade principal precisa estar selecionada.")
        if categories and len(categories) > settings.PROVIDER_MAX_CATEGORIES:
            self.add_error(
                "categories",
                f"Selecione no máximo {settings.PROVIDER_MAX_CATEGORIES} especialidades.",
            )
        return cleaned


SERVICE_MODE_CHOICES = (
    ("HOME", "Atendimento a domicílio"),
    ("FIXED", "Atendimento em ponto fixo"),
    ("REMOTE", "Atendimento remoto"),
)


class ProviderServiceAreaForm(ProviderApplicationForm):
    service_modes = forms.MultipleChoiceField(
        choices=SERVICE_MODE_CHOICES,
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label="Como você atende?",
    )

    class Meta:
        model = ProviderApplication
        fields = [
            "service_modes",
            "city",
            "state",
            "service_region",
            "service_radius_km",
            "remote_scope",
            "fixed_point_name",
            "fixed_point_postal_code",
            "fixed_point_street",
            "fixed_point_number",
            "fixed_point_complement",
            "fixed_point_neighborhood",
            "fixed_point_city",
            "fixed_point_state",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            "city": "Cidade-base",
            "state": "Estado",
            "service_region": "Região de atuação",
            "service_radius_km": "Até onde você vai?",
            "fixed_point_name": "Nome do ponto de atendimento (opcional)",
            "fixed_point_postal_code": "CEP",
            "fixed_point_street": "Rua ou avenida",
            "fixed_point_number": "Número",
            "fixed_point_complement": "Complemento (opcional)",
            "fixed_point_neighborhood": "Bairro",
        }
        for name, label in labels.items():
            self.fields[name].label = label
        self.fields["city"].required = True
        self.fields["state"].required = True
        self.fields["fixed_point_postal_code"].widget.attrs.update(
            {"inputmode": "numeric", "autocomplete": "postal-code", "placeholder": "00000-000"}
        )
        self.fields["fixed_point_street"].widget.attrs["autocomplete"] = "address-line1"
        self.fields["city"].widget.attrs["autocomplete"] = "address-level2"
        self.fields["service_region"].widget.attrs["placeholder"] = (
            "Ex.: Campinas e cidades próximas"
        )
        self.fields["service_radius_km"].widget = forms.NumberInput(
            attrs={"class": "provider-field", "type": "range", "min": 1, "max": 200, "step": 1}
        )
        if not self.initial.get("service_radius_km"):
            self.initial["service_radius_km"] = 20
        self.fields["state"].widget.attrs["maxlength"] = 2
        self.fields["fixed_point_state"].widget.attrs["maxlength"] = 2
        self.fields["state"].widget = forms.Select(
            choices=[("", "Selecione")] + [(state, state) for state in STATE_CHOICES],
            attrs={"class": "provider-field", "autocomplete": "address-level1"},
        )
        self.fields["remote_scope"] = forms.ChoiceField(
            choices=[("BRAZIL", "Todo o Brasil"), ("REGIONS", "Regiões selecionadas")],
            required=False,
            label="Região do atendimento remoto",
            widget=forms.Select(attrs={"class": "provider-field"}),
        )
        if self.instance and self.instance.pk:
            self.initial["service_modes"] = self.instance.service_modes

    def clean_state(self):
        value = self.cleaned_data["state"].upper()
        if value and value not in STATE_CHOICES:
            raise ValidationError("Informe uma sigla de estado válida.")
        return value

    def clean_fixed_point_state(self):
        value = self.cleaned_data["fixed_point_state"].upper()
        if value and value not in STATE_CHOICES:
            raise ValidationError("Informe uma sigla de estado válida.")
        return value

    def clean_fixed_point_postal_code(self):
        value = self.cleaned_data["fixed_point_postal_code"]
        if not value:
            return ""
        digits = re.sub(r"\D", "", value)
        if len(digits) != 8:
            raise ValidationError("Informe os 8 números do CEP.")
        return f"{digits[:5]}-{digits[5:]}"

    def clean(self):
        cleaned = super().clean()
        modes = cleaned.get("service_modes", [])
        # One city/state input in the wizard; preserve the existing API's fixed-point fields.
        cleaned["fixed_point_city"] = cleaned.get("fixed_point_city") or cleaned.get("city", "")
        cleaned["fixed_point_state"] = cleaned.get("fixed_point_state") or cleaned.get("state", "")
        if not cleaned.get("city") or not cleaned.get("state"):
            self.add_error("city", "Informe sua cidade-base e estado.")
        if "HOME" in modes:
            if not cleaned.get("service_region"):
                self.add_error("service_region", "Informe a região principal de atendimento.")
            if not cleaned.get("service_radius_km"):
                self.add_error("service_radius_km", "Informe um raio aproximado de atendimento.")
        if "FIXED" in modes:
            cleaned["fixed_point_name"] = (
                cleaned.get("fixed_point_name") or self.instance.public_name
            )
            required = (
                "fixed_point_name",
                "fixed_point_postal_code",
                "fixed_point_street",
                "fixed_point_number",
                "fixed_point_neighborhood",
                "fixed_point_city",
                "fixed_point_state",
            )
            for name in required:
                if not cleaned.get(name):
                    self.add_error(name, "Preencha este campo para cadastrar o ponto fixo.")
        if "REMOTE" in modes and not cleaned.get("remote_scope"):
            self.add_error("remote_scope", "Escolha a região do atendimento remoto.")
        return cleaned


class ProviderDocumentsForm(forms.Form):
    front_image = forms.FileField(
        required=False,
        label="Frente do documento",
        widget=forms.ClearableFileInput(attrs={"accept": "image/jpeg,image/png,image/webp"}),
    )
    back_image = forms.FileField(
        required=False,
        label="Verso do documento",
        widget=forms.ClearableFileInput(attrs={"accept": "image/jpeg,image/png,image/webp"}),
    )

    def __init__(self, *args, application, submit=False, **kwargs):
        self.application = application
        self.submit = submit
        super().__init__(*args, **kwargs)

    def clean_front_image(self):
        upload = self.cleaned_data.get("front_image")
        if upload:
            validate_document_file(upload)
        return upload

    def clean_back_image(self):
        upload = self.cleaned_data.get("back_image")
        if upload:
            validate_document_file(upload)
        return upload

    def clean(self):
        cleaned = super().clean()
        if self.submit:
            documents = {
                ProviderDocumentSide.FRONT: cleaned.get("front_image"),
                ProviderDocumentSide.BACK: cleaned.get("back_image"),
            }
            for side, upload in documents.items():
                exists = self.application.identity_documents.filter(
                    side=side, prevalidation_passed=True
                ).exists()
                if not upload and not exists:
                    self.add_error(
                        "front_image" if side == ProviderDocumentSide.FRONT else "back_image",
                        "Envie as duas fotos do documento antes de enviar sua solicitação.",
                    )
        return cleaned


class ProviderDocumentSide:
    FRONT = "FRONT"
    BACK = "BACK"


class ProviderReviewForm(ProviderDocumentsForm):
    acknowledged = forms.BooleanField(
        label=(
            "Conferi minhas informações e entendo que o envio não libera a publicação "
            "de serviços. Meu cadastro depende de análise e aprovação."
        ),
        error_messages={"required": "Confirme que conferiu as informações antes de enviar."},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["acknowledged"].required = self.submit
