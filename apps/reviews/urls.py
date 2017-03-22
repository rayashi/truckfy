from django.conf.urls import url

from apps.reviews import views

urlpatterns = [
    url(r'^make-review', views.make_review)
]
