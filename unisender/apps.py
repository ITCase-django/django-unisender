# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UnisenderConfig(AppConfig):
    name = 'unisender'
    verbose_name = _(u'Рассылка е-mail')

    # def ready(self):
    #     pass
