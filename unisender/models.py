# -*- coding: utf-8 -*-
# python imports
import logging
import re
from datetime import datetime

# django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from filebrowser.fields import FileBrowseField
# third part imports
from tinymce_4.fields import TinyMCEModelField

from pyunisend import PyUniSend

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^tinymce_4\.fields\.TinyMCEModelField'])
except ImportError:
    pass
# app imports
from error_codes import UNISENDER_COMMON_ERRORS
from settings import UNISENDER_API_KEY, UNISENDER_TEST_MODE

from unisender.managers import (
    UnisenderTagManager, UnisenderFieldManager, UnisenderListManager,
    UnisenderCampaignManager)

test_mode = 1 if UNISENDER_TEST_MODE else 0

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UnisenderModel(models.Model):
    default_error_message = _(u'неизвестная ошибка')

    unisender_id = models.CharField(_(u'unisender id'), max_length=255,
                                    blank=True, null=True)
    last_error = models.CharField(_(u'последняя ошибка'), max_length=255,
                                  blank=True, null=True)
    sync = models.BooleanField(
        _(u'Синхронизированно с Unisender?'), default=False)

    error_dict = UNISENDER_COMMON_ERRORS

    objects = models.Manager()

    def get_last_error(self):
        if self.last_error:
            try:
                return self.error_dict[self.last_error]
            except KeyError:
                return self.last_error
        else:
            return None
    get_last_error.short_description = u'последняя ошибка'

    def get_api(self):
        return PyUniSend(UNISENDER_API_KEY, test_mode=test_mode)

    def log_warning(self, msg, request=None):
        if request:
            messages.warning(request, _(u'Сообщение при синхронизации с unisender: %s' % msg))
        logger.info(unicode(_(u'Сообщение при синхронизации с unisender: %s' % msg)))

    def success_message(self, message, request=None):
        if request:
            messages.success(request, message)
        if UNISENDER_TEST_MODE:
            messages.warning(request, _(u'Внимание включен тестовый режим и никаких изменений в БД unisender не было внесено'))

    def log_error(self, request=None, error=None):
        last_error = error if error else self.get_last_error()
        if request:
            messages.error(
                request,
                _(u'При синхронизации с unisender проиошла ошибка: %s' % last_error))
        logger.error(unicode(_(u'При синхронизации с unisender проиошла ошибка: %s' % last_error)))

    class Meta:
        abstract = True


class Tag(UnisenderModel):
    name = models.CharField(_(u'Метка'), max_length=255)
    unisender = UnisenderTagManager()

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Метка')
        verbose_name_plural = _(u'Метки')


def validate_field_name_field(value):
    if not re.match('[a-zA-Z0-9_]+', value):
        raise ValidationError(
            u'''Название поля может содержать, только символы английского
                алфавита цифры и знак подчеркивания''')

class Field(UnisenderModel):
    TYPE_CHOICES = [
        ('string', _(u'строка')),
        ('text', _(u'одна или несколько строк')),
        ('number', _(u'число')),
        ('bool', _(u'да/нет.')),
    ]
    name = models.CharField(_(u'Поле'), max_length=255,
                            validators=[validate_field_name_field])
    field_type = models.CharField(_(u'Тип поля'), max_length=50,
                                  choices=TYPE_CHOICES,
                                  default=TYPE_CHOICES[0][0])
    visible = models.BooleanField(
        _(u'Является ли поле «видимым» в веб-интерфейсе в таблицах. ?'),
        default=True)
    sort = models.SmallIntegerField(
        _(u'Порядок вывода в в таблицах веб-интерфейса'), default=1,
        help_text=_(u'''Число от 1 до 99, задающее положение поля в
            таблицах веб-интерфейса. Чем меньше число, тем левее выводится поле.
            По умолчанию 1. При совпадении этого числа у разных полей порядок
            не гарантируется.'''))

    unisender = UnisenderFieldManager()

    def _serialize_visible(self):
        return 1 if self.visible else 0

    def create_field(self, request=None):
        '''
        http://www.unisender.com/ru/help/api/createField/
        '''
        api = self.get_api()
        responce = api.createField(
            name=self.name, type=self.field_type,
            is_visible=self._serialize_visible(), view_pos=self.sort)
        result = responce.get('result')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if result:
            self.sync = True
            self.last_error = None
            self.success_message(
                u'Поле %s успешно синхронизировано с unisender' % self.name,
                request=request)
            return result['id']
        if error:
            self.last_error = error
            self.log_error(request)


    def update_field(self, request=None):
        '''
        http://www.unisender.com/ru/help/api/updateField/
        '''
        api = self.get_api()
        responce = api.updateField(
            id=self.unisender_id, name=self.name,
            type=self.field_type, is_visible=self._serialize_visible(),
            view_pos=self.sort)
        result = responce.get('id')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if result:
            self.sync = True
            self.last_error = None
            self.success_message(
                u'Поле %s успешно синхронизировано с unisender' % self.name,
                request=request)
            return result
        if error:
            self.last_error = error
            self.log_error(request)

    def delete_field(self, request=None):
        '''
        http://www.unisender.com/ru/help/api/deleteField/
        '''
        api = self.get_api()
        responce = api.deleteField(id=self.unisender_id)
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if error:
            self.log_error(request, error)
            self.log_warning(
                _(u'''Не удалось удалить поле из БД unisender, вам необходимо
                      удалить его самостоятельно'''), request)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Поле')
        verbose_name_plural = _(u'Поля')


