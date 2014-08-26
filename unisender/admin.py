# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, url
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError

from unisender.models import (
    Tag, Field, SubscribeList, Subscriber, SubscriberFields,
    EmailMessage, Campaign, Attachment, VisitedLink, OptinEmail)

from unisender.unisender_urls import (
    EMAIL_MESSAGES_LIST, EMAIL_MESSAGES_DETAIL, TAG_LIST, FIELD_LIST,
    CAMPAIGN_LIST, CAMPAIGN_DETAIL, SUBSCRIBELIST_LIST, SUBSCRIBELIST_DETAIL
)

from unisender.views import (
    GetCampaignStatistic, GetTags, GetFields, GetLists, GetCampaigns
)

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
    change_list_template = 'unisender/admin/change_tag_list.html'

    def get_urls(self):
        urls = super(TagAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r'get_tags/$',
                               self.admin_site.admin_view(GetTags.as_view()),
                               name='unisender_get_tags',
                               ),
                           )
        return my_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['unisender_site'] = TAG_LIST
        return super(TagAdmin, self).changelist_view(request,
                                                     extra_context=extra_context)

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

    change_list_template = 'unisender/admin/change_field_list.html'

    def get_urls(self):
        urls = super(FieldAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r'get_fields/$',
                               self.admin_site.admin_view(GetFields.as_view()),
                               name='unisender_get_fields',
                               ),
                           )
        return my_urls + urls

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

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['unisender_site'] = FIELD_LIST
        return super(FieldAdmin, self).changelist_view(request,
                                                       extra_context=extra_context)

admin.site.register(Field, FieldAdmin)


class OptinEmailInline(admin.StackedInline):
    model = OptinEmail
    can_delete = False
    readonly_fields = ['unisender_id', 'sync', 'get_last_error']
    fieldsets = [[u'Unisender', {
                 'fields': ['sync', 'get_last_error']
                 }],
                 (u'Письмо', {
                  'fields': ['sender_name', 'sender_email', 'subject', 'body',]
                  })]

    # def save_model(self, request, obj, form, change):

