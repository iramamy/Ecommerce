# Generated by Django 5.0.7 on 2024-07-23 08:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wishlist", "0003_rename_quantity_wishlist_product_quantity_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wishlist",
            name="product_subtotal",
        ),
    ]
