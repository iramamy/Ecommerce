from django.shortcuts import render
from django.db.models import Count, Q
from taggit.models import Tag
from .models import Category, Vendor

def default(request):
    categories = Category.objects.annotate(
        product_count=Count(
            'category',
            filter=Q(category__product_status='published')
        )
    )
    vendors = Vendor.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'categories': categories,
        'vendors': vendors,
        'tags': tags,
    }

    return context