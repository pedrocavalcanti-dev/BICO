from django.urls import path

from . import views

app_name = "providers"

urlpatterns = [
    path("prestador/", views.onboarding_start, name="start"),
    path("prestador/cadastro/<int:step>/", views.onboarding_step, name="onboarding-step"),
    path("prestador/solicitacao/", views.application_status, name="application-status"),
    path("prestador/painel/", views.dashboard, name="dashboard"),
    path("prestador/servicos/", views.managed_listings, name="managed-listings"),
    path("prestador/perfil/", views.managed_profile, name="profile-edit"),
    path("prestador/perfil/previa/", views.profile_preview, name="profile-preview"),
    path("prestador/portfolio/", views.portfolio, name="portfolio"),
    path(
        "prestador/portfolio/<uuid:image_id>/mover/<str:direction>/",
        views.portfolio_reorder,
        name="portfolio-reorder",
    ),
    path(
        "prestador/portfolio/<uuid:image_id>/imagem/", views.portfolio_image, name="portfolio-image"
    ),
    path(
        "prestador/portfolio/<uuid:image_id>/remover/",
        views.portfolio_delete,
        name="portfolio-delete",
    ),
    path("prestador/atendimento/", views.managed_service_area, name="service-area"),
    path("prestador/configuracoes/", views.professional_settings, name="professional-settings"),
    path(
        "prestador/documentos/<str:side>/imagem/",
        views.identity_document_image,
        name="document-image",
    ),
]
