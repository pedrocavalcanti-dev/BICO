from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from .models import ServiceCategory, ServiceListing, ServiceListingImage


class ServiceListingGalleryFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        listing = self.instance
        if listing.status != ServiceListing.Status.PUBLISHED:
            return

        if not listing._state.adding:
            current_status = (
                ServiceListing.objects.filter(pk=listing.pk)
                .values_list("status", flat=True)
                .first()
            )
            if current_status == ServiceListing.Status.PUBLISHED:
                return

        gallery_images = []
        for form in self.forms:
            cleaned_data = getattr(form, "cleaned_data", {}) or {}
            if cleaned_data.get("DELETE"):
                continue
            image = cleaned_data.get("image") or form.instance.image
            if image:
                gallery_images.append(image)
        if not listing.has_minimum_publication_images(gallery_images):
            raise ValidationError(
                "Um anúncio precisa de duas imagens distintas para ser publicado."
            )


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
        formset = ServiceListingGalleryFormSet
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
