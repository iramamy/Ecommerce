from django.urls import path
from . import views


urlpatterns = [
    path("", views.wishlist, name='wishlist'),

    # Add to wishlist
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),

    # Remove wishlist
    path('delete-from-wishlist/', views.delete_from_wishlist, name='delete_from_wishlist'),
]
