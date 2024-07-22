from django.shortcuts import render
from django.http import JsonResponse


def wishlist(request):
    return render(request, 'wishlist/wishlist.html')
    
def add_to_wishlist(request):

    product_id = request.GET.get('product_id')
    product_title = request.GET.get('product_title')
    product_price = request.GET.get('product_price')
    image = request.GET.get('image')
    category = request.GET.get('category')

    wishlist_product = {
        'product_title': product_title,
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

    print(request.session['wishlist_data_obj'] )

    return JsonResponse({
        'bool': True,
        'data': request.session['wishlist_data_obj'],
        'total_items': len(request.session['wishlist_data_obj'])
    })
