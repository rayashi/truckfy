# -*- coding: utf-8 -*-
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver

from apps.reviews.models import *


@receiver(pre_delete, sender=Review)
def client_deleted(sender, instance, **kwargs):
    instance.truck.review_amount -= 1
    instance.truck.save()



