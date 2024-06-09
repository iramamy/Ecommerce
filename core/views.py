from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Category

# Create your views here.


def index(request):
    """
    Renders the index page with a list of featured and published products.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response containing the index page with the list of products.
    """
    
    products = Product.objects.filter(
        featured=True,
        product_status='published',
    ).order_by('-updated')

    context = {
        'products': products
    }

    return render(request, 'core/index.html', context)


def product_list(request):
    """
    Retrieves a list of all published products from the database and renders them.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response containing the list of published products.
    """
    products = Product.objects.filter(
        product_status='published'
    )

    context = {
        'products': products
    }

    return render(request, 'core/product_list.html', context)


def category_list(request):
    """
    Retrieves a list of all categories from the database and renders them.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response containing the list of categories.
    """

    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'core/category_list.html', context)


 
def product_per_category(request, category_name, cid):
    """
        
    """
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(
        product_status='published',
        category=category        
        )
    
    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'core/product_per_category.html', context)

