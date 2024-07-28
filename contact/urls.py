from django.urls import path
from . import views


urlpatterns = [
    path("", views.contact_us, name='contact_us'),
    path("about/", views.about_us, name='about_us'),
]
 