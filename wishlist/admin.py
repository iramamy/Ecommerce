from django.contrib import admin
from .models import WishList

# Register your models here.
class WishlistAdmin(admin.ModelAdmin):

    list_display = [
        "user",
        'product',
        'image',
        'quantity',
        'date',
    ]

admin.site.register(WishList, WishlistAdmin)
