# -*- coding: utf-8 -*-
from django.test import TestCase

from mock import patch

from unisender.models import Tag, Field, SubscribeList, Campaign, Subscriber


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

class SubscriberManagerTestCase(TestCase):

    list_export_contacts ={
      'result':{
        'field_names':['email', u'Имя', u'email_status', u'email_availability',
                       'email_subscribed_lists', 'email_subscribed_times',
                       'email_add_time'],
        'data':[['test1@example.org', u'Вася', 'active', 'available',
                 '123,127', '2010-06-15 12:54:07,2010-06-15 12:54:07',
                 '2010-06-15 12:34:01'],
                ['test2@example.org', u'Петя', 'invited', 'unreachable',
                 '123', '2010-03-15 18:12:55', '2010-03-15 18:12:55'],
                ['test3@example.org', u'Коля', 'active', 'avaialable',
                 '', '', '2010-03-15 18:12:55']]
        }
    }

    def setUp(self):
        self.manager = Subscriber.unisender
        with patch('unisender.managers.UnisenderManager.api') as mock:
            self.manager.api = mock.return_value
            self.manager.api.exportContacts.return_value = self.list_export_contacts

    def test__export_contacts(self):
        # simple test
        contacts = self.manager.export_contacts()
        self.assertEquals(self.list_export_contacts, contacts)

    def test__update_subsribers(self):
        subscribe_list_1 = SubscribeList.objects.create(title='test 1', sync=True,
                                                      unisender_id=123)
        subscribe_list_2 = SubscribeList.objects.create(title='test 2', sync=True,
                                                      unisender_id=124)
        subscriber_1 = Subscriber.objects.create(contact='test1@example.org')
        subscriber_1.list_ids.add(subscribe_list_2)
        self.manager.update_subsribers()
        subscriber_1 = Subscriber.objects.get(contact='test1@example.org')
        self.assertEquals(subscriber_1.list_ids.all(), [subscribe_list_1])
        subscriber_2 = Subscriber.objects.get(contact='test2@example.org')
        self.assertEquals(subscriber_2.list_ids.all(), [subscribe_list_1])
        subscriber_3 = Subscriber.objects.get(contact='test3@example.org')
        self.assertEquals(subscriber_3.list_ids.all(), [])
