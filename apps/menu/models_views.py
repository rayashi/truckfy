from rest_framework import viewsets

from apps.shared.pagination import *
from apps.menu.permission import *


class DishViewSet(viewsets.ModelViewSet):
    permission_classes = (DishOwnerOrRead,)
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    pagination_class = StandardResultsSetPagination

