from django.shortcuts import render
from django.db.models import Count, Q
from .models import Category, Vendor

def default(request):
    categories = Category.objects.annotate(
        product_count=Count(
            'category',
            filter=Q(category__product_status='published')
        )
    )
    
    context = {
        'categories': categories,
    }

    return context

def vendor(request):
    vendors = Vendor.objects.all()

    context = {
        'vendors': vendors
    }

    return context