# Generated by Django 5.0.7 on 2024-07-23 07:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0004_cart_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="product_image",
            field=models.CharField(
                blank=True, default="product.jpg", max_length=100, null=True
            ),
        ),
    ]
