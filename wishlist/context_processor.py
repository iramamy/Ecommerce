from .models import WishList

def wishlist_view(request):

    if 'wishlist_data_obj' in request.session:
        del request.session['wishlist_data_obj']

    if request.user.is_authenticated:
        try:
            wishlist_items = WishList.objects.filter(
                user=request.user
            )

            wishlist_data_obj = {}
            for item in wishlist_items:

                wishlist_data_obj[f"{item.product.pid}"] = {
                    'product_title': str(item.product.title),
                    'quantity': float(item.quantity),
                    'product_price': float(item.product.price),
                    'image': str(item.product.image.url),
                    'category': str(item.product.category),
                    'subtotal': float(item.product.price * item.quantity)
                }

            request.session['wishlist_data_obj'] = wishlist_data_obj

        except WishList.DoesNotExist:
            wishlist_items = None

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
