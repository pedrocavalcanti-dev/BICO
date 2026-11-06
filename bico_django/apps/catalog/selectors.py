from django.db.models import Q

from apps.providers.models import ProviderProfile

from .models import ServiceCategory, ServiceListing


def public_listings():
    return (
        ServiceListing.objects.filter(
            status=ServiceListing.Status.PUBLISHED,
            provider__status=ProviderProfile.Status.APPROVED,
            category__is_active=True,
        )
        .select_related("provider", "category", "provider__user")
        .prefetch_related("gallery_images")
    )


def search_public_listings(*, query="", category="", city=""):
    listings = public_listings()
    if query:
        listings = listings.filter(
            Q(title__icontains=query)
            | Q(category__name__icontains=query)
            | Q(provider__public_name__icontains=query)
        )
    if category:
        listings = listings.filter(category__slug=category)
    if city:
        listings = listings.filter(city__icontains=city)
    return listings.order_by("-published_at", "-created_at", "id")


def public_categories():
    return ServiceCategory.objects.filter(is_active=True).order_by("display_order", "name")


def header_categories(*, limit=7):
    return public_categories().filter(is_featured=True)[:limit]
