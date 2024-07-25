from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse
import datetime

from .models import Payment, Order, OrderProduct, OrderItem
from cart.models import Cart, Product
from userauths.models import Address


# Create order number
def order_number():

    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M%S")


def place_order(request):
    
    try:
        address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        address = None

    # Show item in check out
    total_amount = 0
    
    try:
        checkout_items = Cart.objects.filter(
            user=request.user
        )

        for item in checkout_items:
            total_amount += item.product_quantity * item.product.price
        
    except Cart.DoesNotExist:
        checkout_items = None

    try:
        order, order_created = Order.objects.get_or_create(
            user=request.user,
            price=total_amount,
            product_status='processing',
            paid_status=False,
            defaults={
                'address': address,
                'invoice_number': order_number()
            }
        )
        if not order_created:
            order.invoice_number = order_number()
            order.address = address
            order.save()

    except Order.DoesNotExist:
        pass

    # Place items to order item
    try:
        for item in checkout_items:

            order_item, order_item_created = OrderItem.objects.get_or_create(
                order=order,
                item=item.product.title,
                quantity=item.product_quantity,
                image=item.product.image,
                price=item.product.price,
                total=item.product.price*item.product_quantity,
                product_status=order.product_status.capitalize()
            )

            if not order_item_created:
                pass

    except OrderItem.DoesNotExist:
        pass

    # Show item in check out
    total_amount = 0

    try:
        checkout_items = Cart.objects.filter(
            user=request.user
        )

        for item in checkout_items:
            total_amount += item.product_quantity * item.product.price
        
    except Cart.DoesNotExist:
        checkout_items = None

    context = {
        'checkout_items': checkout_items,
        'total_item': checkout_items.count(),
        'total_amount': round(total_amount, 2),
        'order_number': order.invoice_number,
        'address': address
    }

    return render(request, 'order/place_order.html', context)

def payment(request):

    body = json.loads(request.body)

    try:
        order = Order.objects.get(
            user=request.user,
            paid_status=False,
            invoice_number=body['orderID']
            )
    except Order.DoesNotExist:
        order = None
    
    # Store transaction detail
    payment = Payment(
        user=request.user,
        amount_paid=order.price,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        status=body['status'],
    )

    # Save
    payment.save()

    if payment.status != 'COMPLETED':
        return redirect('payment_failed')

    order.paid_status = True
    order.payment = payment
    order.save()

    # Move item to user history
    try:
        cart_items = Cart.objects.filter(
            user=request.user
        )
    except Cart.DoesNotExist:
        cart_items = None

    for item in cart_items:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.user = request.user
        order_product.payment = payment
        order_product.product_id = item.product.id
        order_product.quantity = item.product_quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        # Reduce quantity in stock
        product = Product.objects.get(pid=item.product.pid)
        product.stock_count -= item.product_quantity
        product.save()

    # Clear item in cart
    Cart.objects.filter(user=request.user).delete()

    # Render payment complete page
    data = {
        'invoice_number': order.invoice_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)

def payment_completed(request):

    grand_total = 0
    invoice_number = request.GET['invoice_number']
    transID = request.GET['payment_id']

    order = get_object_or_404(
        Order,
        invoice_number=invoice_number,
        paid_status=True
        )
    
    try:
        ordered_products = OrderProduct.objects.filter(
            order=order
        )
    except OrderProduct.DoesNotExist:
        return redirect('home')

    for item_ordered in ordered_products:
        grand_total += (item_ordered.quantity * item_ordered.product.price)

    context = {
        "order": order,
        'order_products': ordered_products,
        'grand_total': grand_total
    }

    return render(request, 'order/payment-completed.html', context)


def payment_failed(request):
    return render(request, 'order/payment-failed.html')
