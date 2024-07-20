from django.shortcuts import render
from django.http import JsonResponse

def add_to_cart(request):
    
    product_id = request.GET.get('product_id')
    product_title = request.GET.get('product_title')
    quantity = int(request.GET.get('quantity'))
    product_price = request.GET.get('product_price')
    image = request.GET.get('image')
    category = request.GET.get('category')
    
    cart_product = {
        'product_title': product_title,
        'quantity': quantity,
        'product_price': product_price,
        'image': image,
        'category': category,
    }

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        if product_id in cart_data:
            cart_data[product_id]['quantity'] += quantity
        else:
            cart_data[product_id] = cart_product
    else:
        cart_data = {product_id: cart_product}

    request.session['cart_data_obj'] = cart_data

    return JsonResponse({
        'bool': True,
        'data': request.session['cart_data_obj'],
        'total_items': len(request.session['cart_data_obj'])
    })


def cart_view(request):

    return render(request, 'cart/cart.html')
