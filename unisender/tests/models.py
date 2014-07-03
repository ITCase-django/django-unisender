# -*- coding: utf-8 -*-
from django.test import TestCase

from mock import patch

from unisender.models import (
    UnisenderModel, Tag, Field, SubscribeList, Subscriber, SubscriberFields,
    EmailMessage, Campaign, CampaignStatus
)


from unisender.error_codes import UNISENDER_COMMON_ERRORS
from .mock_api import unisender_test_api, unisender_test_api_errors


class FieldModelTestCase(TestCase):

    def setUp(self):
        self.field = Field.objects.create(name='test')

    @patch.object(Field, 'get_api', unisender_test_api_errors)
    def test__get_last_error(self):
        field = Field.objects.create(name='test')
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'], field.get_last_error())

    @patch.object(Field, 'get_api', unisender_test_api)
    def test__get_last_error_none(self):
        field = Field.objects.create(name='test')
        self.assertIsNone(field.get_last_error())

    @patch.object(Field, 'get_api', unisender_test_api)
    def test__create_field(self):
        self.assertEquals(self.field.create_field(), 1)

    @patch.object(Field, 'get_api', unisender_test_api)
    def test__update_field(self):
        self.assertEquals(self.field.update_field(), 1)

    @patch.object(Field, 'get_api', unisender_test_api)
    def test__delete_field(self):
        self.assertEquals(self.field.delete_field(), None)


class SubscribeListTestCase(TestCase):

    def setUp(self):
        self.list = SubscribeList.objects.create(title='test')

    @patch.object(SubscribeList, 'get_api', unisender_test_api)
    def test__delete_list(self):
        self.assertIsNone(self.list.delete_list())

    @patch.object(SubscribeList, 'get_api', unisender_test_api)
    def test__update_list(self):
        self.assertIsNone(self.list.update_list())

    @patch.object(SubscribeList, 'get_api', unisender_test_api)
    def test__create_list(self):
        self.assertEquals(self.list.create_list(), 1)


class SubscriberTestCase(TestCase):

    def test__serialize_fields(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        subscriber_2 = Subscriber.objects.create(
            contact='9123456789', contact_type='phone')

        self.assertEquals(
            {'email': 'mail@example.com'}, subscriber.serialize_fields())
        self.assertEquals(
            {'phone': '9123456789'}, subscriber_2.serialize_fields())

        field_1 = Field.objects.create(name='test')
        SubscriberFields.objects.create(
            subscriber=subscriber, field=field_1, value='test_value')
        self.assertDictEqual(
            {u'test': u'test_value', 'email': 'mail@example.com'},
            subscriber.serialize_fields())
        field_2 = Field.objects.create(name='test_2')
        SubscriberFields.objects.create(
            subscriber=subscriber_2, field=field_1, value='test_value')
        SubscriberFields.objects.create(
            subscriber=subscriber_2, field=field_2, value='test_value_2')
        self.assertDictEqual(
            {u'test': u'test_value', 'phone': '9123456789', u'test_2': u'test_value_2'},
            subscriber_2.serialize_fields())

    @patch.object(Subscriber, 'get_api', unisender_test_api)
    @patch.object(SubscribeList, 'get_api', unisender_test_api)
    def test__serialize_list_id(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        subscriber_list_1 = SubscribeList.objects.create(
            title='test')
        subscriber.list_ids.add(subscriber_list_1)
        self.assertEquals(
            str(subscriber_list_1.pk), subscriber.serialize_list_id())
        subscriber_list_2 = SubscribeList.objects.create(
            title='test_2')
        subscriber.list_ids.add(subscriber_list_2)
        self.assertEquals('1,1', subscriber.serialize_list_id())

    def test__serialize_tags(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        tag_1 = Tag.objects.create(name='test')
        subscriber.tags.add(tag_1)
        self.assertEquals('test', subscriber.serialize_tags())
        tag_2 = Tag.objects.create(name='test_2')
        subscriber.tags.add(tag_2)
        self.assertEquals('test,test_2', subscriber.serialize_tags())

    @patch.object(Subscriber, 'get_api', unisender_test_api)
    def test__subscribe(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        self.assertEquals(subscriber.subscribe(), 1)

    @patch.object(Subscriber, 'get_api', unisender_test_api)
    def test__unsubscribe(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        self.assertIsNone(subscriber.unsubscribe())

    @patch.object(Subscriber, 'get_api', unisender_test_api)
    def test__exclude(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        self.assertIsNone(subscriber.unsubscribe())


class EmailMessageTestCase(TestCase):

    def setUp(self):
        subscriber_list = SubscribeList.objects.create(title='test')
        self.message = EmailMessage.objects.create(
            sender_name='test', sender_email='mail@example.com', subject='test',
            body='test', list_id=subscriber_list)

    @patch.object(EmailMessage, 'get_api', unisender_test_api)
    def test__delete_message(self):
        self.assertIsNone(self.message.delete_message())

    @patch.object(EmailMessage, 'get_api', unisender_test_api)
    def test__create_email_message(self):
        self.assertEquals(self.message.create_email_message(), 1)


class CampaignTestCase(TestCase):

    def setUp(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        subscriber_list = SubscribeList.objects.create(title='test')
        message = EmailMessage.objects.create(
            sender_name='test', sender_email='mail@example.com', subject='test',
            body='test', list_id=subscriber_list)
        self.campaign = Campaign.objects.create(
            name='test', email_message=message)
        self.campaign.contacts.add(subscriber)

    def test__serrialize_contacts(self):
        self.assertEquals(
            'mail@example.com', self.campaign.serrialize_contacts())
        subscriber = Subscriber.objects.create(contact='mail_2@example.com')
        self.campaign.contacts.add(subscriber)
        self.assertEquals(
            'mail@example.com,mail_2@example.com',
            self.campaign.serrialize_contacts())

    @patch.object(Campaign, 'get_api', unisender_test_api)
    def test__create_campaign(self):
        self.assertDictEqual(
            self.campaign.create_campaign(),
            {'campaign_id': 1, 'status': 'scheduled', 'count': 2})


class CampaignStatusTestCase(TestCase):

    def test__get_success_count(self):
        pass

    def test__get_campaign_status(self):
        pass

    def test__get_campaign_agregate_stats(self):
        pass

    def test__get_visited_links(self):
        pass

    def test__get_error_count(self):
        pass
