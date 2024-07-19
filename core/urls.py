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
    path("products/<category_name>/<pid>/", views.product_detail, name='product_detail'),

    # Tags
    path('products-tag/<tag_slug>/', views.tag_list, name='tag_list'),

    # Search
    path('search/', views.search_product, name='search_product'),

    # Filter
    path('filter-product/', views.filter_product, name='filter_product'),
    
    # Add review
    path('add-review/<str:pid>', views.add_review, name='add_review'),

]