class SubscribeList(UnisenderModel):
    title = models.CharField(
        _(u'Список рассылки'), max_length=255, unique=True)
    before_subscribe_url = models.CharField(
        _(u'URL для редиректа на страницу "перед подпиской". '), max_length=255,
        blank=True, null=True, help_text=_(
            u'''Обычно на этой странице показывается сообщение, что подписчику
            надо перейти по ссылке подтверждения для активации подписки.
            В этот URL можно добавлять поля подстановки - например,
            вы можете идентифицировать подписчика по email-адресу,
            подставив сюда email - либо по коду подписчика в своей базе данных,
            сохраняя код в дополнительное поле и подставляя его в этот URL.'''))
    after_subscribe_url = models.CharField(
        _(u'URL для редиректа на страницу "после подписки"'), max_length=255,
        blank=True, null=True, help_text=_(
            u'''Обычно на этой странице показывается сообщение,
            что подписка успешно активирована. В этот URL можно добавлять поля
            подстановки - например, вы можете идентифицировать подписчика
            по email-адресу, подставив сюда email - либо по коду подписчика
            в своей базе данных, сохраняя код в дополнительное поле и подставляя
            его в этот URL.'''))

    unisender = UnisenderListManager()

    def delete_list(self, request=None):
        '''
        http://www.unisender.com/ru/help/api/deleteList/
        '''
        api = self.get_api()
        responce = api.deleteList(list_id=self.unisender_id)
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if error:
            self.log_error(request, error)
            self.log_warning(
                _(u'''Не удалось удалить список рассылки из БД unisender,
                      вам необходимо удалить его самостоятельно'''), request)
            return
        self.success_message(
            _(u'Список рассылки успешно удален из БД unisender'), request)

    def update_list(self, request=None):
        '''
        http://www.unisender.com/ru/help/api/updateList/
        '''
        api = self.get_api()
        responce = api.updateList(
            title=self.title.encode('utf-8'), list_id=self.unisender_id,
            before_subscribe_url=self.before_subscribe_url,
            after_subscribe_url=self.after_subscribe_url)
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if error:
            self.last_error = error
            self.log_error(request)
            return
        self.sync = True
        self.last_error = None
        self.success_message(_(
            u'''Список рассылки %s успешно синхронизирован
                с unisender''' % self.title),
            request=request)

    def create_list(self, request=None):
        '''
        создает список
        http://www.unisender.com/ru/help/api/createList/
        '''
        api = self.get_api()
        responce = api.createList(
            title=self.title.encode('utf-8'),
            before_subscribe_url=self.before_subscribe_url,
            after_subscribe_url=self.after_subscribe_url)
        result = responce.get('result')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if result:
            self.sync = True
            self.last_error = None
            self.success_message(_(
                u'''Список рассылки %s успешно синхронизирован
                    с unisender''' % self.title),
                request=request)
            return result['id']
        if error:
            self.last_error = error
            self.log_error(request)

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        ordering = ('title',)
        verbose_name = _(u'Список рассылки')
        verbose_name_plural = _(u'Списки рассылки')


