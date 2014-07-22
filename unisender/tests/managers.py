# -*- coding: utf-8 -*-
from django.test import TestCase

from mock import patch

from unisender.models import Tag, Field, SubscribeList, Campaign


class TagManagerTestCase(TestCase):

    tag_result = {
        'result': [
        {'id': 1, 'name': 'test 1'},
        {'id': 2, 'name': 'test 2'}
        ]
    }

    def setUp(self):
        self.manager = Tag.unisender
        with patch('unisender.managers.UnisenderManager.api') as mock:
            self.manager.api = mock.return_value
            self.manager.api.getTags.return_value = self.tag_result

    def test__get_tags(self):
        # simple test
        tags = Tag.unisender.get_tags()
        resulted_tags = {
            'result': [
                {'id': 1, 'name': 'test 1'},
                {'id': 2, 'name': 'test 2'}
            ]
        }
        self.assertEquals(tags, resulted_tags)

    def test__get_and_update_tags(self):
        tag_1 = Tag.objects.create(name='test 1')
        self.assertFalse(tag_1.sync)
        self.manager.get_and_update_tags()
        tag_1 = Tag.objects.get(unisender_id=1)
        self.assertTrue(tag_1.sync)
        tag_2 = Tag.objects.get(unisender_id=2)
        self.assertEquals(tag_2.name, 'test 2')
        self.assertTrue(tag_2.sync)


class FieldManagerTestCase(TestCase):

    field_result = {
        'result': [
        {'id': 1, 'name': 'test 1', 'type':
         'string', 'is_visible': 1, 'view_pos': 1},
        {'id': 2, 'name': 'test 2', 'type':
         'text', 'is_visible': 1, 'view_pos': 3}
        ]
    }

    def setUp(self):
        self.manager = Field.unisender
        with patch('unisender.managers.UnisenderManager.api') as mock:
            self.manager.api = mock.return_value
            self.manager.api.getFields.return_value = self.field_result

    def test__get_fields(self):
        # simple test
        fields = self.manager.get_fields()
        resulted_fields = {
            'result': [
                {'id': 1, 'name': 'test 1', 'type':
                 'string', 'is_visible': 1, 'view_pos': 1},
                {'id': 2, 'name': 'test 2', 'type':
                 'text', 'is_visible': 1, 'view_pos': 3}
            ]
        }
        self.assertEquals(fields, resulted_fields)

    def test__get_and_update_fields(self):
        Field.objects.create(
            name='test 1', field_type='string', sort=3)
        self.manager.get_and_update_fields()
        field_1 = Field.objects.get(name='test 1')
        self.assertEquals(field_1.field_type, 'string')
        self.assertEquals(field_1.sort, 1)
        self.assertTrue(field_1.sync)
        self.assertTrue(field_1.visible)

        field_2 = Field.objects.get(name='test 2')
        self.assertEquals(field_2.field_type, 'text')
        self.assertTrue(field_2.sync)
        self.assertTrue(field_2.visible)
        self.assertEquals(field_2.sort, 3)


class ListManagerTestCase(TestCase):

    list_get_result = {
        'result': [
            {'id': 1, 'title': 'test 1'},
            {'id': 2, 'title': 'test 2'},
        ]
    }

    def setUp(self):
        self.manager = SubscribeList.unisender
        with patch('unisender.managers.UnisenderManager.api') as mock:
            self.manager.api = mock.return_value
            self.manager.api.getLists.return_value = self.list_get_result

    def test__get_subscribe_lists(self):
        # simple test
        subscribe_list = self.manager.get_lists()
        resulted_list = {
            'result': [
                {'id': 1, 'title': 'test 1'},
                {'id': 2, 'title': 'test 2'}
            ]
        }
        self.assertEquals(subscribe_list, resulted_list)

    def test__get_and_update_subscribe_lists(self):
        list_1 = SubscribeList.objects.create(title='test 1')
        self.assertFalse(list_1.sync)
        self.manager.get_and_update_lists()
        list_1 = SubscribeList.objects.get(title='test 1')
        self.assertTrue(list_1.sync)
        list_2 = SubscribeList.objects.get(title='test 2')
        self.assertTrue(list_2.sync)


class CampaignManagerTestCase(TestCase):

    list_get_campaings = {
        'result': [
            {'id': 1, 'start_time':
             '2011-08-01 19:30:00', 'status': 'completed'},
            {'id': 2, 'start_time':
                '2011-08-10 19:30:00', 'status': 'analysed'},
        ]
    }

    def setUp(self):
        self.manager = Campaign.unisender
        with patch('unisender.managers.UnisenderManager.api') as mock:
            self.manager.api = mock.return_value
            self.manager.api.getCampaigns.return_value = self.list_get_campaings

    def test__get_campaings(self):
        # simple test
        subscribe_list = self.manager.get_campaigns()
        resulted_list = {
            'result': [
            {'id': 1, 'start_time':
             '2011-08-01 19:30:00', 'status': 'completed'},
            {'id': 2, 'start_time':
                '2011-08-10 19:30:00', 'status': 'analysed'},
            ]
        }
        self.assertEquals(subscribe_list, resulted_list)

    def test__get_campaings_time_filter(self):
        # TODO
        pass
