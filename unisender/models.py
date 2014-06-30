# -*- coding: utf-8 -*-
# python imports
from datetime import datetime

# django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _

# third part imports
from tinymce_4.fields import TinyMCEModelField

# app imports
from error_codes import UNISENDER_COMMON_ERRORS
from unisender.managers import (
    UnisenderTagManager, UnisenderFIeldManager, UnisenderListManager,
    SubscriberListManager, CampaignManager)


class UnisenderModel(models.Model):
    unisender_id = models.CharField(_(u'unisender id'), max_length=255,
                                    blank=True, null=True)
    last_error = models.CharField(_(u'последняя ошибка'), max_length=255,
                                  blank=True, null=True)
    sync = models.BooleanField(
        _(u'Синхронизированно с Unisender?'), default=True)

    error_dict = UNISENDER_COMMON_ERRORS

    def get_last_error(self):
        if self.last_error:
            return self.error_dict.get(self.last_error, _(u'неизвестная ошибка'))
        else:
            return None

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


class Fields(UnisenderModel):
    TYPE_CHOICES = [
        ('string', _(u'строка')),
        ('text', _(u'одна или несколько строк')),
        ('number', _(u'число')),
        ('bool', _(u'да/нет.')),
    ]
    name = models.CharField(_(u'Поле'), max_length=255)
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

    unisender = UnisenderFIeldManager()

    def _create_field(self):
        '''
        http://www.unisender.com/ru/help/api/createField/
        '''
        pass

    def _update_field(self):
        '''
        http://www.unisender.com/ru/help/api/updateField/
        '''
        pass

    def _delete_field(self):
        '''
        http://www.unisender.com/ru/help/api/deleteField/
        '''
        pass

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

    def delete_list(self):
        '''
        http://www.unisender.com/ru/help/api/deleteList/
        '''
        pass

    def update_list(self):
        '''
        http://www.unisender.com/ru/help/api/updateList/
        '''
        pass

    def create_list(self):
        '''
        http://www.unisender.com/ru/help/api/createList/
        '''
        pass

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        ordering = ('title',)
        verbose_name = _(u'Список рассылки')
        verbose_name_plural = _(u'Списки рассылки')


class Subscriber(UnisenderModel):
    CONTACT_TYPE = [
        ('email', _(u'email')),
        ('phone', _(u'телефон')),
    ]
    list_ids = models.ManyToManyField(
        SubscribeList, related_name='subscribers',
        verbose_name=_(u'Списки рассылки'))
    tags = models.ManyToManyField(Tag, related_name='subscribers',
                                  verbose_name=u'Метки')
    contact_type = models.CharField(_(u'Тип контакта'), max_length=50,
                                    choices=CONTACT_TYPE,
                                    default=CONTACT_TYPE[0][0])
    contact = models.CharField(_(u'email/телефон'), max_length=255)
    double_optin = models.SmallIntegerField(
        _(u'Число от 0 до 3 - есть ли подтверждённое согласие подписчика'),
        help_text='''Если 0, то мы считаем, что подписчик только высказал
                     желание подписаться, но ещё не подтвердил подписку.
                     В этом случае подписчику будет отправлено
                     письмо-приглашение подписаться. Текст письма будет взят из
                     свойств первого списка из list_ids. Кстати, текст можно
                     поменять с помощью метода updateOptInEmail или через
                     веб-интерфейс.

                    Если 1, то мы считаем, что у Вас уже есть согласие
                    подписчика. Но при этом для защиты от злоупотреблений есть
                    суточный лимит подписок. Если он не превышен, мы не посылаем
                    письмо-приглашение. Если же он превышен, подписчику
                    высылается письмо с просьбой подтвердить подписку. Текст
                    этого письма можно настроить для каждого списка с помощью
                    метода updateOptInEmail или через веб-интерфейс.
                    Лимиты мы согласовываем в индивидуальном порядке.

                    Если 2, то также считается, что у Вас согласие подписчика
                    уже есть, но в случае превышения лимита мы возвращаем код
                    ошибки too_many_double_optins.

                    Если 3, то также считается, что у Вас согласие подписчика
                    уже есть, но в случае превышения лимита подписчик
                    добавляется со статусом «новый». ''', default=1)

    unisender = SubscriberListManager()

    def serialize_fields(self):
        pass

    def subscribe(self):
        '''
        добавить подписчика
        http://www.unisender.com/ru/help/api/subscribe/
        '''
        pass

    def unsubscribe(self, list_ids):
        '''
        убрать подписчика
        http://www.unisender.com/ru/help/api/unsubscribe/
        '''
        pass

    def exclude(self, list_ids):
        '''
        убрать подписчика
        http://www.unisender.com/ru/help/api/exclude/
        '''
        pass

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        ordering = ('title',)
        verbose_name = _(u'Подписчик')
        verbose_name_plural = _(u'Подписчики')


