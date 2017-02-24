from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'client', views.ClientViewSet)
router.register(r'truck', views.TruckViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
