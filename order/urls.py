from django.urls import path
from . import views


urlpatterns = [
    path("payement/", views.payement, name='payement')
]
 