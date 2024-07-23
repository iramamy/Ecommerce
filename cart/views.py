from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

from .models import Cart
from core.models import Product

@login_required(login_url='signin')
def cart_view(request):

    return render(request, 'cart/cart.html')


def add_to_cart(request):

    if request.user.is_authenticated:
        if request.method == 'GET':
        
            try:
                product_id = request.GET.get('product_id')
                product_title = request.GET.get('product_title')
                quantity = int(request.GET.get('quantity'))
                product_price = float(request.GET.get('product_price'))
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
                try:
                    product = Product.objects.get(pid=product_id)

                except Product.DoesNotExist:
                    product = None

                cart, create = Cart.objects.get_or_create(
                    user=request.user,
                    product=product,
                    defaults={
                        'product_quantity': quantity,
                        'product_subtotal': product_price * quantity,
                    },
                )
                
                if not create:
                    cart.product_quantity += quantity
                    cart.product_subtotal += (product_price * quantity)
                    cart.save()


                return JsonResponse({
                    'bool': True,
                    'data': request.session['cart_data_obj'],
                    'total_items': len(request.session['cart_data_obj'])
                })
            except Exception as e:
                return JsonResponse({'bool': False, 'error': str(e)})
    else:

        messages.error(request, 'Please login!')

        return JsonResponse({'bool': False, 'redirect': '/user/signin/'})


def delete_from_cart(request):

    if request.method == 'GET':
        product_id = str(request.GET['product_id'])
        cart_data = request.session['cart_data_obj']
        cart_total_amount = 0
        fee = 1.5

        try:
            product = Product.objects.get(pid=product_id)
        except:
            product = None

        try:
            cart_items = Cart.objects.filter(
                user=request.user,
                product=product
            ).delete()

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
        except Cart.DoesNotExist:
            cart_items = None

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
            product = Product.objects.get(pid=product_id)
        except:
            product = None

        try:
            cart_items = Cart.objects.filter(
                user=request.user,
                product=product
                )

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
