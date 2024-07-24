from django.shortcuts import render
import json
from django.http import JsonResponse

from .models import Payment, Order, OrderProduct
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

    if payement.status == 'COMPLETED':
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


def payement_failed(request):
    return render(request, 'order/payment-failed.html')

def payement_completed(request):
    return render(request, 'order/payment-completed.html')