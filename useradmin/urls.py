from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name='useradmin_dashboard'),
    path("products/", views.products, name='useradmin_products'),
    path("add_products/", views.add_products, name='useradmin_add_products'),
    path("edit_products/<str:pid>/", views.edit_products, name='useradmin_edit_products'),
    path("delete_product/<str:pid>/", views.delete_product, name='useradmin_delete_product'),
    path("orders/", views.admin_orders, name='admin_orders'),
    path("order_detail/<str:orderID>/", views.admin_order_detail, name='admin_order_detail'),

    path(
        "change_order_status/<str:orderID>/",
        views.change_order_status,
        name='change_order_status'
        ),

    path("delete-order/<str:orderID>/", views.delete_order, name='delete_order'),
    path("vendor-page/<str:vendor_name>/<str:vid>/", views.vendor_page, name='vendor_page'),
    path("reviews/", views.reviews, name='reviews'),
    path("settings/", views.settings, name='settings'),
    
]