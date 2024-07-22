from django.contrib import admin
from .models import Cart


class CartAmind(admin.ModelAdmin):
    list_display = [
        "user",
        'image',
        "product_title",
        "product_quantity",
        "product_price",
        "product_category",
    ]

    list_filter = ["user", "product_category"]

# Register your models here.
admin.site.register(Cart, CartAmind)
