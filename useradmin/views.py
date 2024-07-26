from django.shortcuts import render
from core.models import Product, Category
from order.models import OrderProduct
from userauths.models import User
from django.db.models import Sum

import datetime

def dashboard(request):
    revenue = OrderProduct.objects.aggregate(
        total_price=Sum("product_price")
    )

    total_orders_count = OrderProduct.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by('-id')

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
    }

    return render(request, 'useradmin/useradmin.html', context)

