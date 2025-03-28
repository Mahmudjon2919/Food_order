from django.contrib import admin
from django.utils.html import format_html
from .models import RestaurantInfo, Dish, Rating

@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "working_hours", "get_social_links")
    search_fields = ("name", "address", "phone")
    list_filter = ("working_hours",)

    def get_social_links(self, obj):
        links = []
        if obj.telegram:
            links.append(f'<a href="{obj.telegram}" target="_blank">Telegram</a>')
        if obj.facebook:
            links.append(f'<a href="{obj.facebook}" target="_blank">Facebook</a>')
        if obj.instagram:
            links.append(f'<a href="{obj.instagram}" target="_blank">Instagram</a>')
        return format_html(" | ".join(links)) if links else "No Links"

    get_social_links.short_description = "Social Links"

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discount", "average_rating", "sold_count", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active", "price")
    ordering = ("-sold_count",)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "dish", "rating")
    search_fields = ("user__username", "dish__name")
    list_filter = ("rating",)
