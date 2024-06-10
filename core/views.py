from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from taggit.models import Tag
from .models import Product, Category, Vendor

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

    categories = Category.objects.annotate(
        product_count=Count(
            'category', 
            filter=Q(category__product_status='published')
            )
    )

    context = {
        'categories': categories
    }

    return render(request, 'core/category_list.html', context)


 
def product_per_category(request, category_name, cid):

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


def vendor_list(request):
    vendors = Vendor.objects.annotate(
        product_count=Count('vendor', filter=Q(vendor__product_status='published'))
    )
    context = {
        'vendors': vendors
    }

    return render(request, 'core/vendor.html', context)


def vendor_detail(request, vendor_name, vid):
    vendor = Vendor.objects.get(vid=vid)

    products_per_vendor = Product.objects.filter(
        vendor=vendor, 
        product_status='published'
    )

    product_counts = products_per_vendor.values(
        'category__title',
        'category__image'
        ).annotate(count=Count('id'))

    context = {
        'vendor': vendor,
        'products': products_per_vendor,
        'product_counts': product_counts
    }

    return render(request, 'core/vendor_detail.html', context)

def product_detail(request, category_name, pid):

    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(
        category=product.category
        ).exclude(pid=pid)

    p_images = product.p_images.all()

    for p in products:
        print('related_product:', p.title)
        print('related_product:', p.category)
    
    context = {
        "product": product,
        "p_images": p_images,
        "products": products,
    }
    
    return render(request, 'core/product_detail.html', context)


def tag_list(request, tag_slug=None):

    products = Product.objects.filter(
        product_status='published'
    ).order_by('-id')

    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag,
    }

    return render(request, 'core/tag_list.html', context)
