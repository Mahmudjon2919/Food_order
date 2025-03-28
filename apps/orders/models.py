from django.conf import settings
from django.db import models
from django.db.models import Sum

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_total_price(self):
        self.total_price = self.items.aggregate(total=Sum('subtotal'))['total'] or 0.00
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.total_price} UZS"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    dish = models.ForeignKey("restaurants.Dish", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return (self.dish.price - self.dish.discount) * self.quantity

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_total_price()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.order.update_total_price()