class SubscriberFields(models.Model):
    subscriber = models.ForeignKey(Subscriber, verbose_name=u'подписчик',
                                   related_name='fields')
    field = models.ForeignKey(Fields, verbose_name=u'поле')
    value = models.CharField(_(u'Значение'), max_length=255)

    class Meta:
        verbose_name = _(u'дополнительное поле к подписчику')
        verbose_name_plural = _(u'дополнительные поля к подписчику')


class MessageModel(UnisenderModel):

    def delete_message(self):
        '''
        удалить сообщение
        http://www.unisender.com/ru/help/api/deleteMessage/
        '''
        pass

    class Meta:
        abstract = True


class EmailMessage(MessageModel):
    # TODO attachments
    LANGUAGES = [
        ('ru', _(u'русский')),
        ('en', _(u'английский')),
        ('it', _(u'иткальянский')),
    ]
    TEXT_GENERATE = [
        (0, _(u'Нет')),
        (1, _(u'Да')),
    ]
    WRAP_TYPE = [
        ('skip', _(u'не применять')),
        ('right', _(u'выравнивание по правому краю')),
        ('left', _(u'выравнивание по левому краю')),
        ('center', _(u'выравнивание по центру')),
    ]
    sender_name = models.CharField(_(u'Имя отправителя'), max_length=255)
    subject = models.CharField(_(u'Тема'), max_length=255)
    body = TinyMCEModelField(_(u'Текст письма в формате HTML'))
    list_id = models.ForeignKey(SubscribeList, verbose_name=u'Список рассылки',
                                related_name='emails')
    tags = models.ManyToManyField(Tag, related_name='emails',
                                  verbose_name=u'Метки')
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
                                 choices=TEXT_GENERATE,
                                 default=TEXT_GENERATE[1][0])
    categories = models.CharField(
        _(u'Категории письма'), max_length=255, blank=True, null=True)
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

    def create_email_message(self):
        '''
        создать сообщение электронной почты
        http://www.unisender.com/ru/help/api/createEmailMessage/
        '''
        pass

    def __unicode__(self):
        return unicode(self.subject)

    class Meta:
        ordering = ('subject',)
        verbose_name = _(u'Email сообщение')
        verbose_name_plural = _(u'Email сообщениея')


class SmsMessage(MessageModel):
    # sms
    pass


class Campaign(UnisenderModel):
    TEXT_GENERATE = [
        (0, _(u'Нет')),
        (1, _(u'Да')),
    ]

    name = models.CharField(_(u'Название рассылки'), max_length=255)
    email_message = models.ForeignKey(EmailMessage, verbose_name=u'Сообщение')
    start_time = models.DateTimeField(
        _(u'Дата и время запуска рассылки'), blank=True, null=True)
    timezone = models.CharField(_(u'часовой пояс'), max_length=255)
    track_read = models.CharField(
        _(u'отслеживать ли факт прочтения e-mail сообщения'),
        max_length=50,  choices=TEXT_GENERATE, default=TEXT_GENERATE[0][0])
    track_links = models.CharField(
        _(u'отслеживать ли  переходы по ссылкам в e-mail сообщении'),
            max_length=50,
        choices=TEXT_GENERATE,
        default=TEXT_GENERATE[0][0])
    contacts = models.CharField(
        _(u'email-адреса (или телефоны для sms-сообщений)'),
        help_text='''Если этот аргумент отсутствует, то отправка будет
                     осуществлена по всем контактам списка, для которого
                     составлено сообщение (возможно, с учётом сегментации
                     по меткам). Если аргумент contacts присутствует,
                     то во внимание будут приняты только те контакты, которые
                     входят в список, а остальные будут проигнорированы. ''',
        blank=True, null=True)
    track_ga = models.CharField(
        _(u'включить интеграцию с Google Analytics/Яндекс.Метрика. '),
        max_length=50, choices=TEXT_GENERATE, default=TEXT_GENERATE[0][0])
    payment_limit = models.PositiveSmallIntegerField(
        _(u'ограничить бюджет рассылки'), blank=True, null=True)

    unisender = CampaignManager()

    def create_campaign(self):
        '''
        http://www.unisender.com/ru/help/api/createCampaign/
        '''
        pass

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Рассылка')
        verbose_name_plural = _(u'Рассылки')