class OptinEmail(UnisenderModel):
    sender_name = models.CharField(
        _(u'Имя отправителя'), max_length=255, help_text=_(
            u'Произвольная строка, не совпадающая с e-mail адресом'))
    sender_email = models.CharField(
        _(u'E-mail адрес отправителя.'), max_length=255, help_text=_(
            u'''Этот e-mail должен быть проверен (для этого надо создать вручную
                хотя бы одно письмо с этим обратным адресом через веб-интерфейс,
                затем нажать на ссылку "отправьте запрос подтверждения"
                и перейти по ссылке из письма).'''))
    subject = models.CharField(_(u'Тема письма'), max_length=255)
    body = TinyMCEModelField(
        _(u'Текст письма в формате HTML'), help_text=_(
            u'''Текст обязательно должен включать в себя как минимум одну ссылку
                с атрибутом href="{{ConfirmUrl}}"'''), default=_(
                u'<a href="{{ConfirmUrl}}">Подписаться на рассылку</a>'))
    list_id = models.OneToOneField(SubscribeList)

    def update_optin_email(self, request=None):
        '''
        создает список
        http://www.unisender.com/ru/help/api/updateOptInEmail/
        '''
        api = self.get_api()
        responce = api.updateOptInEmail(
            sender_name=self.sender_name.encode('utf-8'),
            sender_email=self.sender_email.encode('utf-8'),
            subject=self.subject.encode('utf-8'),
            body=self.body.encode('utf-8'), list_id=self.list_id.unisender_id)
        result = responce.get('result')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if result == {}:
            self.sync = True
            self.last_error = None
            self.success_message(_(u'Сообщение успешно синхронизировано'),
                request=request)
            return
        if error:
            self.last_error = error
            self.log_error(request)

    def __unicode__(self):
        return unicode(self.list_id.title)

    class Meta:
        verbose_name = _(u'Письмо приглашение для рассылки')
        verbose_name_plural = _(u'Письмо приглашение для рассылки')

class Subscriber(UnisenderModel):
    CONTACT_TYPE = [
        ('email', _(u'email')),
        ('phone', _(u'телефон')),
    ]
    DOUBLE_OPTIN_CHOICES = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]
    list_ids = models.ManyToManyField(
        SubscribeList, related_name='subscribers',
        verbose_name=_(u'Списки рассылки'))
    tags = models.ManyToManyField(Tag, related_name='subscribers',
                                  verbose_name=u'Метки', blank=True, null=True)
    contact_type = models.CharField(_(u'Тип контакта'), max_length=50,
                                    choices=CONTACT_TYPE,
                                    default=CONTACT_TYPE[0][0])
    contact = models.CharField(_(u'email/телефон'), max_length=255)
    double_optin = models.CharField(
        _(u'Есть ли подтверждённое согласие подписчика'),
        help_text='''<h2>Если выбрано 0</h2>
                     <div>Подписчик высказал
                     желание подписаться, но ещё не подтвердил подписку.
                     В этом случае подписчику будет отправлено
                     письмо-приглашение подписаться.</div>
                     <h2>Если выбрано 1</h2>
                     <div>У Вас уже есть согласие
                    подписчика. Но при этом для защиты от злоупотреблений есть
                    суточный лимит подписок. Если же он превышен, подписчику
                    высылается письмо с просьбой подтвердить подписку.</div>
                    <h2>Если выбрано 2</h2>
                    <div>Считается, что у Вас согласие подписчика
                    уже есть, но в случае превышения лимита мы возвращаем код
                    ошибки too_many_double_optins.</div>
                    <h2>Если выбрано 3</h2>
                    <div>Считается, что у Вас согласие подписчика
                    уже есть, но в случае превышения лимита подписчик
                    добавляется со статусом «новый».</div> ''',
                    choices=DOUBLE_OPTIN_CHOICES, default=DOUBLE_OPTIN_CHOICES[1][0], max_length=2)

    def serialize_fields(self):
        result = {}
        if self.contact_type == 'email':
            result['email'] = self.contact
        else:
            result['phone'] = self.contact
        fields = self.fields.all().prefetch_related('field').select_related(
            'value', 'field__name')
        result.update({item.field.name: item.value.encode('utf-8') for item in fields})
        return result

    def serialize_list_id(self):
        return ','.join(str(x) for x in self.list_ids.all().values_list(
            'unisender_id', flat=True))

    def serialize_tags(self):
        return u','.join(str(x) for x in self.tags.all().values_list(
            'name', flat=True))

    def subscribe(self, request=None):
        '''
        добавить подписчика
        http://www.unisender.com/ru/help/api/subscribe/
        '''
        api = self.get_api()
        responce = api.subscribe(
            fields=self.serialize_fields(),
            list_ids=self.serialize_list_id(), overwrite=1,
            tags=self.serialize_tags(), double_optin=self.double_optin)
        result = responce.get('result')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if result:
            self.sync = True
            self.last_error = None
            self.success_message(_(
                u'''Подписчик %s успешно синхронизирован
                    с unisender''' % self.contact), request=request)
            return result['person_id']
        if error:
           self.last_error = error
           self.log_error(request)

    def unsubscribe(self, request=None):
        '''
        убрать подписчика (по воле подписчика)
        http://www.unisender.com/ru/help/api/unsubscribe/
        '''
        api = self.get_api()
        responce = api.unsubscribe(
            list_ids=self.serialize_list_id(),
            contact_type=self.contact_type, contact=self.contact)
        result = responce.get('result')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if result:
            self.success_message(_(
                u'''Подписчик %s успешно синхронизирован
                    с unisender''' % self.contact), request=request)
            return result['id']
        if error:
            self.last_error = error
            self.log_error(request)

    def exclude(self, request=None, exclude_list=None, show_success_message=None):
        '''
        убрать подписчика
        http://www.unisender.com/ru/help/api/exclude/
        '''
        api = self.get_api()
        list_ids = exclude_list if exclude_list else self.serialize_list_id()
        responce = api.exclude(
            contact=self.contact,
            list_ids=list_ids, contact_type=self.contact_type)
        result = responce.get('result')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if error:
            self.last_error = error
            self.log_error(request)
            return
        if show_success_message:
            self.success_message(
                _(u'Подписчик %s успешно отписан из списков БД unisender' % self.contact),
                request=request)

    def __unicode__(self):
        return unicode(self.contact)

    class Meta:
        ordering = ('contact',)
        verbose_name = _(u'Подписчик')
        verbose_name_plural = _(u'Подписчики')

