from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string


def wishlist(request):
    return render(request, 'wishlist/wishlist.html')
    
def add_to_wishlist(request):

    product_id = request.GET.get('product_id')
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

    return JsonResponse({
        'data': request.session['wishlist_data_obj'],
        'total_items': len(request.session['wishlist_data_obj'])
    })


def delete_from_wishlist(request):
    
    product_id = str(request.GET['product_id'])
    wishlist_data = request.session['wishlist_data_obj']

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