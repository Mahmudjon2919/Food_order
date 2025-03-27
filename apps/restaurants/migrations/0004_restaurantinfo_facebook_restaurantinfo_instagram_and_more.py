# Generated by Django 5.1.7 on 2025-03-27 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_restaurantinfo_dish_sold_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantinfo',
            name='facebook',
            field=models.URLField(blank=True, null=True, verbose_name='Facebook Link'),
        ),
        migrations.AddField(
            model_name='restaurantinfo',
            name='instagram',
            field=models.URLField(blank=True, null=True, verbose_name='Instagram Link'),
        ),
        migrations.AddField(
            model_name='restaurantinfo',
            name='telegram',
            field=models.URLField(blank=True, null=True, verbose_name='Telegram Link'),
        ),
        migrations.AddField(
            model_name='restaurantinfo',
            name='working_hours',
            field=models.CharField(default='10:00 - 22:00', max_length=255, verbose_name='Working Hours'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Discount'),
        ),
    ]
