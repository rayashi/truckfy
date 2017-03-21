from rest_framework.authtoken import views as rest_views
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login', rest_views.obtain_auth_token),
    url(r'^user-authenticated', views.get_user_authenticated)
]
