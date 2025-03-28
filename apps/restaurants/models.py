from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.humanize.templatetags.humanize import intcomma

User = get_user_model()


class RestaurantInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name="Restaurant Name")
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="Address")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    working_hours = models.CharField(max_length=255, default="10:00 - 22:00", verbose_name="Working Hours")
    telegram = models.URLField(blank=True, null=True, verbose_name="Telegram Link")
    facebook = models.URLField(blank=True, null=True, verbose_name="Facebook Link")
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram Link")

    class Meta:
        verbose_name = "Restaurant Information"
        verbose_name_plural = "Restaurant Informations"

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255, verbose_name="Dish Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Discount")
    average_rating = models.FloatField(default=0.0, editable=False, verbose_name="Average Rating")
    sold_count = models.PositiveIntegerField(default=0, editable=False, verbose_name="Sold Count")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def get_price_display(self):
        return f"{intcomma(self.price)} UZS"

    def __str__(self):
        return self.name

    def update_average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        self.average_rating = avg_rating if avg_rating else 0.0
        self.save()


class Rating(models.Model):
    RATING_CHOICES = [
        (1, 'R1'),
        (2, 'R2'),
        (3, 'R3'),
        (4, 'R4'),
        (5, 'R5'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="ratings", verbose_name="Dish")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Rating")

    class Meta:
        unique_together = ('user', 'dish')

    def save(self, *args, **kwargs):
        if self.user.is_superuser:
            raise ValueError("Superuser cannot rate!")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} -> {self.dish} ({self.rating})"


@receiver(post_save, sender=Rating)
@receiver(post_delete, sender=Rating)
def update_dish_rating(sender, instance, **kwargs):
    instance.dish.update_average_rating()
