from django.contrib import admin

from .models import ServiceCategory, ServiceListing, ServiceListingImage


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "is_featured", "is_specialty", "display_order")
    list_filter = ("is_active", "is_featured", "is_specialty")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("display_order", "name")
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(ServiceListing)
class ServiceListingAdmin(admin.ModelAdmin):
    class GalleryImageInline(admin.TabularInline):
        model = ServiceListingImage
        extra = 0
        fields = ("image", "alt_text", "display_order")

    list_display = (
        "title",
        "provider",
        "category",
        "status",
        "is_featured",
        "is_demo",
        "published_at",
    )
    list_filter = ("status", "category", "is_featured", "is_demo", "state")
    search_fields = ("title", "description", "provider__public_name", "city")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at", "-created_at")
    readonly_fields = ("id", "is_demo", "created_at", "updated_at", "published_at")
    autocomplete_fields = ("provider", "category")
    inlines = (GalleryImageInline,)
