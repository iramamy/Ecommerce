# Generated by Django 5.0.7 on 2024-07-23 08:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wishlist", "0004_remove_wishlist_product_subtotal"),
    ]

    operations = [
        migrations.DeleteModel(
            name="WishList",
        ),
    ]
