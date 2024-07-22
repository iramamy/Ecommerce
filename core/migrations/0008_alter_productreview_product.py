# Generated by Django 5.0.7 on 2024-07-22 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_alter_product_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productreview",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="p_reviews",
                to="core.product",
            ),
        ),
    ]
