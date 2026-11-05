from apps.catalog.selectors import public_categories as active_categories
from apps.catalog.selectors import public_listings, search_public_listings
from apps.providers.models import ProviderProfile
from apps.providers.selectors import public_providers

from .models import HomeBanner

HOME_PROVIDER_LIMIT = 8
HOME_CATEGORY_LIMIT = 8
HOME_LISTING_LIMIT = 8


def search_listings(*, query="", category="", city=""):
    return search_public_listings(query=query, category=category, city=city)


def home_sections():
    banners = HomeBanner.objects.filter(is_active=True).order_by("display_order", "created_at")[:5]
    featured_categories = active_categories().filter(is_featured=True)[:HOME_CATEGORY_LIMIT]
    specialties = active_categories().filter(is_specialty=True)[:HOME_CATEGORY_LIMIT]
    popular_providers = (
        public_providers()
        .filter(
            is_featured=True,
            provider_type=ProviderProfile.ProviderType.INDIVIDUAL,
        )
        .order_by("-approved_at", "public_name")[:HOME_PROVIDER_LIMIT]
    )
    featured_listings = list(
        public_listings()
        .filter(is_featured=True)
        .order_by("-published_at", "-created_at", "id")[:HOME_LISTING_LIMIT]
    )
    featured_ids = [listing.pk for listing in featured_listings]
    other_listings = (
        public_listings()
        .exclude(pk__in=featured_ids)
        .order_by("-published_at", "-created_at", "id")[:HOME_LISTING_LIMIT]
    )
    companies = (
        public_providers()
        .filter(provider_type=ProviderProfile.ProviderType.COMPANY)
        .order_by("-approved_at", "public_name")[:HOME_PROVIDER_LIMIT]
    )
    recent_listings = public_listings().order_by("-published_at", "-created_at", "id")[
        :HOME_LISTING_LIMIT
    ]
    return {
        "banners": banners,
        "featured_categories": featured_categories,
        "specialties": specialties,
        "popular_providers": popular_providers,
        "popular_services": featured_listings,
        "other_services": other_listings,
        "service_companies": companies,
        "recent_listings": recent_listings,
    }
