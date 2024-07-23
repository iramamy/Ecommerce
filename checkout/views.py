from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime

from cart.models import Cart
from order.models import Order, OrderItem


# Create order number
def order_number():

    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M%S")


@login_required(login_url='signin')
def checkout(request):

    # Show item in check out
    total_amount = 0
    try:
        checkout_items = Cart.objects.filter(
            user=request.user
        )
        for item in checkout_items:
            total_amount += item.product_quantity * item.product_price
        
    except Cart.DoesNotExist:
        checkout_items = None

    try:
        order, order_created = Order.objects.get_or_create(
            user=request.user,
            price=total_amount,
            product_status='processing',
            paid_status=False,
            defaults={
                'invoice_number': order_number()
            }
        )
        if not order_created:
            order.invoice_number = order_number()
            order.save()

    except Order.DoesNotExist:
        pass

    # Plage items to order item
    try:
        for item in checkout_items:

            order_item, order_item_created = OrderItem.objects.get_or_create(
                order=order,
                item=item.product_title,
                quantity=item.product_quantity,
                image=item.product_image,
                price=item.product_price,
                total=item.product_price*item.product_quantity,
                product_status=order.product_status.capitalize()
            )

            if not order_item_created:
                pass

    except OrderItem.DoesNotExist:
        pass

    context = {
        'checkout_items': checkout_items,
        'total_item': checkout_items.count(),
        'total_amount': round(total_amount, 2),
        'order_number': order.invoice_number
    }

    return render(request, 'checkout/checkout.html', context)
