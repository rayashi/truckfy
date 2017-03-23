# -*- coding: utf-8 -*-
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Avg

from apps.reviews.models import *


@receiver(pre_delete, sender=Review)
def client_deleted(sender, instance, **kwargs):
    instance.truck.review_amount = instance.truck.review_set.count()
    instance.truck.review_rate = instance.truck.review_set.all().aggregate(Avg('rate')).get('rate__avg')
    instance.truck.save()



