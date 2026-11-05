from django.db.models import Prefetch, Q

from apps.catalog.models import ServiceCategory

from .models import ProviderProfile


def public_providers():
    return (
        ProviderProfile.objects.filter(status=ProviderProfile.Status.APPROVED)
        .select_related("user")
        .prefetch_related(
            Prefetch("categories", queryset=ServiceCategory.objects.filter(is_active=True))
        )
    )


def search_public_providers(*, query="", category="", city="", provider_type=""):
    providers = public_providers()
    if query:
        providers = providers.filter(
            Q(public_name__icontains=query)
            | Q(description__icontains=query)
            | Q(categories__name__icontains=query)
        )
    if category:
        providers = providers.filter(categories__slug=category)
    if city:
        providers = providers.filter(city__icontains=city)
    if provider_type:
        providers = providers.filter(provider_type=provider_type)
    return providers.distinct().order_by("public_name", "id")
