from django.urls import path

from . import views

app_name = "providers"

urlpatterns = [
    path("prestador/", views.onboarding_start, name="start"),
    path("prestador/cadastro/<int:step>/", views.onboarding_step, name="onboarding-step"),
    path("prestador/solicitacao/", views.application_status, name="application-status"),
    path(
        "prestador/documentos/<str:side>/imagem/",
        views.identity_document_image,
        name="document-image",
    ),
]
