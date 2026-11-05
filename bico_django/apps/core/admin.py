from django.contrib import admin

from .models import HomeBanner


@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "is_demo", "display_order", "updated_at")
    list_filter = ("is_active", "is_demo")
    search_fields = ("title", "subtitle", "slug")
    ordering = ("display_order", "created_at")
    readonly_fields = ("id", "is_demo", "created_at", "updated_at")
    fieldsets = (
        ("Conteúdo", {"fields": ("title", "subtitle", "image", "mobile_image", "image_alt")}),
        ("Ação", {"fields": ("action_label", "destination")}),
        ("Publicação", {"fields": ("slug", "display_order", "is_active", "is_demo")}),
        ("Datas", {"fields": ("id", "created_at", "updated_at")}),
    )
