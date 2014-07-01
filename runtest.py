#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from django.conf import settings

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
APPS_PATH = os.path.join(PROJECT_DIR, 'itcase')
sys.path.insert(0, APPS_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

settings.configure(DEBUG=True,
                   SITE_ID=1,
                   DATABASES={
                       'default': {
                           'ENGINE': 'django.db.backends.sqlite3',
                       }
                   },
                   INSTALLED_APPS=('django.contrib.auth',
                                   'django.contrib.contenttypes',
                                   'django.contrib.sessions',
                                   'django.contrib.admin',
                                   'unisender',
                                   'tinymce_4'),

                    # List of callables that know how to import templates from various sources.
                    TEMPLATE_LOADERS = (
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                        'django.template.loaders.eggs.Loader',
                    ),
                    TEMPLATE_CONTEXT_PROCESSORS = (
                        'django.contrib.auth.context_processors.auth',
                        'django.core.context_processors.i18n',
                        'django.core.context_processors.media',
                        'django.core.context_processors.static',
                        'django.contrib.messages.context_processors.messages',
                        'django.core.context_processors.request',
                    ),
                   )

from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(['unisender', ])
if failures:
    sys.exit(failures)
