from django.shortcuts import render
from django.db.models import Count, Q, Min, Max
from taggit.models import Tag
from .models import Category, Vendor, Product

def default(request):
    
    categories = Category.objects.annotate(
        product_count=Count(
            'category',
            filter=Q(category__product_status='published')
        )
    )
    vendors = Vendor.objects.all()
    tags = Tag.objects.all()

    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))
    
    context = {
        'categories': categories,
        'vendors': vendors,
        'tags': tags,
        'min_max_price': min_max_price,
    }

    return context