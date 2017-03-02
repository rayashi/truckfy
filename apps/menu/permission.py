from rest_framework import permissions

from apps.menu.serializers import *
from apps.personas.models import *


class DishOwnerOrRead(permissions.BasePermission):

    #Permissoes de alteracoes de objetos
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            try:
                if isinstance(obj, Dish):
                    return obj.truck.user == request.user
            except Dish.DoesNotExist:
                pass
            return False

    #Permissoes de criacao de objetos
    def has_permission(self, request, view):
        if view.request.method in ['POST'] and request.data:

            if view.serializer_class == DishSerializer:
                try:
                    return request.data.get('truck') == request.user.truck.id
                except Truck.DoesNotExist:
                    return False
            return True
        else:
            return True
