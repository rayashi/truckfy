
from rest_framework import routers
from apps.menu import models_views as menu_views
from apps.personas import models_views as personas_views

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'client', personas_views.ClientViewSet)
router.register(r'truck', personas_views.TruckViewSet)
router.register(r'dish', menu_views.DishViewSet)
