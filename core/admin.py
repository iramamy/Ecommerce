from django.contrib import admin

from .models import (
    Category,
    Vendor,
    Product,
    CartOrder,
    CartOrderItem,
    ProductImage,
    ProductReview,
    WishList,
    Address
)

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):

    inlines = [ProductImageAdmin]

    list_display = [
        "user",
        'title',
        'product_image',
        'price',
        'featured',
        'product_status',
    ]


class CategoryAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        'category_image',
    ]


class VendorAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        'vendor_image',
    ]

class CartOrderAdmin(admin.ModelAdmin):

    list_display = [
        "user",
        'paid_status',
        'order_date',
        'product_status',
    ]


class CartOrderItemAdmin(admin.ModelAdmin):

    list_display = [
        "order",
        'invoice_number',
        'item',
        'image',
        'quantity',
        'price',
        'total',
    ]


class ProductReviewAdmin(admin.ModelAdmin):

    list_display = [
        "product",
        'user',
        'rating',
        'review',
        'date',
    ]


class WishlistAdmin(admin.ModelAdmin):

    list_display = [
        "user",
        'product',
        'date',
    ]


class AddressAdmin(admin.ModelAdmin):

    list_display = [
        "user",
        'address',
        'status',
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItem, CartOrderItemAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(WishList, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
