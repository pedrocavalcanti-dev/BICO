from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from apps.audit.models import AuditEvent
from apps.catalog.models import ServiceListing

from .models import ProviderApplication, ProviderPortfolioImage

RECENT_PROVIDER_ACTIONS = {
    "account.profile.updated": "Informações da conta atualizadas",
    "provider.application.submitted": "Cadastro profissional enviado para análise",
    "provider.document.uploaded": "Documento enviado para análise",
    "provider.dashboard.profile_updated": "Perfil profissional atualizado",
    "provider.dashboard.area_updated": "Região de atendimento atualizada",
    "provider.dashboard.portfolio_added": "Imagem adicionada ao portfólio privado",
    "provider.dashboard.portfolio_removed": "Imagem removida do portfólio privado",
}


def provider_dashboard_context(provider):
    listings = ServiceListing.objects.filter(provider=provider)
    listing_counts = {
        row["status"]: row["total"] for row in listings.values("status").annotate(total=Count("id"))
    }
    application = ProviderApplication.objects.filter(user=provider.user).first()
    missing_profile_items = []
    if not provider.avatar:
        missing_profile_items.append(("Adicionar foto profissional", "providers:profile-edit"))
    if not provider.description.strip():
        missing_profile_items.append(("Completar apresentação", "providers:profile-edit"))
    if not provider.categories.exists():
        missing_profile_items.append(("Selecionar especialidades", "providers:profile-edit"))
    if not provider.portfolio_images.exists():
        missing_profile_items.append(("Adicionar fotos de trabalhos", "providers:portfolio"))
    if application and not application.service_modes:
        missing_profile_items.append(
            ("Configurar modalidades de atendimento", "providers:service-area")
        )

    action_names = tuple(RECENT_PROVIDER_ACTIONS)
    activities = [
        {
            "label": RECENT_PROVIDER_ACTIONS[event.action],
            "created_at": event.created_at,
        }
        for event in AuditEvent.objects.filter(
            actor=provider.user,
            action__in=action_names,
            outcome=AuditEvent.Outcome.SUCCESS,
            created_at__gte=timezone.now() - timedelta(days=90),
        )[:6]
    ]
    return {
        "provider": provider,
        "listing_counts": listing_counts,
        "published_count": listing_counts.get(ServiceListing.Status.PUBLISHED, 0),
        "draft_count": listing_counts.get(ServiceListing.Status.DRAFT, 0),
        "paused_count": listing_counts.get(ServiceListing.Status.PAUSED, 0),
        "featured_listings": listings.filter(
            status=ServiceListing.Status.PUBLISHED,
            category__is_active=True,
        )
        .select_related("category")
        .order_by("-published_at", "-created_at")[:3],
        "recent_activities": activities,
        "profile_tasks": missing_profile_items,
        "portfolio_count": ProviderPortfolioImage.objects.filter(provider=provider).count(),
        "views_available": False,
    }


def provider_listing_queryset(provider, *, status="", query=""):
    listings = ServiceListing.objects.filter(provider=provider).select_related("category")
    valid_statuses = {value for value, _label in ServiceListing.Status.choices}
    if status in valid_statuses:
        listings = listings.filter(status=status)
    if query:
        listings = listings.filter(title__icontains=query)
    return listings.order_by("-updated_at", "-created_at")
