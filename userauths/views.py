from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.template.loader import render_to_string
import json

from .forms import UserRegisterForm
from .models import User, Address
from order.models import Order, OrderProduct


def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():

            new_user = form.save()
            username = form.cleaned_data['username']

            messages.success(request, f"{username}, your account was created successfully.") # noqa

            new_user = auth.authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
                )

            auth.login(request, new_user)

            return redirect('home')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }

    return render(request, 'userauths/register.html', context)


def signin(request):

    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in!')

        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(
                email=email,
            )

            user = auth.authenticate(
                request,
                email=email,
                password=password
            )

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You are logged in!')
                return redirect('home')

        except User.DoesNotExist:
            messages.error(request, f"User with {email} does not exist!")
            return redirect('signin')

    return render(request, 'userauths/signin.html')


@login_required(login_url='signin')
def signout(request):
    auth.logout(request)

    messages.success(request, 'You are currently logged out!')
    return redirect('signin')

# User dashbord
@login_required(login_url='signin')
def dashboard_view(request):

    address = Address.objects.get(user=request.user)

    context = {
        'address': address,
    }

    return render(request, 'userauths/dashboard.html', context)
    
@login_required(login_url='signin')
def dashboard_order(request):
    # Get orders
    orders = Order.objects.filter(
        user=request.user,
        paid_status=True
    ).annotate(item_count=Count('orderitem')).order_by('-order_date')

    orders_count = orders.count()

    if orders_count:
        context = {
            'orders': orders,
        }

        data = render_to_string('userauths/async/dashboard-order.html', context)

        return JsonResponse({
            'data': data,
        })
    else:
        data = render_to_string('userauths/async/no-order.html')

        return JsonResponse({
            'data': data,
        })


@login_required(login_url='signin')
def order_detail(request, orderID):
    order = Order.objects.get(
        user=request.user,
        paid_status=True,
        invoice_number=orderID
    )

    order_products = OrderProduct.objects.filter(order=order).order_by('-created_at')

    context = {
        'order_products': order_products,
        'order': order,
    }
    data = render_to_string('userauths/order-detail.html', context)

    return JsonResponse({
        'data': data
    })

def address(request):
    address = Address.objects.get(user=request.user)

    context = {
        'address': address,
    }

    data = render_to_string('userauths/async/address.html', context)

    return JsonResponse({
        'data': data
        })

def billing_address(request):

    if request.method == 'POST':
        data = json.loads(request.body)

        address, create = Address.objects.get_or_create(
            user=request.user,
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'address1': data['address1'],
                'address2': data['address2'],
                'country': data['country'],
                'city': data['city'],
                'zipcode': data['zipcode'],
                'phone': data['phone'],
                'email': data['email'],
                'company_name': data['company_name'],
            }
        )
        if not create:
            address.first_name = data['first_name']
            address.last_name = data['last_name']
            address.address1 = data['address1']
            address.address2 = data['address2']
            address.country = data['country']
            address.city = data['city']
            address.zipcode = data['zipcode']
            address.phone = data['phone']
            address.email = data['email']
            address.company_name = data['company_name']
            address.save()

            context = {
                'address': address,
            }

            data = render_to_string('userauths/async/address.html', context)

            return JsonResponse({
                'data': data
                })

    address = Address.objects.get(user=request.user)

    context = {
        'address': address,
    }

    data = render_to_string(
        'userauths/async/billing-address.html',
        context,
        request=request
        )

    return JsonResponse({
        'data': data
    })

def shipping_address(request):

    data = render_to_string('userauths/async/shipping-address.html')

    return JsonResponse({
        'data': data
    })