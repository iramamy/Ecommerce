from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name='register'),
    path("signin/", views.signin, name='signin'),
    path("signout/", views.signout, name='signout'),

    # Dashboard
    path("dashboard/", views.dashboard_view, name='dashboard'),

    path("dashboard-order/", views.dashboard_order, name='dashboard_order'),


    # User order detail
    path("order-detail/<int:orderID>/", views.order_detail, name='order_detail'),

    # Address
    path("address/", views.address, name='address'),

    # Change addresses
    path("billing-address/", views.billing_address, name='billing_address'),
    path("shipping-address/", views.shipping_address, name='shipping_address'),

    # User profile
    path("profile/", views.user_profile, name='user_profile'),
    path("edit-profile/", views.edit_profile, name='edit_profile'),

    # Save edited profile
    path("save-profile/", views.save_edited_profile, name='save_edited_profile'),
    


]