from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^near-trucks', views.near_trucks),
    url(r'^checkin', views.truck_checkin)
]
