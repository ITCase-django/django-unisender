#     # -*- coding: utf-8 -*-

from django.db.models.signals import pre_save, pre_delete, post_save, m2m_changed
from django.dispatch import receiver
from unisender.models import (
    SubscribeList, Subscriber, EmailMessage, Campaign)

@receiver(m2m_changed, sender=Subscriber.list_ids.through)
def sync_subscriber_m2m_on_save(sender, instance, action, **kwargs):
    if action == 'pre_clear':
        instance.exclude()
    if action == 'post_add':
        instance.unisender_id = instance.subscribe()

# @receiver(pre_save, sender=EmailMessage)
# def sync_email_message_on_save(sender, instance, **kwargs):
#     if not instance.unisender_id:
#         instance.unisender_id = instance.create_email_message()


# @receiver(m2m_changed, sender=Campaign.contacts.through)
# def sync_campaign_on_save(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         instance.unisender_id = instance.create_campaign()
#         instance.save()
