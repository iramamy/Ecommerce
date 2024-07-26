from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q, Avg
from taggit.models import Tag
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.utils import timezone

from .models import Product, Category, Vendor, ProductReview
from .forms import ReviewForm



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
        product_status='published',
        stock_count__gt=0
    )
    
    product_count = products.count()
    product = Product.objects.first()

    # Get all related images
    related_images = product.p_images.all()

    context = {
        'products': products,
        'product_count': product_count,
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
        category=category,
        stock_count__gt=0   
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
        product_status='published',
        stock_count__gt=0
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
        category=product.category,
        stock_count__gt=0
        ).exclude(pid=pid)

    if request.user.is_authenticated:
        is_review_exist = ProductReview.objects.filter(
            user=request.user, product=product
        ).exists()
    else:
        is_review_exist = False

    # Get review
    p_reviews = ProductReview.objects.filter(product=product).order_by('-date')

    # Average review
    avg_rating = ProductReview.objects.filter(
        product=product).aggregate(rating=Avg('rating'))

    # Rating counts
    rating_counts = ProductReview.objects.filter(
        product=product).values('rating').annotate(count=Count('rating'))

    rating_track = {1:0, 2:0, 3:0, 4:0, 5:0}

    for rating in rating_counts:
        rating_track[rating['rating']] = rating['count']

    p_images = product.p_images.all()

    # Review comment form
    review_form = ReviewForm()

    
    context = {
        "product": product,
        "p_images": p_images,
        "products": products,
        "reviews": p_reviews,
        'avg_rating': avg_rating,
        'rating_track': rating_track,
        "review_form": review_form,
        "is_review_exist": is_review_exist
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


def search_product(request):
    keyword = request.GET.get('keyword', '')
    category_id = request.GET.get('category')
    products = Product.objects.none()
    product_count = 0
    
    if keyword:
        if category_id:
            products = Product.objects.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword),
                Q(category__cid=category_id), Q(product_status='published'),
                Q(stock_count__gt=0)
            ).order_by('-date')
        else:
            products = Product.objects.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword),
                Q(product_status='published')
            ).order_by('-date')

        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword,
    }

    return render(request, 'core/search.html', context)


def filter_product(request):
    categories_id = request.GET.getlist('category[]')
    vendors_id = request.GET.getlist('vendor[]')
    tags_id = request.GET.getlist('tags[]')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(
        product_status='published',
        stock_count__gt=0
    ).order_by('-id').distinct()

    if len(categories_id)>0:
        products = products.filter(category__id__in=categories_id).distinct()

    if len(vendors_id)>0:
        products = products.filter(vendor__id__in=vendors_id).distinct()

    if len(tags_id)>0:
        products = products.filter(tags__id__in=tags_id).distinct()

    if len([min_price, max_price])>0:
        products = products.filter(price__range=[min_price, max_price]).distinct()

    context = {
        'products': products,
        'product_count': products.count(),
    }

    data = render_to_string('core/async/product_list.html', context)
    count = render_to_string('core/async/product_count.html', context)

    return JsonResponse({
        "data": data,
        "product_count": count,
    })


# Review comment
def add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user

    review=request.POST['review']
    rating=request.POST['rating']
    current_time = timezone.now()

    new_review = ProductReview.objects.create(
        user=user,
        product=product,
        review=review,
        rating=rating,
    )

    context = {
        'user': user.username,
        'review': review,
        'rating': rating,
        'date': new_review.date.strftime('%d %b, %Y %H:%M'),
    }

    avg_rating = ProductReview.objects.filter(
        product=product).aggregate(rating=Avg('rating'))

    return JsonResponse({
        'bool': True,
        'context': context,
        'avg_rating': avg_rating
    })
