from django.contrib import admin
from .models import Order, OrderItem, Payment


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
        'item',
        'item_image',
        'quantity',
        'price',
        'total',
        'product_status'
    ]

    
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        "user",
        'invoice_number',
        'payement',
        "price",
        'paid_status',
        'product_status',
        'order_date',        
    ]

    list_editable = ['product_status',]
    
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


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Payment, PaymentAdmin)
