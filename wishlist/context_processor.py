

def wishlist_view(request):

    if 'wishlist_data_obj' in request.session:

        wishlist_data_obj = request.session['wishlist_data_obj']

        context = {
            'wishlist_data': wishlist_data_obj,
            'total_item_wishlist': len(wishlist_data_obj),
        }

        return context

    else:          
        context = {
            'total_item_wishlist': 0,
        }

        return context