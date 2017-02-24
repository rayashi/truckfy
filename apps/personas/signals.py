# -*- coding: utf-8 -*-
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver

from apps.personas.models import Client, Truck


@receiver(pre_delete, sender=Client)
def client_deleted(sender, instance, **kwargs):
    if instance.avatar:
        instance.avatar.delete()


@receiver(pre_delete, sender=Truck)
def truck_deleted(sender, instance, **kwargs):
    if instance.avatar:
        instance.avatar.delete()
