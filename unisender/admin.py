# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, url
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from unisender.models import (
    Tag, Field, SubscribeList, Subscriber, SubscriberFields,
    EmailMessage, Campaign)

from unisender.views import GetCampaignStatistic

unisender_fieldsets = [
    [u'Unisender', {
     'fields': ['unisender_id', 'sync', 'get_last_error']
     }]
]


class UnisenderAdmin(admin.ModelAdmin):
    readonly_fields = ['unisender_id', 'sync', 'get_last_error']

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

    actions = ['delete_selected_fields']

    def get_actions(self, request):
        actions = super(FieldAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_selected_fields(self, request, queryset):
        for item in queryset:
            self.delete_model(request, item)
    delete_selected_fields.short_description = u'Удалить выбранные Поля'

    def save_model(self, request, obj, form, change):
        if obj.pk:
            if obj.unisender_id:
                obj.update_field(request)
            else:
                obj.unisender_id = obj.create_field(request)
        else:
            obj.unisender_id = obj.create_field(request)
        obj.save()

    def delete_model(self, request, obj):
        obj.delete_field(request)
        obj.delete()

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

    def save_model(self, request, obj, form, change):
        if obj.unisender_id:
            if obj.pk:
                obj.update_list(request)
            else:
                obj.unisender_id = obj.create_list(request)
        else:
            obj.unisender_id = obj.create_list(request)
        obj.save()

    actions = ['delete_selected_subscribe_list']

    def get_actions(self, request):
        actions = super(SubscribeListAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_selected_subscribe_list(self, request, queryset):
        for item in queryset:
            self.delete_model(request, item)
    delete_selected_subscribe_list.short_description = u'Удалить выбранные Списки подписчиков'

    def delete_model(self, request, obj):
        obj.delete_list(request)
        obj.delete()

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

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(SubscriberAdmin, self).get_readonly_fields(request, obj=None)
        if obj and obj.sync:
            readonly_fields += ('contact', 'contact_type')
        return readonly_fields

    def save_model(self, request, obj, form, change):
        obj.save()
        if not obj.unisender_id:
            obj.unisender_id = obj.subscribe(request)
        obj.save()

    actions = ['delete_selected_subscribers']

    def get_actions(self, request):
        actions = super(SubscriberAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_selected_subscribers(self, request, queryset):
        for item in queryset:
            self.delete_model(request, item)
    delete_selected_subscribers.short_description = u'Удалить выбранных Подписчиков'

    def delete_model(self, request, obj):
        obj.exclude(request)
        obj.delete()

admin.site.register(Subscriber, SubscriberAdmin)

auto_send_fieldset = [[u'Автоматическая отправка', {
            'fields': ['series_day', 'series_time', ]
        }]]

class EmailMessageAdmin(UnisenderAdmin):
    fieldsets = unisender_fieldsets + [
        [u'Сообщение', {
            'fields': ['sender_name', 'sender_email', 'subject', 'body', 'list_id',
                       'lang', 'text_body', 'generate_text', 'wrap_type',
                       'categories', 'tag']
        }]] + auto_send_fieldset

    list_display = (
        '__unicode__', 'sender_name', 'subject', 'unisender_id', 'sync')
    list_display_links = ('__unicode__', )
    search_fields = ['sender_name', 'subject', 'body', ]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.sync:
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result += ['get_last_error']
            result += ['read_only_body']
            return result
        return super(EmailMessageAdmin, self).get_readonly_fields(request, obj=None)

    def get_fieldsets(self, request, obj=None):
        field_sets = super(EmailMessageAdmin, self).get_fieldsets(request, obj=None)
        if obj and obj.unisender_id:
            field_sets = unisender_fieldsets + [
            [u'Сообщение', {
                'fields': ['sender_name', 'sender_email', 'subject',
                           'read_only_body', 'list_id', 'lang', 'text_body',
                           'generate_text', 'wrap_type', 'categories', 'tag']
            }]] + auto_send_fieldset
        return field_sets

    def save_model(self, request, obj, form, change):
        if not obj.unisender_id:
            obj.unisender_id = obj.create_email_message(request)
        obj.save()

    actions = ['delete_selected_emails']

    def get_actions(self, request):
        actions = super(EmailMessageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_selected_emails(self, request, queryset):
        for item in queryset:
            self.delete_model(request, item)
    delete_selected_emails.short_description = u'Удалить выбранные сообщения электронной почты'

    def delete_model(self, request, obj):
        obj.delete_message(request)
        obj.delete()

admin.site.register(EmailMessage, EmailMessageAdmin)


# admin.site.register(SmsMessage)


class CampaignAdmin(UnisenderAdmin):
    change_form_template = 'unisender/admin/change_campaign.html'
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

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.sync:
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result += ['get_last_error', 'get_error_count', 'get_success_count']
            return result
        return super(CampaignAdmin, self).get_readonly_fields(request, obj=None)

    def get_fieldsets(self, request, obj=None):
        field_sets = super(
            CampaignAdmin, self).get_fieldsets(request, obj=None)
        if obj and obj.sync:
            field_sets = field_sets + [
                (u'Статус', {
                 'fields': ['status', 'start_time', ]
                 }),
                (u'Краткая информация', {
                 'fields': ['get_error_count', 'get_success_count']
                 }),
                (u'Подробная информация', {
                 'fields': ['not_sent', 'ok_delivered', 'ok_read',
                            'ok_spam_folder', 'ok_link_visited',
                            'ok_unsubscribed',
                            'err_user_unknown', 'err_user_inactive',
                            'err_mailbox_full', 'err_spam_rejected',
                            'err_spam_folder', 'err_delivery_failed',
                            'err_will_retry', 'err_resend', 'err_not_allowed',
                            'err_domain_inactive', 'err_unsubscribed',
                            'err_skip_letter', 'err_spam_retry',
                            'err_src_invalid', 'err_dest_invalid',
                            'err_not_available', 'err_lost', 'err_internal', ]
                 })]
        return field_sets

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        campaign = Campaign.objects.get(pk=object_id)
        if campaign.sync:
            extra_context['show_get_statistic_button'] = True
            extra_context['pk'] = object_id
        return super(CampaignAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)


    def get_urls(self):
        urls = super(CampaignAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'(?P<pk>\d+)/get_statistic/$',
             self.admin_site.admin_view(GetCampaignStatistic.as_view()),
             name='unisender_campaign_get_statistic',
             ),
        )
        return my_urls + urls


    def save_model(self, request, obj, form, change):
        obj.save()
        if not obj.unisender_id:
            obj.unisender_id = obj.create_campaign(request)
        obj.save()

    actions = ['delete_selected_campaigns']

    def get_actions(self, request):
        actions = super(CampaignAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_selected_campaigns(self, request, queryset):
        for item in queryset:
            self.delete_model(request, item)
    delete_selected_campaigns.short_description = u'Удалить выбранные Поля'

    def delete_model(self, request, obj):
        messages.warning(
            request, _(u'Объект был удален из БД сайта, но остался в БД unisender вам необходимо удалить его самостоятельно оттуда'))
        obj.delete()

admin.site.register(Campaign, CampaignAdmin)
