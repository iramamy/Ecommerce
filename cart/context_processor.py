from .models import Cart

def cart_view(request):

    cart_total_amount = 0
    fee = 1.5

    if 'cart_data_obj' in request.session:
        del request.session['cart_data_obj']
        
    if request.user.is_authenticated:
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

        return context

    else:          
        context = {
            'total_item': 0,
        }

        return context