@receiver(m2m_changed, sender=Subscriber.list_ids.through)
def sync_subscriber_m2m_on_save(sender, instance, action, **kwargs):
    if action == 'pre_clear':
        instance.exclude()
    if action == 'post_add':
        instance.unisender_id = instance.subscribe()


class SubscriberFields(models.Model):
    subscriber = models.ForeignKey(Subscriber, verbose_name=u'подписчик',
                                   related_name='fields')
    field = models.ForeignKey(Field, verbose_name=u'поле')
    value = models.CharField(_(u'Значение'), max_length=255)

    class Meta:
        verbose_name = _(u'дополнительное поле к подписчику')
        verbose_name_plural = _(u'дополнительные поля к подписчику')

@receiver(post_save, sender=SubscriberFields)
def sync_subscriberlist_on_save(sender, instance, created, **kwargs):
    instance.subscriber.subscribe()


class MessageModel(UnisenderModel):

    def delete_message(self, request=None):
        '''
        удалить сообщение
        http://www.unisender.com/ru/help/api/deleteMessage/
        '''
        api = self.get_api()
        responce = api.deleteMessage(message_id=self.unisender_id)
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if error:
            self.last_error = error
            self.log_error(request)
            self.log_warning(
                _(u'''Не удалось сообщение из БД unisender, вам необходимо
                      удалить его самостоятельно'''), request)

    class Meta:
        abstract = True


