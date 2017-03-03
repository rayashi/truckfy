from rest_framework import viewsets

from apps.personas.serializers import *
from apps.shared.permission import *
from apps.shared.pagination import *


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrRead,)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = StandardResultsSetPagination


class TruckViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrRead,)
    queryset = Truck.objects.all()
    serializer_class = TruckModelSerializer
    pagination_class = StandardResultsSetPagination
