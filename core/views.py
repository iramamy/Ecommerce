from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Category

# Create your views here.


def index(request):
    products = Product.objects.filter(
        featured=True,
        product_status='published',
    ).order_by('-updated')

    context = {
        'products': products
    }

    return render(request, 'core/index.html', context)


def product_list(request):

    products = Product.objects.filter(
        product_status='published'
    )

    context = {
        'products': products
    }

    return render(request, 'core/product_list.html', context)


def category_list(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'core/category_list.html', context)