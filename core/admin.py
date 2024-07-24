from django.contrib import admin

from .models import (
    Category,
    Vendor,
    Product,
    ProductImage,
    ProductReview
)

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):

    inlines = [ProductImageAdmin]

    list_display = [
        'title',
        'product_image',
        'price',
        'category',
        'vendor',
        'featured',
        'product_status',
        'stock_count',
    ]

    list_filter = [
        'category',
        'vendor',
    ]

    list_editable = ['featured',]


class CategoryAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        'category_image',
    ]


class VendorAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        "title",
        'vendor_image',
    ]


class ProductReviewAdmin(admin.ModelAdmin):

    list_display = [
        "product",
        'user',
        'rating',
        'review',
        'date',
    ]
    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
