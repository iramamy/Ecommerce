from django.shortcuts import render
import json

from .models import Payment, Order


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

    return render(request, 'order/payement.html')
