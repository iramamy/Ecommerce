def cart_view(request):

    cart_total_amount = 0
    fee = 1.5

    if 'cart_data_obj' in request.session:

        cart_data_obj = request.session['cart_data_obj']

        for product_id, item in cart_data_obj.items():

            subtotal = round(int(item['quantity']) * float(item['product_price']), 2)
            item['subtotal'] = subtotal
            cart_total_amount += subtotal

        cart_grand_total = round((cart_total_amount + (cart_total_amount * fee)/100), 2)
        
        request.session['cart_data_obj'] = cart_data_obj

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