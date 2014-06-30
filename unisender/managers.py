# -*- coding: utf-8 -*-
from django.db import models


class UnisenderTagManager(models.Manager):

    def get_tags(self):
        '''
        Возвращает результат выполнения команды getTags:
        http://www.unisender.com/ru/help/api/getTags/
        '''
        pass

    def get_and_update_tags(self):
        '''
        Выполняет команду getTags и обновляет значения в БД:
        http://www.unisender.com/ru/help/api/getTags/
        '''
        pass


class UnisenderFIeldManager(models.Manager):

    def get_fields(self):
        '''
        Возвращает результат выполнения команды getFields:
        http://www.unisender.com/ru/help/api/getFields/
        '''
        pass

    def get_and_update_fields(self):
        '''
        Выполняет команду getFields и обновляет значения в БД:
        http://www.unisender.com/ru/help/api/getFields/
        '''
        pass

class UnisenderListManager(models.Manager):

    def get_lists(self):
        '''
        Возвращает результат выполнения команды getLists:
        http://www.unisender.com/ru/help/api/getLists/
        '''
        pass

    def get_and_update_lists(self):
        '''
        Выполняет команду getLists и обновляет значения в БД:
        http://www.unisender.com/ru/help/api/getLists/
        '''
        pass

    def create_list(self):
        '''
        создает список
        http://www.unisender.com/ru/help/api/createList/
        '''
        pass

    def create_list_and_update_db(self):
        '''
        создает список и обновляет БД
        http://www.unisender.com/ru/help/api/createList/
        '''
        pass


class SubscriberListManager(models.Manager):

    def subscribe(self):
        '''
        Возвращает результат выполнения команды subscribe:
        http://www.unisender.com/ru/help/api/subscribe/
        '''
        pass


class CampaignManager(models.Manager):

    def get_campaings(self):
        '''
        Возвращает результат выполнения команды getCampaigns:
        http://www.unisender.com/ru/help/api/getCampaigns/
        '''
        pass

    def get_campaing_status(self):
        '''
        Возвращает результат выполнения команды getCampaigns:
        http://www.unisender.com/ru/help/api/getCampaignStatus/
        '''
        pass
