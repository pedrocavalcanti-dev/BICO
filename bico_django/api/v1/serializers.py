from apps.catalog.models import ServiceCategory, ServiceListing
from apps.core.models import HomeBanner
from apps.providers.models import ProviderProfile
from rest_framework import serializers


class PublicCategorySerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(read_only=True)

    class Meta:
        model = ServiceCategory
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "cover_image",
            "display_order",
            "is_featured",
            "is_specialty",
        )


class PublicProviderCompactSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = ProviderProfile
        fields = (
            "id",
            "public_name",
            "slug",
            "provider_type",
            "avatar",
            "city",
            "state",
            "is_demo",
        )


class PublicProviderSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)
    categories = PublicCategorySerializer(many=True, read_only=True)

    class Meta:
        model = ProviderProfile
        fields = (
            "id",
            "public_name",
            "slug",
            "provider_type",
            "description",
            "avatar",
            "city",
            "state",
            "categories",
            "is_demo",
        )


class PublicListingSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    category = PublicCategorySerializer(read_only=True)
    provider = PublicProviderCompactSerializer(read_only=True)

    class Meta:
        model = ServiceListing
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "image",
            "price_start",
            "price_type",
            "city",
            "state",
            "category",
            "provider",
            "is_demo",
            "published_at",
        )


class PublicBannerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    mobile_image = serializers.ImageField(read_only=True)

    class Meta:
        model = HomeBanner
        fields = (
            "id",
            "title",
            "subtitle",
            "image",
            "mobile_image",
            "image_alt",
            "action_label",
            "destination",
            "display_order",
            "is_demo",
        )
