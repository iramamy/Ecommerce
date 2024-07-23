from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cart.models import Cart

@login_required(login_url='signin')
def checkout(request):

    total_amount = 0
    try:
        checkout_items = Cart.objects.filter(
            user=request.user
        )
        for item in checkout_items:
            total_amount += item.product_quantity * item.product_price
        
    except Cart.DoesNotExist:
        checkout_items = None

    context = {
        'checkout_items': checkout_items,
        'total_item': checkout_items.count(),
        'total_amount': round(total_amount, 2)
    }

    return render(request, 'checkout/checkout.html', context)
