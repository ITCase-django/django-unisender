# -*- coding: utf-8 -*-
from django.db import models

from pyunisend import PyUniSend
from settings import UNISENDER_API_KEY


class UnisenderManager(models.Manager):

    api = PyUniSend(UNISENDER_API_KEY)


class UnisenderTagManager(UnisenderManager):

    def get_tags(self):
        '''
        Возвращает результат выполнения команды getTags:
        http://www.unisender.com/ru/help/api/getTags/
        '''
        return self.api.getTags()

    def get_and_update_tags(self):
        '''
        Выполняет команду getTags и обновляет значения в БД:
        http://www.unisender.com/ru/help/api/getTags/
        '''
        tags = self.get_tags()
        result = tags.get('result')
        error = tags.get('error')
        warning = tags.get('warning')
        if result:
            for item in tags['result']:
                self.model.objects.get_or_create(
                    name=item['name'], unisender_id=item['id'])
        if error:
            # TODO last errors
            pass
        if warning:
            # TODO last warnings
            pass


class UnisenderFieldManager(UnisenderManager):

    def get_fields(self):
        '''
        Возвращает результат выполнения команды getFields:
        http://www.unisender.com/ru/help/api/getFields/
        '''
        return self.api.getFields()

    def get_and_update_fields(self):
        '''
        Выполняет команду getFields и обновляет значения в БД:
        http://www.unisender.com/ru/help/api/getFields/
        '''
        fields = self.get_fields()
        result = fields.get('result')
        error = fields.get('error')
        warning = fields.get('warning')
        if result:
            for item in fields['result']:
                visible = True if item['is_visible'] == 1 else 0
                self.model.objects.get_or_create(
                    name=item['name'], unisender_id=item['id'], visible=visible,
                    field_type=item['type'], sort=item['view_pos'])
        if error:
            # TODO last errors
            pass
        if warning:
            # TODO last warnings
            pass

class UnisenderListManager(UnisenderManager):

    def get_lists(self):
        '''
        Возвращает результат выполнения команды getLists:
        http://www.unisender.com/ru/help/api/getLists/
        '''
        return self.api.getLists()

    def get_and_update_lists(self):
        '''
        Выполняет команду getLists и обновляет значения в БД:
        http://www.unisender.com/ru/help/api/getLists/
        '''
        lists = self.get_lists()
        result = lists.get('result')
        error = lists.get('error')
        warning = lists.get('warning')
        if result:
            for item in lists['result']:
                self.model.objects.get_or_create(
                    title=item['title'], unisender_id=item['id'])
        if error:
            # TODO last errors
            pass
        if warning:
            # TODO last warnings
            pass


class UnisenderCampaignManager(UnisenderManager):

    def get_campaings(self, from_arg=None, to_arg=None):
        '''
        Возвращает результат выполнения команды getCampaigns:
        http://www.unisender.com/ru/help/api/getCampaigns/
        '''
        params = {'from': from_arg, 'to': to_arg}
        return self.api.getCampaigns(params=params)
