from django.urls import path
from . import views


urlpatterns = [
    path("payement/", views.payement, name='payement'),
    path("payment-failed/", views.payment_failed, name='payment_failed'),
    path("payment-completed/", views.payment_completed, name='payment_completed'),
]
 