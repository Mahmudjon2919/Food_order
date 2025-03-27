from rest_framework import serializers
from .models import RestaurantInfo, Dish, Order, Rating

# Restaurant Information Serializer
class RestaurantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantInfo
        fields = ["id", "name", "description", "address", "phone", "working_hours", "telegram", "facebook", "instagram"]

# Dish Serializer
class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ["id", "name", "price", "discount", "average_rating", "is_active", "sold_count"]

# Order Status Serializer
class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "status"]

# Rating Serializer
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["dish", "rating"]

    def validate(self, data):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Request context is required for validation.")
        user = request.user

        if user.is_superuser or user.is_staff:
            raise serializers.ValidationError({"user": "Administrators and superusers cannot rate dishes."})

        dish = data.get("dish")
        if not dish.is_active:
            raise serializers.ValidationError({"dish": "This dish is no longer available for rating."})

        if Rating.objects.filter(user=user, dish=dish).exists():
            raise serializers.ValidationError({"dish": "You have already rated this dish."})

        return data
