from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^near-trucks', views.near_trucks),
    url(r'^checkin', views.truck_checkin),
    url(r'^checkout', views.truck_checkout),
    url(r'^actived-checkin', views.actived_checkin)
]