class EmailMessage(MessageModel):
    LANGUAGES = [
        ('ru', _(u'русский')),
        ('en', _(u'английский')),
        ('it', _(u'итальянский')),
    ]
    TEXT_GENERATE = [
        ('0', _(u'Нет')),
        ('1', _(u'Да')),
    ]
    WRAP_TYPE = [
        ('skip', _(u'не применять')),
        ('right', _(u'выравнивание по правому краю')),
        ('left', _(u'выравнивание по левому краю')),
        ('center', _(u'выравнивание по центру')),
    ]
    sender_name = models.CharField(_(u'Имя отправителя'), max_length=255)
    sender_email = models.CharField(
        _(u'E-mail адрес отправителя'), max_length=255,
        help_text=_(u'''Этот e-mail должен быть проверен (для этого надо создать
                      вручную хотя бы одно письмо с этим обратным адресом через
                      веб-интерфейс, затем нажать на ссылку
                      «отправьте запрос подтверждения» и перейти по ссылке из
                      письма).'''))
    subject = models.CharField(_(u'Тема'), max_length=255)
    body = TinyMCEModelField(_(u'Текст письма в формате HTML'))
    list_id = models.ForeignKey(SubscribeList, verbose_name=u'Список рассылки',
                                related_name='emails',
                                on_delete=models.SET_NULL, null=True)
    tag = models.ForeignKey(
        Tag, related_name='emails', verbose_name=u'Метка', blank=True,
        null=True, on_delete=models.SET_NULL)
    lang = models.CharField(_(u'Язык'), max_length=50,
                            choices=LANGUAGES,
                            default=LANGUAGES[0][0])
    text_body = models.TextField(
        _(u'Текстовый вариант письма'), blank=True, null=True)
    generate_text = models.CharField(_(u'Генерировать текстовую часть письма'),
                                     max_length=50,
                                     choices=TEXT_GENERATE,
                                     default=TEXT_GENERATE[1][0])
    wrap_type = models.CharField(_(u'Выравнивание текста сообщения'),
                                 max_length=50,
                                 choices=WRAP_TYPE,
                                 default=WRAP_TYPE[0][0])
    categories = models.CharField(
        _(u'Категории письма'), max_length=255, blank=True, null=True,
        help_text=_(u'Категории письма, перечисленные в текстовом виде через'
                     u' запятую'))
    series_day = models.PositiveSmallIntegerField(
        _(u'День отправки для автоматически рассылаемого письма'),
        help_text='''Если задан, то это должно быть целое положительное число,
                     задающее день отправки письма по отношению к дню подписки.
                     У дня номер 1 специальный смысл: если указан этот день,
                     то письмо будет отправлено в момент подписки,
                     и значение series_time будет проигнорировано
                     (т.к. заранее неизвестно время подписки).''',
        blank=True, null=True)
    series_time = models.TimeField(
        _(u'Время отправки для автоматически рассылаемого письма'),
        default=datetime.now())

    def read_only_body(self):
        return self.body

    read_only_body.allow_tags = True

    def create_email_message(self, request=None):
        '''
        создать сообщение электронной почты
        http://www.unisender.com/ru/help/api/createEmailMessage/
        '''
        params = {'sender_name': self.sender_name.encode('utf-8'),
                  'sender_email': self.sender_email,
                  'subject': self.subject.encode('utf-8'),
                  'body': self.body.encode('utf-8'),
                  'list_id': self.list_id.unisender_id,
                  'generate_text': self.generate_text,
                  'tag': self.tag,
                  'lang': self.lang,
                  'wrap_type': self.wrap_type}
        if self.text_body:
            params['text_body'] = self.text_body
        if self.series_day:
            params['series_day'] = self.series_day
        if self.series_time:
            params['series_time'] = self.series_time.strftime('%H:%M')
        if self.categories:
            params['categories'] = self.categories
        attachments = self.attachments.all()

        if attachments:
            attachments_dict = {}
            for item in attachments:
                attachments_dict[item.filename.filename] = ''.join(
                    ''.join(s) for s in tuple(open(item.filename.path_full, 'r')))
            params['attachments'] = attachments_dict
        api = self.get_api()
        responce = api.createEmailMessage(**params)
        result = responce.get('result')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if result:
            self.sync = True
            self.success_message(_(
                u'''Email сообщение %s успешно синхронизировано
                    с unisender''' % self.subject), request=request)
            return result['message_id']
        if error:
            self.last_error = error
            self.log_error(request)

    def __unicode__(self):
        return unicode(self.subject)

    class Meta:
        ordering = ('subject',)
        verbose_name = _(u'Email сообщение')
        verbose_name_plural = _(u'Email сообщениея')


class Attachment(models.Model):
    email_message = models.ForeignKey(
        EmailMessage, verbose_name=u'Сообщение', related_name='attachments')
    filename = FileBrowseField(_(u'Прикрепленный файл'), max_length=255)

    class Meta:
        verbose_name = _(u'Вложение')
        verbose_name_plural = _(u'Вложения')


class SmsMessage(MessageModel):
    # sms
    pass


