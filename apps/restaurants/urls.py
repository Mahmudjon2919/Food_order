from django.urls import path
from .views import (
    RestaurantInfoView, RestaurantMenuView, DishDetailView,
    OrderStatusView, RateDishView
)

urlpatterns = [
    path("api/restaurants/info/", RestaurantInfoView.as_view(), name="restaurant-info"),
    path("api/restaurants/menu/", RestaurantMenuView.as_view(), name="restaurant-menu"),
    path("api/dishes/<int:id>/", DishDetailView.as_view(), name="dish-detail"),
    path("api/orders/<int:id>/status/", OrderStatusView.as_view(), name="order-status"),
    path("api/dishes/<int:id>/rate/", RateDishView.as_view(), name="rate-dish"),
]
