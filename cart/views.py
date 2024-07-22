from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

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


def delete_from_cart(request):
    product_id = str(request.GET['product_id'])
    cart_data = request.session['cart_data_obj']
    cart_total_amount = 0
    fee = 1.5

    if 'cart_data_obj' in request.session:
        if product_id in cart_data:
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data
            request.session.modified = True

    if 'cart_data_obj' in request.session:
        for p_id, item in cart_data.items():
            subtotal = round(int(item['quantity']) * float(item['product_price']), 2)
            item['subtotal'] = subtotal
            cart_total_amount += subtotal

        cart_grand_total = round((cart_total_amount + (cart_total_amount * fee)/100), 2)
        request.session['cart_data_obj'] = cart_data

        context = {
                'cart_total_amount': round(cart_total_amount, 2),
                'cart_data': cart_data,
                'cart_grand_total': cart_grand_total,
                'total_item': len(cart_data),
            }
    else:
        is_not_empty = False            
        context = {
            'total_item': 0,
        }
    
    data = render_to_string('cart/async/cart-list.html', context)

    return JsonResponse({
        'data': data,
        'total_items': len(cart_data),
    })
    