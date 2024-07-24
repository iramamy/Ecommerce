from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse

from .models import Payment, Order, OrderProduct, OrderItem
from cart.models import Cart, Product


def payement(request):

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
    payement = Payment(
        user=request.user,
        amount_paid=order.price,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        status=body['status'],
    )

    # Save
    payement.save()

    if payment.status != 'COMPLETED':
        return redirect('payment_failed')

    order.paid_status = True
    order.payement = payement
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
        order_product.payment = payement
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
        'transID': payement.payment_id,
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
