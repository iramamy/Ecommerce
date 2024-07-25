from django.urls import path
from . import views


urlpatterns = [
    path("place-order/", views.place_order, name='place_order'),

    path("payment/", views.payment, name='payment'),
    path("payment-failed/", views.payment_failed, name='payment_failed'),
    path("payment-completed/", views.payment_completed, name='payment_completed'),
]
 