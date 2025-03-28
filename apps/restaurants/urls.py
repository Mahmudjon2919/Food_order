from django.urls import path
from .views import (
    RestaurantInfoView, RestaurantMenuView, DishDetailView, RateDishView
)

urlpatterns = [
    path("restaurant/info/", RestaurantInfoView.as_view(), name="restaurant-info"),
    path("restaurant/menu/", RestaurantMenuView.as_view(), name="restaurant-menu"),
    path("restaurant/dishes/<int:id>/", DishDetailView.as_view(), name="dish-detail"),
    path("restaurant/dishes/<int:id>/rate/", RateDishView.as_view(), name="rate-dish"),
]
