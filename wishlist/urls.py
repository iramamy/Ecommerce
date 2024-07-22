from django.urls import path
from . import views


urlpatterns = [
    path("", views.wishlist, name='wishlist'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
]