from rest_framework import permissions
from apps.personas.models import *


class AdminOrRead(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False


class IsTruck(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return not not request.user.truck
        except Truck.DoesNotExist:
            return False


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return not not request.user.client
        except Client.DoesNotExist:
            return False
