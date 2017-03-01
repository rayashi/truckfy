from rest_framework import viewsets

from apps.menu.serializers import *
from apps.shared.permission import *
from apps.shared.pagination import *


class DishViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrRead,)
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    pagination_class = StandardResultsSetPagination

