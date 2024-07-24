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

]