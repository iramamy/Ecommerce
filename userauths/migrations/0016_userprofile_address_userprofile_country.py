# Generated by Django 5.0.7 on 2024-07-27 18:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userauths", "0015_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="address",
            field=models.CharField(
                blank=True, default="Your address", max_length=200, null=True
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="country",
            field=models.CharField(
                blank=True, default="Your country", max_length=200, null=True
            ),
        ),
    ]
