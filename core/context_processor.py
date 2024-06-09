from django.shortcuts import render
from .models import Category

def default(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }

    return context