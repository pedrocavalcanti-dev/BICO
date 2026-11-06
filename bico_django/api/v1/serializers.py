from apps.catalog.models import ServiceCategory, ServiceListing, ServiceListingImage
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
    gallery_images = serializers.SerializerMethodField()

    def get_gallery_images(self, obj):
        return PublicListingImageSerializer(
            obj.gallery_images.all(), many=True, context=self.context
        ).data

    class Meta:
        model = ServiceListing
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "image",
            "gallery_images",
            "price_start",
            "price_type",
            "city",
            "state",
            "category",
            "provider",
            "is_demo",
            "published_at",
        )


class PublicListingImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = ServiceListingImage
        fields = ("image", "alt_text", "display_order")


class PublicProviderDetailSerializer(PublicProviderSerializer):
    listings = serializers.SerializerMethodField()

    def get_listings(self, obj):
        from apps.catalog.selectors import public_listings

        listings = public_listings().filter(provider=obj).order_by("-published_at")[:12]
        return PublicListingSerializer(listings, many=True, context=self.context).data

    class Meta(PublicProviderSerializer.Meta):
        fields = (*PublicProviderSerializer.Meta.fields, "listings")


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
