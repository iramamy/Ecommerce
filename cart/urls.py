from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_view, name='cart'),

    # Add to cart
    path("add-to-cart/", views.add_to_cart, name='add_to_cart'),
    
    # Delete from cart
    path("delete-from-cart/", views.delete_from_cart, name='delete_from_cart'),

]