class Campaign(UnisenderModel):
    TEXT_GENERATE = [
        ('0', _(u'Нет')),
        ('1', _(u'Да')),
    ]
    STATUS_CHOICES = [
        ('scheduled',
         u'рассылка поставлена очередь и будет отправлена, как только наступит '
         u'время'),
        ('censor_hold',
         u'рассмотрена администратором, но отложена для дальнейшей проверки'),
        ('waits_censor', u'рассылка ожидает проверки администратором.'),
        ('waits_schedule',
         u'задача на отправку рассылки запомнена системой и будет обработана'),
        ('declined', u'рассылка отклонена администратором'),
        ('in_progress', u'рассылка выполняется'),
        ('analysed', u'все сообщения отправлены, идёт анализ результатов'),
        ('completed', u'все сообщения отправлены и анализ результатов закончен'),
        ('stopped', u'рассылка поставлена "на паузу"'),
        ('canceled',
         u'рассылка отменена (обычно из-за нехватки денег или по желанию пользователя)'),
    ]

    name = models.CharField(
        _(u'Название рассылки'), max_length=255, blank=True, null=True)
    email_message = models.ForeignKey(
        EmailMessage, verbose_name=u'Сообщение', null=True)
    start_time = models.DateTimeField(
        _(u'Дата и время запуска рассылки'), blank=True, null=True,
        help_text=_(u'Если не указано, то рассылка будет осуществлена немедленно'))
    track_read = models.CharField(
        _(u'отслеживать ли факт прочтения e-mail сообщения'),
        max_length=50,  choices=TEXT_GENERATE, default=TEXT_GENERATE[0][0])
    track_links = models.CharField(
        _(u'отслеживать ли  переходы по ссылкам в e-mail сообщении'),
        max_length=50,
        choices=TEXT_GENERATE,
        default=TEXT_GENERATE[0][0])
    contacts = models.ManyToManyField(
        Subscriber, related_name='campaign', verbose_name=u'Контакты',
        blank=True, null=True)
    track_ga = models.CharField(
        _(u'включить интеграцию с Google Analytics/Яндекс.Метрика. '),
        max_length=50, choices=TEXT_GENERATE, default=TEXT_GENERATE[0][0])
    payment_limit = models.PositiveSmallIntegerField(
        _(u'ограничить бюджет рассылки'), blank=True, null=True)

    status = models.CharField(
        _(u'статус рассылки'), max_length=50, choices=STATUS_CHOICES,
        default=None, blank=True, null=True)
    last_check = models.DateTimeField(
        _(u'Дата и время последней проверки'), blank=True, null=True)
    not_sent = models.PositiveSmallIntegerField(
        _(u'Сообщение еще не было обработано'),
        default=0,
        help_text=_(u'Также этот статус возвращается для отложенных для модерации сообщений'))
    ok_delivered = models.PositiveSmallIntegerField(
        _(u'Сообщение доставлено'), default=0)
    ok_read = models.PositiveSmallIntegerField(
        _(u'Сообщение доставлено и зарегистрировано его прочтение'), default=0)
    ok_spam_folder = models.PositiveSmallIntegerField(
        _(u'Сообщение доставлено, но помещено в папку "спам" получателем'),
        default=0,
        help_text=_(u'К сожалению, редкие почтовые службы сообщают такую информацию, поэтому таких статусов обычно немного'))
    ok_link_visited = models.PositiveSmallIntegerField(
        _(u'Сообщение доставлено, прочитано и выполнен переход по одной из ссылок'),
        default=0)
    ok_unsubscribed = models.PositiveSmallIntegerField(
        _(u'Сообщение доставлено и прочитано, но пользователь отписался по ссылке в письме'),
        default=0)
    err_user_unknown = models.PositiveSmallIntegerField(
        _(u'Адрес не существует, доставка не удалась'), default=0)
    err_user_inactive = models.PositiveSmallIntegerField(
        _(u'Адрес когда-то существовал, но сейчас отключен. Доставка не удалась'),
        default=0)
    err_mailbox_full = models.PositiveSmallIntegerField(
        _(u'Почтовый ящик получателя переполнен'), default=0)
    err_spam_rejected = models.PositiveSmallIntegerField(
        _(u'Письмо отклонено сервером как спам'), default=0)
    err_spam_folder = models.PositiveSmallIntegerField(
        _(u'Письмо помещено в папку со спамом почтовой службой'),
        help_text=_(
            u'К сожалению, редкие почтовые службы сообщают такую информацию, поэтому таких статусов обычно немного'),
        default=0)
    err_delivery_failed = models.PositiveSmallIntegerField(
        _(u'Доставка не удалась по иным причинам'), default=0)
    err_will_retry = models.PositiveSmallIntegerField(
        _(u' Одна или несколько попыток доставки оказались неудачными, но попытки продолжаются'),
        default=0)
    err_resend = models.PositiveSmallIntegerField(
        _(u' Фактически эквивалентен err_will_retry, с некоторыми несущественными внутренними особенностями'),
        default=0)
    err_domain_inactive = models.PositiveSmallIntegerField(
        _(u'Домен не принимает почту или не существует'),
        default=0)
    err_skip_letter = models.PositiveSmallIntegerField(
        _(u'Адресат не является активным - он отключён или заблокирован'),
        default=0)
    err_spam_skipped = models.PositiveSmallIntegerField(
        _(u'Сообщение не отправлено, т.к. большая часть рассылки попала в cпам и остальные письма отправлять не имеет смысла'),
        default=0)
    err_spam_retry = models.PositiveSmallIntegerField(
        _(u'письмо ранее не было отправлено из-за подозрения на спам'),
        help_text=_(
            u'после расследования выяснилось, что всё в порядке и его нужно переотправить'),
        default=0)
    err_unsubscribed = models.PositiveSmallIntegerField(
        _(u'отправка не выполнялась, т.к. адрес, по которому пытались отправить письмо, ранее отписался'),
        help_text=_(
            u'Выделяется по сравнению с err_skip_letter в отдельный случай, чтобы позволить пользователю API пометить этот адрес как отписавшийся и в своей базе данных и больше не отправлять на него'),
        default=0)
    err_src_invalid = models.PositiveSmallIntegerField(
        _(u'неправильный адрес отправителя'),
        help_text=_(
            u'Используется, если "невалидность email-а отправителя" обнаружилась не на стадии приёма задания и проверки параметров, а на более поздней стадии, когда осуществляется детальная проверка того, что нужно отправить'),
        default=0)
    err_dest_invalid = models.PositiveSmallIntegerField(
        _(u'неправильный адрес получателя'),
        help_text=_(
            u'Используется, если "невалидность email-а получателя" обнаружилась не на стадии приёма задания и проверки параметров, а на более поздней стадии, когда осуществляется подробная проверка того, что нужно отправить'),
        default=0)
    err_not_allowed = models.PositiveSmallIntegerField(_
                                                      (u'возможность отправки писем заблокирована'),
                                                       help_text=_(
                                                       u'системой из-за нехватки средств на счету или сотрудниками технической поддержки вручную'),
                                                       default=0)
    err_not_available = models.PositiveSmallIntegerField(
        _(u'адрес, по которому пытались отправить письмо, не является доступным'),
        help_text=_(
            u'(т.е. ранее отправки на него приводили к сообщениям а-ля "адрес не существует" или "блокировка по спаму") Доступность адреса теоретически может быть восстановлена через несколько дней или недель, поэтому можно его не вычёркивать полностью из списка потенциальных адресатов'),
        default=0)
    err_lost = models.PositiveSmallIntegerField(
        _(u'письмо было утеряно из-за сбоя на нашей стороне, и отправитель должен переотправить письмо самостоятельно, т.к. оригинал не сохранился'),
        default=0)
    err_internal = models.PositiveSmallIntegerField(
        _(u'внутренний сбой, при котором переотправка письма отправителем не должна осуществляться'),
        default=0)
    total = models.PositiveSmallIntegerField(_(u'Общее количество обработанных сообщений'),
        default=0)

    unisender = UnisenderCampaignManager()

    def was_send(self):
        if self.status =='completed':
            return True
        return False
    was_send.short_description = u'Рассылка завершена'
    was_send.boolean = True


    def get_error_count(self):
        result = 0
        err_fields = ['err_user_unknown', 'err_user_inactive',
                      'err_mailbox_full', 'err_spam_rejected',
                      'err_spam_folder', 'err_delivery_failed',
                      'err_will_retry', 'err_resend',
                      'err_domain_inactive', 'err_skip_letter',
                      'err_spam_skipped', 'err_spam_retry',
                      'err_unsubscribed', 'err_src_invalid',
                      'err_dest_invalid', 'err_not_allowed',
                      'err_not_available', 'err_lost', 'err_internal', ]
        for item in err_fields:
            result += getattr(self, item, 0)
        return result

    get_error_count.short_description = u'Общее количество ошибок'

    def get_success_count(self):
        result = 0
        err_fields = ['ok_delivered', 'ok_read',
                      'ok_spam_folder', 'ok_link_visited', 'ok_unsubscribed', ]
        for item in err_fields:
            result += getattr(self, item, 0)
        return result

    get_success_count.short_description = u'Общее количество успешно доставленных сообщений'

    def get_campaign_status(self, request=None):
        '''
        http://www.unisender.com/ru/help/api/getCampaignStatus/
        '''
        api = self.get_api()
        responce = api.getCampaignStatus(campaign_id=self.unisender_id)
        result = responce.get('result')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if result:
            self.last_error = None
            self.status = result.get('status')
            self.creation_time = result.get('creation_time')
            self.start_time = result.get('start_time')
            self.success_message(_(
                u'''Статус рассылки %s успешно синхронизирован
                    с unisender''' % self.name), request=request)
            return result
        if error:
            self.last_error = error
            self.log_error(request)

    def get_campaign_agregate_status(self, request=None):
        '''
        http://www.unisender.com/ru/help/api/getCampaignAggregateStats/
        '''
        api = self.get_api()
        responce = api.getCampaignAggregateStats(campaign_id=self.unisender_id)
        result = responce.get('result')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if result:
            self.last_error = None
            self.total = result.get('total')
            data = result.get('data')
            for item in data.keys():
                if hasattr(self, item):
                    setattr(self, item, data[item])
            self.success_message(_(
                u'''Информация о рассылке %s успешно синхронизирована
                    с unisender''' % self.name), request=request)
            return result
        if error:
            self.last_error = error
            self.log_error(request)

    def get_visited_links(self, request=None):
        '''
        http://www.unisender.com/ru/help/api/getVisitedLinks/
        '''
        params = {'campaign_id': self.unisender_id,
                  'group': '1',}
        api = self.get_api()
        responce = api.getVisitedLinks(**params)
        result = responce.get('result')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if result:
            self.last_error = None
            self.sync = True
            fields = result['fields']
            data = result.get('data')
            if data:
                self.visited_links.all().delete()
                for link_list in data:
                    result_dict = {
                    item[0]:item[1] for item in zip(fields, link_list)}
                    link, created = VisitedLink.objects.get_or_create(
                        campaign=self, email=result_dict['email'],
                        url=result_dict['url'], ip=result_dict.get('ip'))
                    request_time = result_dict.get('request_time')
                    if request_time:
                        link.request_time = datetime.strptime(request_time,
                            '%Y-%m-%d %H:%M:%S')
                    if created:
                        link.count = result_dict.get('count')
                    else:
                        link.count += int(result_dict.get('count', '0'))
                    link.save()
                self.success_message(
                    _(u'Информация о посещенных ссылках получена от unisender'),
                    request=request)
        if error:
            self.last_error = error
            self.log_error(request)

    def serrialize_contacts(self):
        return ','.join(str(x) for x in self.contacts.all().values_list(
            'contact', flat=True))

    def create_campaign(self, request=None):
        '''
        http://www.unisender.com/ru/help/api/createCampaign/
        '''
        params = {'message_id': self.email_message.unisender_id,
                  'track_read': self.track_read,
                  'track_links': self.track_links,
                  'contacts': self.serrialize_contacts(),
                  'defer': 1,
                  'track_ga': self.track_ga}
        if self.start_time:
            params['start_time'] = self.start_time
        if self.payment_limit:
            params['payment_limit'] = self.payment_limit

        api = self.get_api()
        responce = api.createCampaign(**params)
        result = responce.get('result')
        error = responce.get('error')
        warning = responce.get('warning')
        if warning:
            self.log_warning(warning, request)
        if result:
            self.last_error = None
            self.sync = True
            self.success_message(_(
                u'''Рассылка создана и %s успешно синхронизирована
                    с unisender''' % self.name), request=request)
            return result['campaign_id']
        if error:
            self.last_error = error
            self.log_error(request)

    def __unicode__(self):
        name = self.pk
        if self.name:
            name = self.name
        elif self.unisender_id:
            name = self.unisender_id
        return unicode(name)

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Рассылка')
        verbose_name_plural = _(u'Рассылки')


class VisitedLink(models.Model):
    campaign = models.ForeignKey(
        Campaign, verbose_name=u'Рассылка', related_name='visited_links')
    email = models.CharField(_(u'email'), max_length=255, blank=True)
    ip = models.CharField(_(u'ip пользователя'), max_length=255, blank=True)
    url = models.CharField(_(u'url'), max_length=255, blank=True)
    request_time = models.DateTimeField(
        _(u'Время посещения'), blank=True, null=True)
    count = models.SmallIntegerField(
        _(u'Количетсво посещений'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Посещенная ссылка')
        verbose_name_plural = _(u'Посещенные ссылки')
# TODO
#  http://www.unisender.com/ru/help/api/sendEmail/
#  http://www.unisender.com/ru/help/api/checkEmail/
