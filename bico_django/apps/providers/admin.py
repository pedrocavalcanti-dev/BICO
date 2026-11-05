from django.contrib import admin

from .models import ProviderProfile


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = (
        "public_name",
        "provider_type",
        "status",
        "city",
        "state",
        "is_featured",
        "is_demo",
    )
    list_filter = ("status", "provider_type", "is_featured", "is_demo", "state")
    search_fields = ("public_name", "slug", "city", "user__email")
    prepopulated_fields = {"slug": ("public_name",)}
    ordering = ("public_name",)
    readonly_fields = ("id", "is_demo", "approved_at", "created_at", "updated_at")
    autocomplete_fields = ("user",)
    filter_horizontal = ("categories",)
