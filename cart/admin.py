from django.contrib import admin
from .models import Cart


class CartAmind(admin.ModelAdmin):
    list_display = [
        "user",
        'image',
        "product_quantity",
        'product_subtotal',
        "product",
    ]

    list_filter = ["user", ]
    
# Register your models here.
admin.site.register(Cart, CartAmind)
