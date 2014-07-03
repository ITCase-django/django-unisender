# -*- coding: utf-8 -*-

from django.db.models.signals import pre_save,pre_delete
from django.dispatch import receiver
from unisender.models import Field


@receiver(pre_save, sender=Field)
def sync_field_on_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.unisender_id:
            instance.update_field()
        else:
            instance.unisender_id = instance.create_field()
    else:
        instance.unisender_id = instance.create_field()


@receiver(pre_delete, sender=Field)
def sync_field_on_delete(sender, instance, **kwargs):
    instance.delete_field()
