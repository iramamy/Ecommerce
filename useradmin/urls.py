from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name='useradmin_dashboard'),
    path("products/", views.products, name='useradmin_products'),
    path("add_products/", views.add_products, name='useradmin_add_products'),
]