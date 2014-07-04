    # -*- coding: utf-8 -*-

from django.db.models.signals import pre_save, pre_delete, post_save, m2m_changed
from django.dispatch import receiver
from unisender.models import (
    Field, SubscribeList, Subscriber, EmailMessage, Campaign)


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


@receiver(pre_save, sender=SubscribeList)
def sync_subscribe_list_on_save(sender, instance, **kwargs):
    if instance.unisender_id:
        if instance.pk:
            instance.update_list()
        else:
            instance.unisender_id = instance.create_list()
    else:
        instance.unisender_id = instance.create_list()


@receiver(pre_delete, sender=SubscribeList)
def sync_subscribe_list_on_delete(sender, instance, **kwargs):
    instance.delete_list()


@receiver(post_save, sender=Subscriber)
def sync_subscriber_on_save(sender, instance, **kwargs):
    instance.unisender_id = instance.subscribe()


@receiver(m2m_changed, sender=Subscriber.list_ids.through)
def sync_subscriber_m2m_on_save(sender, instance, action, **kwargs):
    if action == 'pre_clear':
        instance.exclude()
    if action == 'post_add':
        instance.unisender_id = instance.subscribe()
        instance.save()


@receiver(pre_save, sender=EmailMessage)
def sync_email_message_on_save(sender, instance, **kwargs):
    if not instance.unisender_id:
        instance.unisender_id = instance.create_email_message()


@receiver(m2m_changed, sender=Campaign.contacts.through)
def sync_campaign_on_save(sender, instance, action, **kwargs):
    if action == 'post_add':
        instance.unisender_id = instance.create_campaign()
        instance.save()
