# Generated by Django 5.0.7 on 2024-07-26 18:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_delete_address"),
    ]

    operations = [
        migrations.CreateModel(
            name="Coupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(blank=True, max_length=50)),
                ("discount", models.IntegerField(default=1)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
    ]
