import re

from apps.catalog.selectors import public_categories, search_public_listings
from apps.core.selectors import home_sections
from apps.providers.models import ProviderProfile
from apps.providers.selectors import public_providers, search_public_providers
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    PublicBannerSerializer,
    PublicCategorySerializer,
    PublicListingSerializer,
    PublicProviderSerializer,
)


class PublicReadOnlyMixin:
    http_method_names = ["get", "head"]


class ApiRootView(PublicReadOnlyMixin, APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"name": "BICO API", "version": "v1"})


class HealthView(PublicReadOnlyMixin, APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class PublicPagePagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = "page_size"
    max_page_size = 48


def _query_parameter(request, name, *, max_length=100):
    value = request.query_params.get(name, "").strip()
    if len(value) > max_length:
        raise ValidationError({name: f"Use até {max_length} caracteres."})
    return value


def _category_parameter(request):
    category = _query_parameter(request, "category", max_length=150).lower()
    if category and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", category):
        raise ValidationError({"category": "Informe uma categoria válida."})
    return category


class HomeAPIView(PublicReadOnlyMixin, APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        sections = home_sections()
        context = {"request": request}
        return Response(
            {
                "banners": PublicBannerSerializer(
                    sections["banners"], many=True, context=context
                ).data,
                "popular_providers": PublicProviderSerializer(
                    sections["popular_providers"], many=True, context=context
                ).data,
                "featured_categories": PublicCategorySerializer(
                    sections["featured_categories"], many=True, context=context
                ).data,
                "popular_services": PublicListingSerializer(
                    sections["popular_services"], many=True, context=context
                ).data,
                "service_companies": PublicProviderSerializer(
                    sections["service_companies"], many=True, context=context
                ).data,
                "recent_listings": PublicListingSerializer(
                    sections["recent_listings"], many=True, context=context
                ).data,
            }
        )


class CategoryListAPIView(PublicReadOnlyMixin, generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = PublicCategorySerializer
    pagination_class = PublicPagePagination

    def get_queryset(self):
        categories = public_categories()
        featured = self.request.query_params.get("featured", "").lower()
        if featured in {"1", "true"}:
            categories = categories.filter(is_featured=True)
        elif featured not in {"", "0", "false"}:
            raise ValidationError({"featured": "Use true ou false."})
        return categories


class ProviderListAPIView(PublicReadOnlyMixin, generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = PublicProviderSerializer
    pagination_class = PublicPagePagination

    def get_queryset(self):
        query = _query_parameter(self.request, "q")
        city = _query_parameter(self.request, "city")
        category = _category_parameter(self.request)
        provider_type = _query_parameter(self.request, "type", max_length=10).upper()
        valid_types = {choice for choice, _label in ProviderProfile.ProviderType.choices}
        if provider_type and provider_type not in valid_types:
            raise ValidationError({"type": "Use INDIVIDUAL ou COMPANY."})
        return search_public_providers(
            query=query, category=category, city=city, provider_type=provider_type
        )


class ProviderDetailAPIView(PublicReadOnlyMixin, generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = PublicProviderSerializer
    lookup_field = "id"
    lookup_url_kwarg = "provider_id"

    def get_queryset(self):
        return public_providers()


class ListingListAPIView(PublicReadOnlyMixin, generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = PublicListingSerializer
    pagination_class = PublicPagePagination

    def get_queryset(self):
        return search_public_listings(
            query=_query_parameter(self.request, "q"),
            category=_category_parameter(self.request),
            city=_query_parameter(self.request, "city"),
        )


class ListingDetailAPIView(PublicReadOnlyMixin, generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = PublicListingSerializer
    lookup_field = "id"
    lookup_url_kwarg = "listing_id"

    def get_queryset(self):
        return search_public_listings()
