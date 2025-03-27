from django.contrib import admin
from .models import RestaurantInfo, Dish, Rating, OrderItem, Order

@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    search_fields = ('name', 'address')

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'average_rating', 'sold_count', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish', 'rating')
    list_filter = ('rating',)
    search_fields = ('user__username', 'dish__name')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('dish', 'quantity', 'price')
    search_fields = ('dish__name',)

class OrderItemInline(admin.TabularInline):
    model = Order.items.through
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'total_price')
    list_filter = ('status',)
    search_fields = ('user__username',)
    inlines = [OrderItemInline]
    exclude = ('items',)