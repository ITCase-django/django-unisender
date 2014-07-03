# -*- coding: utf-8 -*-
from django.conf import settings

UNISENDER_API_KEY = getattr(settings, 'UNISENDER_API_KEY', None)

UNISENDER_METHOD = getattr(settings, 'UNISENDER_METHOD', 'POST')

UNISENDER_TEST_MODE = getattr(settings, 'UNISENDER_TEST_MODE', False)