class CampaignStatus(UnisenderModel):
    STATUS_CHOICES = [
        ('scheduled',
         u'рассылка поставлена очередь и будет отправлена, как только наступит '
         u'время'),
        ('censor_hold',
         u'рассмотрена администратором, но отложена для дальнейшей проверки'),
        ('waits_censor', u'рассылка ожидает проверки администратором.'),
        ('waits_schedule',
         u'задача на отправку рассылки запомнена системой и будет обработана'),
        ('declined', u'рассылка отклонена администратором')
        ('in_progress', u'рассылка выполняется')
        ('analysed', u'все сообщения отправлены, идёт анализ результатов')
        ('completed', u'все сообщения отправлены и анализ результатов закончен')
        ('stopped', u'рассылка поставлена "на паузу"')
        ('canceled',
         u'рассылка отменена (обычно из-за нехватки денег или по желанию пользователя)')
    ]
    campaign = models.ForeignKey(EmailMessage, verbose_name=u'Рассылка')
    status = models.CharField(
        _(u'статус рассылки'), max_length=50, choices=STATUS_CHOICES,
        default=None, blank=True, null=True)
    start_time = models.DateTimeField(
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
        help_text=_(u'К сожалению, редкие почтовые службы сообщают такую информацию, поэтому таких статусов обычно немного'),
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
        help_text=_(u'после расследования выяснилось, что всё в порядке и его нужно переотправить'),
        default=0)
    err_unsubscribed = models.PositiveSmallIntegerField(
        _(u'отправка не выполнялась, т.к. адрес, по которому пытались отправить письмо, ранее отписался'),
        help_text=_(u'Выделяется по сравнению с err_skip_letter в отдельный случай, чтобы позволить пользователю API пометить этот адрес как отписавшийся и в своей базе данных и больше не отправлять на него'),
        default=0)
    err_src_invalid = models.PositiveSmallIntegerField(
        _(u'неправильный адрес отправителя'),
        help_text=_(u'Используется, если "невалидность email-а отправителя" обнаружилась не на стадии приёма задания и проверки параметров, а на более поздней стадии, когда осуществляется детальная проверка того, что нужно отправить'),
        default=0)
    err_dest_invalid = models.PositiveSmallIntegerField(
        _(u'неправильный адрес получателя'),
        help_text=_(u'Используется, если "невалидность email-а получателя" обнаружилась не на стадии приёма задания и проверки параметров, а на более поздней стадии, когда осуществляется подробная проверка того, что нужно отправить'),
        default=0)
    err_not_allowed = models.PositiveSmallIntegerField(_
        (u'возможность отправки писем заблокирована'),
        help_text=_(u'системой из-за нехватки средств на счету или сотрудниками технической поддержки вручную'),
        default=0)
    err_not_available = models.PositiveSmallIntegerField(
        _(u'адрес, по которому пытались отправить письмо, не является доступным'),
        help_text=_(u'(т.е. ранее отправки на него приводили к сообщениям а-ля "адрес не существует" или "блокировка по спаму") Доступность адреса теоретически может быть восстановлена через несколько дней или недель, поэтому можно его не вычёркивать полностью из списка потенциальных адресатов'),
        default=0)
    err_lost = models.PositiveSmallIntegerField(
        _(u'письмо было утеряно из-за сбоя на нашей стороне, и отправитель должен переотправить письмо самостоятельно, т.к. оригинал не сохранился'),
        default=0)
    err_internal = models.PositiveSmallIntegerField(
        _(u'внутренний сбой, при котором переотправка письма отправителем не должна осуществляться'),
        default=0)

    def get_campaign_status(self):
        '''
        http://www.unisender.com/ru/help/api/getCampaignStatus/
        '''
        pass

    def get_campaign_agregate_stats(self):
        '''
        http://www.unisender.com/ru/help/api/getCampaignAggregateStats/
        '''
        pass

    def get_visited_links(self):
        '''
        http://www.unisender.com/ru/help/api/getVisitedLinks/
        '''
        pass

    def __unicode__(self):
        return unicode(self.campaign)

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Статусы рассылки')
        verbose_name_plural = _(u'Статусы рассылки')

# TODO
#  http://www.unisender.com/ru/help/api/sendEmail/
#  http://www.unisender.com/ru/help/api/checkEmail/