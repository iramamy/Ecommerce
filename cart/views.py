from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Cart 


@login_required(login_url='signin')
def cart_view(request):

    cart_total_amount = 0
    fee = 1.5

    if 'cart_data_obj' in request.session:
        del request.session['cart_data_obj']
    
    try:
        cart_items = Cart.objects.filter(user=request.user)
        cart_data_obj = {}
        for item in cart_items:
            cart_data_obj[item.product_id] = {
                'product_title': item.product_title,
                'quantity': item.product_quantity,
                'product_price': item.product_price,
                'image': item.product_image,
                'category': item.product_category,
            }
        
        request.session['cart_data_obj'] = cart_data_obj

        for product_id, item in cart_data_obj.items():

            subtotal = round(int(item['quantity']) * float(item['product_price']), 2)
            item['subtotal'] = subtotal
            cart_total_amount += subtotal

        cart_grand_total = round((cart_total_amount + (cart_total_amount * fee)/100), 2)


    except Cart.DoesNotExist:
        cart_items = None

    context = {
            'cart_total_amount': round(cart_total_amount, 2),
            'cart_data': cart_data_obj,
            'cart_grand_total': cart_grand_total,
            'total_item': len(cart_data_obj),
        }

    return render(request, 'cart/cart.html', context)


# @login_required(login_url='signin')
def add_to_cart(request):
    
    if request.method == 'GET' and request.user.is_authenticated:
        try:
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
            request.session.modified = True

            # Add item to cart
            with transaction.atomic():
                cart, created = Cart.objects.get_or_create(
                    product_id=product_id,
                    product_title=product_title,
                    product_quantity=quantity,
                    product_price=product_price,
                    product_category=category,
                    user=request.user,
                    product_image=image,
                )

                # subtotal = round(int(quantity) * float(product_price), 2)

                if not created:
                    cart.product_quantity += quantity
                    cart.product_subtotal = round(cart.product_quantity * float(product_price), 2)
                    cart.save()

            return JsonResponse({
                'bool': True,
                'data': request.session['cart_data_obj'],
                'total_items': len(request.session['cart_data_obj'])
            })
        except Exception as e:
            return JsonResponse({'bool': False, 'error': str(e)})

    return JsonResponse({
        'bool': False,
        'error': 'Invalid request method or user not authenticated'
        })


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
        context = {
            'total_item': 0,
        }
    
    data = render_to_string('cart/async/cart-list.html', context)

    return JsonResponse({
        'data': data,
        'total_items': len(cart_data),
    })

def update_cart(request):

    if request.method == 'GET':

        product_id = str(request.GET['product_id'])
        quantity = int(request.GET['quantity'])
        cart_data = request.session['cart_data_obj']
        cart_total_amount = 0
        fee = 1.5

        try:
            cart_items = Cart.objects.filter(user=request.user, product_id=product_id)

            if 'cart_data_obj' in request.session:
                for p_id, item in cart_data.items():
                    item = cart_data[product_id]
                    item['quantity'] = quantity

                    request.session['cart_data_obj'] = cart_data
                    request.session.modified = True

                    subtotal = round(int(item['quantity']) * float(item['product_price']), 2)
                    item['subtotal'] = subtotal

                    # Save to database
                    cart_items.update(
                        product_quantity=quantity,
                        product_subtotal=subtotal
                        )

            if 'cart_data_obj' in request.session:
                for p_id, item in cart_data.items():
                    subtotal = round(int(item['quantity']) * float(item['product_price']), 2)
                    item['subtotal'] = subtotal
                    cart_total_amount += subtotal

                cart_grand_total = round((cart_total_amount + (cart_total_amount * fee)/100), 2)
                request.session['cart_data_obj'] = cart_data

                # print('cart data', cart_data)
                
                # print('cart_grand_total', cart_grand_total)
                context = {
                        'cart_total_amount': round(cart_total_amount, 2),
                        'cart_data': cart_data,
                        'cart_grand_total': cart_grand_total,
                    }
                
                item = cart_data[product_id]
        except Cart.DoesNotExist:
            cart_items = None

        data = render_to_string('cart/async/update-cart.html', context)

        return JsonResponse({
            'data': data,
            'item': item,
        })
