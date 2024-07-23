from django.urls import path
from . import views


urlpatterns = [
    path("payement/", views.payement, name='payement'),
    path("payment-failder/", views.payement_failed, name='payement_failed'),
    path("payment-completed/", views.payement_completed, name='payement_completed'),
]
 