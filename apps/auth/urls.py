from rest_framework.authtoken import views as rest_views
from django.conf.urls import url


urlpatterns = [
    url(r'^login/', rest_views.obtain_auth_token)
]
