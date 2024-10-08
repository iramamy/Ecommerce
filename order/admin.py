from django.contrib import admin
from .models import Order, OrderItem, Payment, OrderProduct


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = [
        'item',
        'item_image',
        'quantity',
        'price',
        'total',
        'product_status'
    ]


class OrderItemAdmin(admin.ModelAdmin):

    list_display = [
        'order',
        'item',
        'item_image',
        'quantity',
        'price',
        'total',
        'product_status'
    ]

    readonly_fields = [
        'order',
        'item',
        'item_image',
        'image',
        'quantity',
        'price',
        'total',
        'product_status'
    ]

class OrderAdmin(admin.ModelAdmin):

    list_display = [
        "user",
        'address',
        'invoice_number',
        'payment',
        "price",
        'paid_status',
        'product_status',
        'order_date',        
    ]

    readonly_fields = [
        'address',
        "user",
        'invoice_number',
        'payment',
        "price",
        'paid_status',
        'order_date',        
    ]    
    
    inlines = [OrderItemInline]

class PaymentAdmin(admin.ModelAdmin):

    list_display = [
        'payment_id',
        'user',
        'payment_method',
        'amount_paid',
        'status',
        'created_at'
    ]

class OrderProductAdmin(admin.ModelAdmin):

    list_display = [
        "user",
        "product",
        'order',
        "payment",
        "quantity",
        "product_price",
        "ordered",
        "created_at",
    ]

    readonly_fields = [
        "user",
        "product",
        'order',
        "payment",
        "quantity",
        "product_price",
        "ordered",
        "created_at",
        "updated_ad",
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
