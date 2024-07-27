from django.shortcuts import render, redirect
from core.models import Product, Category
from order.models import OrderProduct, Order
from userauths.models import UserProfile
from django.db.models import Sum

from .forms import AddProductForm
from django.contrib import messages
import datetime

def dashboard(request):
    
    revenue = OrderProduct.objects.aggregate(
        total_price=Sum("product_price")
    )

    total_orders_count = OrderProduct.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = UserProfile.objects.all().order_by('-id')

    orders = Order.objects.all().order_by('-order_date')

    this_month = datetime.datetime.now().month

    monthly_revenue = OrderProduct.objects.filter(
        created_at__month=this_month
    ).aggregate(total_price=Sum("product_price"))

    context = {
        'revenue': revenue,
        'total_orders_count': total_orders_count,
        'all_products': all_products,
        'all_categories': all_categories,
        'new_customers': new_customers,
        'monthly_revenue': monthly_revenue,
        'orders': orders
    }

    return render(request, 'useradmin/useradmin.html', context)

def products(request):

    all_products = Product.objects.all().order_by('-id')
    all_categories = Category.objects.all()
    status = Product.get_status()

    context = {
        'all_products': all_products,
        'all_categories': all_categories,
        'status': status
    }

    return render(request, 'useradmin/products.html', context)

def add_products(request):
    if request.method == 'POST':
        
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            

            return redirect('useradmin_dashboard')
        else:
            print(form.errors)

    else:
        form = AddProductForm()

    context = {
        'form': form
    }

    return render(request, 'useradmin/add_products.html', context)


def edit_products(request, pid):

    product = Product.objects.get(
        pid=pid
    )

    if request.method == 'POST':
        
        form = AddProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()

            return redirect('useradmin_edit_products', product.pid)
        else:
            print(form.errors)

    else:
        form = AddProductForm(instance=product)

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'useradmin/edit_products.html', context)

def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()

    return redirect('useradmin_products')


########################## Orders ##########################
def admin_orders(request):
    orders = Order.objects.all().order_by('-id')
    context = {
        'orders': orders
    }

    return render(request, 'useradmin/admin_orders.html', context)

def admin_order_detail(request, orderID):
    orders = Order.objects.get(
        invoice_number=orderID
    )

    print('product_status', orders.product_status)

    order_products = OrderProduct.objects.filter(
        order=orders
    )

    context = {
        'orders': orders,
        "order_products": order_products
    }

    return render(request, 'useradmin/admin_order_detail.html', context)

def change_order_status(request, orderID):

    order = Order.objects.get(invoice_number=orderID)

    if request.method == 'POST':
        status = request.POST.get('status')

        order.product_status = status
        order.save()

        messages.success(request, f'Order status changed to {status}!')

        return redirect('admin_order_detail', orderID)

    else:
        messages.error(request, f'Something went wrong!')


def delete_order(request, orderID):
    orders = Order.objects.get(
        invoice_number=orderID
    )

    orders.delete()

    messages.success(request, f'Order #{orderID} delted successfully!')

    return redirect('admin_orders')
