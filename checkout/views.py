from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
import json
from django.http import JsonResponse
from django.template.loader import render_to_string

from cart.models import Cart
from order.models import Order, OrderItem
from userauths.models import Address


# Create order number
def order_number():

    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M%S")

@login_required(login_url='signin')
def checkout(request):

    address = None

    # Save address
    if request.method == 'POST':
        address_data = json.loads(request.body)

        address, create = Address.objects.get_or_create(
            user=request.user,
            defaults={
                'first_name': address_data['first_name'],
                'last_name': address_data['last_name'],
                'address1': address_data['address1'],
                'address2': address_data['address2'],
                'country': address_data['country'],
                'city': address_data['city'],
                'zipcode': address_data['zipcode'],
                'phone': address_data['phone'],
                'email': address_data['email'],
                'company_name': address_data['company_name'],
                'additional_information': address_data['additional_info'],
            }
        )
        if not create:
            address.first_name = address_data['first_name']
            address.last_name = address_data['last_name']
            address.address1 = address_data['address1']
            address.address2 = address_data['address2']
            address.country = address_data['country']
            address.city = address_data['city']
            address.zipcode = address_data['zipcode']
            address.phone = address_data['phone']
            address.email = address_data['email']
            address.company_name = address_data['company_name']
            address.additional_information = address_data['additional_info']
            address.save()


    context = {
        'address': address
    }

    data = render_to_string('checkout/checkout.html', context)

    return JsonResponse({
        'data': data
    })