class SubscribeListAdmin(UnisenderAdmin):
    fieldsets = unisender_fieldsets + [
        (u'Список рассылки', {
            'fields': ['title', 'before_subscribe_url', 'after_subscribe_url']
        })]

    list_display = ('__unicode__', 'unisender_id', 'sync',
                    'before_subscribe_url', 'after_subscribe_url')
    list_display_links = ('__unicode__', )
    search_fields = ['title', ]
    change_list_template = 'unisender/admin/change_subscriber_list_list.html'
    change_form_template = 'unisender/admin/change_subscriber_list_detail.html'
    inlines = [OptinEmailInline]

    def get_urls(self):
        urls = super(SubscribeListAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r'get_lists/$',
                               self.admin_site.admin_view(GetLists.as_view()),
                               name='unisender_get_lists',
                               ),
                           )
        return my_urls + urls

    def save_model(self, request, obj, form, change):
        if obj.unisender_id:
            if obj.pk:
                obj.update_list(request)
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

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['unisender_site'] = SUBSCRIBELIST_LIST
        return super(SubscribeListAdmin, self).changelist_view(request,
                                                               extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        instance = self.model.objects.get(pk=object_id)
        if instance.unisender_id:
            extra_context['unisender_site'] =\
                SUBSCRIBELIST_DETAIL + instance.unisender_id
        self.inlines = [OptinEmailInline, ]
        return super(SubscribeListAdmin, self).change_view(
            request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(SubscribeListAdmin, self).add_view(
            request, form_url, extra_context)

    def save_related(self, request, form, formsets, change):
        super(type(self), self).save_related(request, form, formsets, change)
        if change and formsets[0].queryset:
            instance = formsets[0].queryset[0]
            instance.update_optin_email(request)
            instance.save()

admin.site.register(SubscribeList, SubscribeListAdmin)


class SubscriberFieldsInline(admin.TabularInline):
    model = SubscriberFields
    extra = 0


class SubscriberAdmin(UnisenderAdmin):
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
        readonly_fields = super(SubscriberAdmin, self).get_readonly_fields(
            request, obj=obj)
        if obj and obj.sync:
            readonly_fields += ['contact', 'contact_type']
        else:
            # save and add another button behavior
            readonly_fields = list(set(readonly_fields))
            if 'contact' in readonly_fields:
                readonly_fields.remove('contact')
            if 'contact_type' in readonly_fields:
                readonly_fields.remove('contact_type')

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


class EmailMessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmailMessageForm, self).__init__(*args, **kwargs)
        if not self.instance.unisender_id:
            self.fields['list_id'].required = True


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


class AttachmentInlineReadOnly(AttachmentInline):
    can_delete = False

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        result = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        result.remove('id')
        return result


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
    change_list_template = 'unisender/admin/change_emailmessage_list.html'
    change_form_template = 'unisender/admin/change_emailmessage.html'
    form = EmailMessageForm

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
        field_sets = super(
            EmailMessageAdmin, self).get_fieldsets(request, obj=None)
        if obj and obj.unisender_id:
            field_sets = unisender_fieldsets + [
                [u'Сообщение', {
                 'fields': ['sender_name', 'sender_email', 'subject',
                            'read_only_body', 'list_id', 'lang', 'text_body',
                            'generate_text', 'wrap_type', 'categories', 'tag']
                 }]] + auto_send_fieldset
        return field_sets

    def response_add(self, request, obj):
        if not obj.unisender_id:
            obj.unisender_id = obj.create_email_message(request)
        obj.save()
        return super(EmailMessageAdmin, self).response_add(request, obj)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

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

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = [AttachmentInline, ]
        return super(EmailMessageAdmin, self).add_view(
            request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [AttachmentInlineReadOnly, ]
        extra_context = extra_context or {}
        instance = self.model.objects.get(pk=object_id)
        if instance.unisender_id:
            extra_context['unisender_site'] = \
                EMAIL_MESSAGES_DETAIL + instance.unisender_id
        return super(EmailMessageAdmin, self).change_view(
            request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['unisender_site'] = EMAIL_MESSAGES_LIST
        return super(EmailMessageAdmin, self).changelist_view(request,
                                                              extra_context=extra_context)

admin.site.register(EmailMessage, EmailMessageAdmin)


# admin.site.register(SmsMessage)


class CampaignAdminForm(forms.ModelForm):

    def clean_contacts(self):
        email_message = self.cleaned_data.get('email_message', None)
        if not email_message:
            return self.cleaned_data['contacts']
        if self.cleaned_data['contacts'] or (email_message and email_message.list_id):
            return self.cleaned_data['contacts']
        else:
            raise ValidationError(
                u'''У выбранного сообщения отсутствует список контактов,
                    вам необходимо выбрать контакты которым будет осуществлена рассылка''')

    def __init__(self, *args, **kwargs):
        super(CampaignAdminForm, self).__init__(*args, **kwargs)
        if not self.instance.unisender_id:
            self.fields['name'].required = True
            self.fields['email_message'].required = True


class CampaignVisitedLinksInline(admin.TabularInline):
    model = VisitedLink
    extra = 0
    can_delete = False
    fields = ('email', 'ip', 'url', 'request_time', 'count')

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        result = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        result.remove('id')
        return result


class CampaignAdmin(UnisenderAdmin):
    change_form_template = 'unisender/admin/change_campaign.html'
    fieldsets = unisender_fieldsets + [
        (u'Рассылка', {
            'fields': ['name', 'email_message', 'start_time',
                       'track_read', 'track_links', 'track_ga',
                       'payment_limit', ]
        },),
        (u'Контакты', {
            'fields': ['contacts',],
            'description': '''Если этот аргумент отсутствует, то отправка будет
                     осуществлена по всем контактам списка, для которого
                     составлено сообщение. В противном случае во внимание будут приняты
                     только те контакты, которые
                     входят в список, а остальные будут проигнорированы. '''
        },)]

    list_display = (
        '__unicode__', 'email_message', 'unisender_id', 'sync', 'was_send',
        'status')
    list_display_links = ('__unicode__',  'email_message', 'unisender_id')
    search_fields = ['name', 'contacts', ]
    filter_horizontal = ['contacts']
    change_list_template = 'unisender/admin/change_campaign_list.html'
    inlines = [CampaignVisitedLinksInline, ]

    form = CampaignAdminForm

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.sync:
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result += [
                'get_last_error', 'get_error_count', 'get_success_count']
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
        instance = self.model.objects.get(pk=object_id)
        if instance.unisender_id:
            extra_context['unisender_site'] =\
                CAMPAIGN_DETAIL + instance.unisender_id
        if campaign.sync:
            extra_context['show_get_statistic_button'] = True
            extra_context['pk'] = object_id
        return super(CampaignAdmin, self).change_view(request, object_id,
                                                      form_url, extra_context=extra_context)

    def get_urls(self):
        urls = super(CampaignAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r'(?P<pk>\d+)/get_statistic/$',
                               self.admin_site.admin_view(
                               GetCampaignStatistic.as_view()),
                               name='unisender_campaign_get_statistic',
                               ),
                           url(r'get_campaigns/$',
                               self.admin_site.admin_view(
                                   GetCampaigns.as_view()),
                               name='unisender_get_campaigns',
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

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['unisender_site'] = CAMPAIGN_LIST
        return super(CampaignAdmin, self).changelist_view(request,
                                                          extra_context=extra_context)

admin.site.register(Campaign, CampaignAdmin)
