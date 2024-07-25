from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.template.loader import render_to_string

from .forms import UserRegisterForm
from .models import User
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


def signout(request):
    auth.logout(request)

    messages.success(request, 'You are currently logged out!')
    return redirect('signin')

# User dashbord
@login_required(login_url='signin')
def dashboard_view(request):
    return render(request, 'userauths/dashboard.html')
    

def dashboard_order(request):
    # Get orders
    orders = Order.objects.filter(
        user=request.user,
        paid_status=True
    ).annotate(item_count=Count('orderitem')).order_by('-order_date')

    context = {
        'orders': orders,
    }

    
    data = render_to_string('userauths/async/dashboard-order.html', context)

    return JsonResponse({
        'data': data
    })


def order_detail(request, orderID):
    order = Order.objects.get(
        user=request.user,
        paid_status=True,
        invoice_number=orderID
    )

    print("Order", order)

    order_products = OrderProduct.objects.filter(order=order).order_by('-created_at')

    context = {
        'order_products': order_products,
        'order': order,
    }
    data = render_to_string('userauths/order-detail.html', context)

    return JsonResponse({
        'data': data
    })
