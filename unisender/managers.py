# -*- coding: utf-8 -*-
import logging

from django.db import models
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from pyunisend import PyUniSend
from settings import UNISENDER_API_KEY, UNISENDER_TEST_MODE

from error_codes import UNISENDER_COMMON_ERRORS

test_mode = 1 if UNISENDER_TEST_MODE else 0

logger = logging.getLogger(__name__)

class UnisenderManager(models.Manager):

    api = PyUniSend(UNISENDER_API_KEY, test_mode=test_mode)

    def log_warning(self, msg, request=None):
        if request:
            messages.warning(request, _(u'Сообщение при синхронизации с unisender: %s' % msg))
        logger.info(unicode(_(u'Сообщение при синхронизации с unisender: %s' % msg)))

    def success_message(self, message, request=None):
        if request:
            messages.success(request, message)

    def log_error(self, error, request=None):
        if request:
            messages.error(
                request,
                _(u'При синхронизации с unisender проиошла ошибка: %s' % error))
        logger.error(unicode(_(u'При синхронизации с unisender проиошла ошибка: %s' % error)))


class UnisenderTagManager(UnisenderManager):

    def get_tags(self):
        '''
        Возвращает результат выполнения команды getTags:
        http://www.unisender.com/ru/help/api/getTags/
        '''
        return self.api.getTags()

    def get_and_update_tags(self, request=None):
        '''
        Выполняет команду getTags и обновляет значения в БД:
        http://www.unisender.com/ru/help/api/getTags/
        '''
        tags = self.get_tags()
        result = tags.get('result', [])
        error = tags.get('error')
        warning = tags.get('warning')
        for item in result:
            tag, created = self.model.objects.get_or_create(name=item['name'])
            tag.unisender_id = int(item['id'])
            tag.sync = True
            tag.save()
        self.success_message(
            _(u'%s меток получено от unisender') % len(result),
            request=request)
        if error:
            error_msg = UNISENDER_COMMON_ERRORS.get(tags.get('code'), error)
            self.log_error(error_msg, request)
        if warning:
            self.log_warning(warning, request)


class UnisenderFieldManager(UnisenderManager):

    def get_fields(self):
        '''
        Возвращает результат выполнения команды getFields:
        http://www.unisender.com/ru/help/api/getFields/
        '''
        return self.api.getFields()

    def get_and_update_fields(self, request=None):
        '''
        Выполняет команду getFields и обновляет значения в БД:
        http://www.unisender.com/ru/help/api/getFields/
        '''
        fields = self.get_fields()
        result = fields.get('result', [])
        error = fields.get('error')
        warning = fields.get('warning')
        for item in result:
            field, create = self.model.objects.get_or_create(name=item['name'])
            field.unisender_id = item['id']
            field.sync = True
            field.visible = True if item['is_visible'] == 1 else False
            field.field_type = item['type']
            field.sort = item['view_pos']
            field.save()
        self.success_message(
            _(u'%s полей получено от unisender') % len(result),
            request=request)
        if error:
            error_msg = UNISENDER_COMMON_ERRORS.get(fields.get('code'), error)
            self.log_error(error_msg, request)
        if warning:
            self.log_warning(warning, request)

class UnisenderListManager(UnisenderManager):

    def get_lists(self):
        '''
        Возвращает результат выполнения команды getLists:
        http://www.unisender.com/ru/help/api/getLists/
        '''
        return self.api.getLists()

    def get_and_update_lists(self, request=None):
        '''
        Выполняет команду getLists и обновляет значения в БД:
        http://www.unisender.com/ru/help/api/getLists/
        '''
        lists = self.get_lists()
        result = lists.get('result', [])
        error = lists.get('error')
        warning = lists.get('warning')
        for item in result:
            tag, created = self.model.objects.get_or_create(title=item['title'])
            tag.unisender_id = int(item['id'])
            tag.sync = True
            tag.save()
        self.success_message(
            _(u'%s списков получено от unisender') % len(result),
            request=request)
        if error:
            error_msg = UNISENDER_COMMON_ERRORS.get(lists.get('code'), error)
            self.log_error(error_msg, request)
        if warning:
            self.log_warning(warning, request)


class UnisenderCampaignManager(UnisenderManager):

    def get_campaigns(self, from_arg=None, to_arg=None):
        '''
        Возвращает результат выполнения команды getCampaigns:
        http://www.unisender.com/ru/help/api/getCampaigns/
        '''
        params = {'from': from_arg, 'to': to_arg}
        return self.api.getCampaigns(params=params)

    def get_and_update_campaigns(self, request=None, from_arg=None, to_arg=None):
        '''
        Выполняет команду getCampaigns и обновляет значения в БД:
         http://www.unisender.com/ru/help/api/getCampaigns/
        '''
        campaigns = self.get_campaigns()
        result = campaigns.get('result', [])
        error = campaigns.get('error')
        warning = campaigns.get('warning')
        for item in result:
            tag, created = self.model.objects.get_or_create(
                unisender_id=int(item['id']))
            tag.sync = True
            tag.save()
        self.success_message(
            _(u'%s рассылок получено от unisender') % len(result),
            request=request)
        if error:
            error_msg = UNISENDER_COMMON_ERRORS.get(campaigns.get('code'), error)
            self.log_error(error_msg, request)
        if warning:
            self.log_warning(warning, request)
