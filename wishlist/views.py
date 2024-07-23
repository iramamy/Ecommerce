from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

from core.models import Product
from .models import WishList

@login_required(login_url='signin')
def wishlist(request):
    return render(request, 'wishlist/wishlist.html')
    
def add_to_wishlist(request):

    if request.user.is_authenticated:

        if request.method == 'GET':
            try:
                product_id = str(request.GET.get('product_id'))
                product_title = request.GET.get('product_title')
                quantity = int(request.GET.get('quantity'))
                product_price = request.GET.get('product_price')
                image = request.GET.get('image')
                category = request.GET.get('category')

                wishlist_product = {
                    'product_title': product_title,
                    'quantity': quantity,
                    'product_price': product_price,
                    'image': image,
                    'category': category,
                }

                if 'wishlist_data_obj' in request.session:
                    wishlist_data = request.session['wishlist_data_obj']
                    if product_id in wishlist_product:
                        pass
                    else:
                        wishlist_data[product_id] = wishlist_product
                else:
                    wishlist_data = {product_id: wishlist_product}

                request.session['wishlist_data_obj'] = wishlist_data
                request.session.modified = True

                # Add item to wishlist
                try:
                    product = Product.objects.get(pid=product_id)

                except Product.DoesNotExist:
                    product = None
                
                wishlist, created = WishList.objects.get_or_create(
                        user=request.user,
                        product=product,
                        defaults={'quantity': quantity}
                    )

                if not created:
                    wishlist.quantity = quantity
                    wishlist.save()

                return JsonResponse({
                    'data': request.session['wishlist_data_obj'],
                    'total_items': len(request.session['wishlist_data_obj'])
                })
            
            except Exception as e:
                return JsonResponse({'bool': False, 'error': str(e)})

    else:

        messages.error(request, 'Please login!')

        return JsonResponse({'bool': False, 'redirect': '/user/signin/'})

def delete_from_wishlist(request):
    
    product_id = str(request.GET['product_id'])
    wishlist_data = request.session['wishlist_data_obj']

    try:
        product = Product.objects.get(pid=product_id)
    except Product.DoesNotExist:
        product = None

    try:
        wishlist_items  = WishList.objects.get(
            user=request.user,
            product=product
        ).delete()

    except WishList.DoesNotExist:
        pass

    if 'wishlist_data_obj' in request.session:
        if product_id in wishlist_data:
            del wishlist_data[product_id]
            request.session['wishlist_data_obj'] = wishlist_data
            request.session.modified = True
        
        wishlist_data = request.session['wishlist_data_obj']

        context = {
                    'wishlist_data': wishlist_data,
                    'total_item_wishlist': len(wishlist_data),
                }

    else:
        context = {
                    'total_item_wishlist': 0,
                }
    
    data = render_to_string('wishlist/async/wish-list.html', context)

    return JsonResponse({
        'data': data,
        'total_items': len(wishlist_data),
    })
