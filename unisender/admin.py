# -*- coding: utf-8 -*-
from django.contrib import admin

from unisender.models import (
    Tag, Field, SubscribeList, Subscriber, SubscriberFields,
    EmailMessage, SmsMessage, Campaign, CampaignStatus)

unisender_fieldsets = [
    [u'Unisender', {
     'fields': ['unisender_id', 'sync']
     }]
]


class UnisenderAdmin(admin.ModelAdmin):
    readonly_fields = ['unisender_id', 'sync']

    fieldsets = unisender_fieldsets


class TagAdmin(UnisenderAdmin):
    fieldsets = unisender_fieldsets + [[u'Метка', {'fields': ['name', ]}]]

    list_display = ('__unicode__', 'unisender_id', 'sync', )
    list_display_links = ('__unicode__', )
    search_fields = ['name', ]

admin.site.register(Tag, TagAdmin)


class FieldAdmin(UnisenderAdmin):
    fieldsets = unisender_fieldsets + [[u'Поле', {
        'fields': ['name', 'field_type', 'visible', 'sort']
    }]]

    list_display = ('__unicode__', 'unisender_id', 'sync', 'field_type',
                    'visible', 'sort')
    list_display_links = ('__unicode__', )
    search_fields = ['name', ]
    list_editable = ('field_type', 'visible', 'sort')

admin.site.register(Field, FieldAdmin)


class SubscribeListAdmin(UnisenderAdmin):
    fieldsets = unisender_fieldsets + [
        (u'Список рассылки', {
            'fields': ['title', 'before_subscribe_url', 'after_subscribe_url']
        })]

    list_display = ('__unicode__', 'unisender_id', 'sync',
                    'before_subscribe_url', 'after_subscribe_url')
    list_display_links = ('__unicode__', )
    search_fields = ['title', ]

admin.site.register(SubscribeList, SubscribeListAdmin)


class SubscriberFieldsInline(admin.TabularInline):
    model = SubscriberFields
    extra = 0


class SubscriberAdmin(UnisenderAdmin):
    # TODO form validation
    fieldsets = unisender_fieldsets + [
        (u'Подписчик', {
            'fields': ['list_ids', 'tags', 'contact_type', 'contact',
                       'double_optin']
        })]

    list_display = ('__unicode__', 'contact_type', 'unisender_id', 'sync')
    list_display_links = ('__unicode__', )
    search_fields = ['contact', ]
    filter_horizontal = ['list_ids', 'tags']
    inlines = [SubscriberFieldsInline]

admin.site.register(Subscriber, SubscriberAdmin)


class EmailMessageAdmin(UnisenderAdmin):
    fieldsets = unisender_fieldsets + [
        (u'Сообщение', {
            'fields': ['sender_name', 'subject', 'body', 'list_id', 'tags',
                       'lang', 'text_body', 'generate_text', 'wrap_type',
                       'categories',]
        }),
        (u'Автоматическая отправка', {
            'fields': ['series_day', 'series_time', ]
        })]

    list_display = (
        '__unicode__', 'sender_name', 'subject', 'unisender_id', 'sync')
    list_display_links = ('__unicode__', )
    search_fields = ['sender_name', 'subject', 'body', ]
    filter_horizontal = ['tags']

admin.site.register(EmailMessage, EmailMessageAdmin)


admin.site.register(SmsMessage)


class CampaignAdmin(UnisenderAdmin):
    fieldsets = unisender_fieldsets + [
        (u'Рассылка', {
            'fields': ['name', 'email_message', 'start_time',
                       'track_read', 'track_links', 'contacts', 'track_ga',
                       'payment_limit', ]
        })]

    list_display = (
        '__unicode__', 'name', 'email_message', 'unisender_id', 'sync')
    list_display_links = ('__unicode__', )
    search_fields = ['name', 'contacts', ]

    filter_horizontal = ['contacts']

admin.site.register(Campaign, CampaignAdmin)


class CampaignStatusAdmin(UnisenderAdmin):
    fieldsets = unisender_fieldsets + [
        (u'Статус', {
            'fields': ['campaign', 'status', 'start_time',]
        }),
        (u'Краткая информация', {
            'fields': ['get_error_count', 'get_success_count' ]
        }),
        (u'Подробная информация', {
            'fields': ['not_sent', 'ok_delivered', 'ok_read',
                       'ok_spam_folder', 'ok_link_visited', 'ok_unsubscribed',
                       'err_user_unknown', 'err_user_inactive',
                       'err_mailbox_full', 'err_spam_rejected',
                       'err_spam_folder', 'err_delivery_failed',
                       'err_will_retry', 'err_resend', 'err_domain_inactive',
                       'err_skip_letter', 'err_spam_retry', 'err_unsubscribed',
                       'err_src_invalid', 'err_dest_invalid', 'err_not_allowed',
                       'err_not_available', 'err_lost', 'err_internal', ]
        })]

    list_display = (
        '__unicode__', 'status', 'campaign', 'get_error_count',
        'get_success_count', 'unisender_id', 'sync')
    list_display_links = ('__unicode__', )
    search_fields = ['campaign', 'status', ]
    readonly_fields = ['get_error_count', 'get_success_count', 'unisender_id', 'sync']
admin.site.register(CampaignStatus, CampaignStatusAdmin)
