from django.shortcuts import render, redirect
from core.models import Product, Category, ProductReview, Vendor
from order.models import OrderProduct, Order
from userauths.models import UserProfile
from django.db.models import Sum
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

from .forms import AddProductForm
from django.contrib import messages
import datetime
from .decorators import admin_required


@admin_required
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

@admin_required
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

@admin_required
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

@admin_required
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

@admin_required
def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()

    return redirect('useradmin_products')


########################## Orders ##########################
@admin_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-id')
    context = {
        'orders': orders
    }

    return render(request, 'useradmin/admin_orders.html', context)

@admin_required
def admin_order_detail(request, orderID):
    orders = Order.objects.get(
        invoice_number=orderID
    )

    order_products = OrderProduct.objects.filter(
        order=orders
    )

    context = {
        'orders': orders,
        "order_products": order_products
    }

    return render(request, 'useradmin/admin_order_detail.html', context)

@admin_required
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

@admin_required
def delete_order(request, orderID):
    orders = Order.objects.get(
        invoice_number=orderID
    )

    orders.delete()

    messages.success(request, f'Order #{orderID} delted successfully!')

    return redirect('admin_orders')

@admin_required
def vendor_page(request, vendor_name, vid):
    vendor = Vendor.objects.get(vid=vid)

    products_per_vendor = Product.objects.filter(
        vendor=vendor,
    )

    revenue_per_vendor = OrderProduct.objects.filter(
        product__vendor=vendor
    ).aggregate(total_price=Sum("product_price"))

    product_sold = OrderProduct.objects.filter(
        product__vendor=vendor
    )

    context = {
        'vendor': vendor,
        'products': products_per_vendor,
        'revenue_per_vendor': revenue_per_vendor,
        "products_per_vendor": products_per_vendor,
        "product_sold": product_sold
    }

    return render(request, 'useradmin/vendor-page.html', context)

@admin_required
def reviews(request):
    product_review = ProductReview.objects.all()

    context = {
        'product_review': product_review
    }

    return render(request, 'useradmin/reviews.html', context)

@admin_required
def settings(request):

    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        profile_picture = request.FILES.get('profile_picture')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        address = request.POST.get('address')
        country = request.POST.get('country')

        # Save/update profile
        profile, create = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'bio': bio,
                'phone_number': phone,
                'image': profile_picture,
                'address': address,
                "country": country
            }
        )

        if not create:
            profile.first_name = first_name
            profile.last_name = last_name
            profile.phone_number = phone
            profile.address = address
            profile.country = country
            if profile_picture:
                profile.image = profile_picture
            profile.bio = bio

            profile.save()

        messages.success(request, 'Profile updated!')

        return redirect('settings')

    context = {
            'profile': user_profile
        }

    return render(request, 'useradmin/settings.html', context)


@admin_required
def change_password(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        old_password = request.POST.get('old_password')

        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if not check_password(old_password, user.password):
            messages.error(request, 'Old password is incorrect!')
            return redirect('change_password')

        user.set_password(new_password)
        user.save()
        messages.success(request, 'Password changed successfully!')
        return redirect('signin')

    context = {
            'profile': user_profile
        }

    return render(request, 'useradmin/change_password.html', context)
