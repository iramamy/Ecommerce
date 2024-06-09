from django.urls import path
from core import views

urlpatterns = [
    path("", views.index, name='home'),
    path("products/", views.product_list, name='product_list'),
    path("categories/", views.category_list, name='category_list'),
    path(
        "categories/<category_name>/<cid>/", 
        views.product_per_category, 
        name='product_per_category'
        ),
]
