from apps.accounts.api_views import UserMeAPIView
from django.urls import path

from .views import (
    ApiRootView,
    CategoryListAPIView,
    HealthView,
    HomeAPIView,
    ListingDetailAPIView,
    ListingListAPIView,
    ProviderDetailAPIView,
    ProviderListAPIView,
)

app_name = "api_v1"

urlpatterns = [
    path("", ApiRootView.as_view(), name="root"),
    path("health/", HealthView.as_view(), name="health"),
    path("users/me/", UserMeAPIView.as_view(), name="user-me"),
    path("home/", HomeAPIView.as_view(), name="home"),
    path("categories/", CategoryListAPIView.as_view(), name="categories"),
    path("providers/", ProviderListAPIView.as_view(), name="providers"),
    path("providers/<uuid:provider_id>/", ProviderDetailAPIView.as_view(), name="provider-detail"),
    path("listings/", ListingListAPIView.as_view(), name="listings"),
    path("listings/<uuid:listing_id>/", ListingDetailAPIView.as_view(), name="listing-detail"),
]
