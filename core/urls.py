from django.urls import path
from core import views

urlpatterns = [

    # Home
    path("", views.index, name='home'),
    path("products/", views.product_list, name='product_list'),

    # category
    path("categories/", views.category_list, name='category_list'),
    path(
        "categories/<category_name>/<cid>/", 
        views.product_per_category, 
        name='product_per_category'
        ),

    # Vendor
    path("vendor/", views.vendor_list, name='vendor_list'),
    path("vendor/<vendor_name>/<vid>/", views.vendor_detail, name='vendor_detail'),

    # Product detail
    path("product/<category_name>/<pid>/", views.product_detail, name='product_detail'),

]
