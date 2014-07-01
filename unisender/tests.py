# -*- coding: utf-8 -*-
from django.test import TestCase

from mock import patch

from unisender.models import Tag
from unisender.managers import UnisenderTagManager


class UnisenderTagManagerTestCase(TestCase):

    def setUp(self):
        with patch('unisender.managers.UnisenderTagManager.get_tags') as self.manager:
            self.manager.get_tags.return_value = {
                "result": [
                    {"id": 123, "name": "test 1 "},
                    {"id": 456, "name": "test 2"}
                ]
            }

    def test__get_tags(self):
        # simple test
        tags = self.manager.get_tags()
        resulted_tags = {
            "result": [
                {"id": 123, "name": "test 1 "},
                {"id": 456, "name": "test 2"}
            ]
        }
        self.assertEquals(tags, resulted_tags)

    def get_and_update_tags(self):
        pass
