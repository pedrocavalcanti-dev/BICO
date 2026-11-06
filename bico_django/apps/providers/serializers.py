from rest_framework import serializers

from .models import ProviderApplication


class ProviderApplicationSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = ProviderApplication
        fields = [
            "id",
            "status",
            "status_label",
            "current_step",
            "provider_type",
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
            "public_name",
            "professional_description",
            "experience_years",
            "main_category",
            "categories",
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
            "fixed_point_public",
            "submitted_at",
        ]
        read_only_fields = fields
