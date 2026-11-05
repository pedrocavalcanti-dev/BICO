from django.urls import path

from .views import home, info_page, listing_detail, provider_detail, search

app_name = "core"

urlpatterns = [
    path("", home, name="home"),
    path("servicos/", search, name="search"),
    path("servicos/<slug:slug>/", listing_detail, name="service-detail"),
    path("profissionais/<slug:slug>/", provider_detail, name="provider-detail"),
    path("informacoes/<slug:slug>/", info_page, name="info"),
]
