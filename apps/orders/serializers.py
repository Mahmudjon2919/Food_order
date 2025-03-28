from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["dish", "quantity", "subtotal"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "total_price", "items", "created_at"]
        read_only_fields = ["user", "total_price", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(user=self.context["request"].user)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        order.update_total_price()
        return order
