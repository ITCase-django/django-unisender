#     # -*- coding: utf-8 -*-

from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from unisender.models import Subscriber, SubscriberFields

@receiver(m2m_changed, sender=Subscriber.list_ids.through)
def sync_subscriber_m2m_on_save(sender, instance, action, **kwargs):
    if action == 'pre_clear':
        instance.exclude()
    if action == 'post_add':
        instance.unisender_id = instance.subscribe()

@receiver(post_save, sender=SubscriberFields)
def sync_subscriberlist_on_save(sender, instance, created, **kwargs):
    instance.subscriber.subscribe()
