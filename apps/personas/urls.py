from django.conf.urls import url

from apps.personas import views

urlpatterns = [
    url(r'^truck/register', views.truck_register),
    url(r'^truck/image', views.truck_image),
    url(r'^client/register', views.client_register),
]
