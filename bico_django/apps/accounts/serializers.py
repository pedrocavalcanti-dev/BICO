from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "created_at")
        read_only_fields = ("email", "created_at")

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Informe seu nome.")
        return value
