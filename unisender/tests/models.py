# -*- coding: utf-8 -*-
from dateutil.tz import tzutc
from datetime import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError

from mock import patch

from unisender.models import (
    Tag, Field, SubscribeList, Subscriber, SubscriberFields,
    EmailMessage, Campaign, validate_field_name_field, VisitedLink, OptinEmail)


from unisender.error_codes import UNISENDER_COMMON_ERRORS
from .mock_api import (
    unisender_test_api, unisender_test_api_errors,
    unisender_test_api_correct_values)


class FieldModelTestCase(TestCase):

    def setUp(self):
        self.field = Field.objects.create(name='test')

    def test__get_last_error(self):
        field = Field.objects.create(name='test', last_error='invalid_arg')
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

    @patch.object(Field, 'get_api', unisender_test_api_errors)
    def test__create_field_error(self):
        self.field.create_field()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'], self.field.get_last_error())

    @patch.object(Field, 'get_api', unisender_test_api_errors)
    def test__update_field_error(self):
        self.field.update_field()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'], self.field.get_last_error())

    @patch.object(Field, 'get_api', unisender_test_api_errors)
    def test__delete_field_error(self):
        self.assertEquals(self.field.delete_field(), None)
        # TODO test logging

    @patch.object(Field, 'get_api', unisender_test_api_correct_values)
    def test__create_field_correct_values(self):
        self.field.create_field()

    @patch.object(Field, 'get_api', unisender_test_api_correct_values)
    def test__update_field_error_correct_values(self):
        self.field.update_field()

    @patch.object(Field, 'get_api', unisender_test_api_correct_values)
    def test__delete_field_error_correct_values(self):
        self.field.delete_field()

    def test__validate_field_name_field(self):
        self.assertRaises(ValidationError, validate_field_name_field, u'тест')
        self.assertIsNone(validate_field_name_field('test'))


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

    @patch.object(SubscribeList, 'get_api', unisender_test_api_errors)
    def test__delete_list_error(self):
        self.assertIsNone(self.list.delete_list())

    @patch.object(SubscribeList, 'get_api', unisender_test_api_errors)
    def test__update_list_error(self):
        self.assertIsNone(self.list.update_list())
        self.list.update_list()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'], self.list.get_last_error())

    @patch.object(SubscribeList, 'get_api', unisender_test_api_errors)
    def test__create_list_error(self):
        self.assertIsNone(self.list.create_list())
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'], self.list.get_last_error())

    @patch.object(SubscribeList, 'get_api', unisender_test_api_correct_values)
    def test__delete_list_correct_values(self):
        self.list.delete_list()

    @patch.object(SubscribeList, 'get_api', unisender_test_api_correct_values)
    def test__update_list_correct_values(self):
        self.list.update_list()

    @patch.object(SubscribeList, 'get_api', unisender_test_api_correct_values)
    def test__create_list_correct_values(self):
        self.list.create_list()


class OptinEmailTestCase(TestCase):

    def setUp(self):
        subscribe_list = SubscribeList.objects.create(
            title='test', unisender_id=1)
        self.optin_email = OptinEmail.objects.create(
            list_id=subscribe_list, sender_name='test',
            sender_email='test@example.com', subject='test')

    @patch.object(OptinEmail, 'get_api', unisender_test_api)
    def test__update_optin_email(self):
        self.assertIsNone(self.optin_email.update_optin_email())

    @patch.object(OptinEmail, 'get_api', unisender_test_api_errors)
    def test__update_optin_email_error(self):
        email = self.optin_email
        email.update_optin_email()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'], email.get_last_error())

    @patch.object(OptinEmail, 'get_api', unisender_test_api_correct_values)
    def test__exclude_correct_values(self):
        email = self.optin_email
        email.update_optin_email()


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
            title='test', unisender_id=1)
        subscriber.list_ids.add(subscriber_list_1)
        self.assertEquals(
            str(subscriber_list_1.pk), subscriber.serialize_list_id())
        subscriber_list_2 = SubscribeList.objects.create(
            title='test_2', unisender_id=2)
        subscriber.list_ids.add(subscriber_list_2)
        self.assertEquals('1,2', subscriber.serialize_list_id())

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
        self.assertIsNone(subscriber.exclude())

    @patch.object(Subscriber, 'get_api', unisender_test_api_errors)
    def test__subscribe_error(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        subscriber.subscribe()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'], subscriber.get_last_error())

    @patch.object(Subscriber, 'get_api', unisender_test_api_errors)
    def test__unsubscribe_error(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        subscriber.unsubscribe()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'], subscriber.get_last_error())

    @patch.object(Subscriber, 'get_api', unisender_test_api_errors)
    def test__exclude_error(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        subscriber.exclude()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'], subscriber.get_last_error())

    @patch.object(Subscriber, 'get_api', unisender_test_api_correct_values)
    def test__subscribe_correct_values(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        subscriber.subscribe()

    @patch.object(Subscriber, 'get_api', unisender_test_api_correct_values)
    def test__unsubscribe_correct_values(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        subscriber.unsubscribe()

    @patch.object(Subscriber, 'get_api', unisender_test_api_correct_values)
    def test__exclude_correct_values(self):
        subscriber = Subscriber.objects.create(contact='mail@example.com')
        subscriber.exclude()

class EmailMessageTestCase(TestCase):

    def setUp(self):
        subscriber_list = SubscribeList.objects.create(title='test')
        self.message = EmailMessage.objects.create(
            sender_name='test', sender_email='mail@example.com', subject='test',
            body='test', list_id=subscriber_list)

    @patch.object(EmailMessage, 'get_api', unisender_test_api)
    def test__delete_message(self):
        self.assertIsNone(self.message.delete_message())

    @patch.object(EmailMessage, 'get_api', unisender_test_api_errors)
    def test__delete_message_errors(self):
        self.message.delete_message()
        self.assertIsNotNone(self.message)
        self.assertIsNotNone(self.message.get_last_error())

    @patch.object(EmailMessage, 'get_api', unisender_test_api)
    def test__create_email_message(self):
        self.assertEquals(self.message.create_email_message(), 1)

    @patch.object(EmailMessage, 'get_api', unisender_test_api_errors)
    def test__create_email_message_error(self):
        self.message.create_email_message()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'],
            self.message.get_last_error())

    @patch.object(EmailMessage, 'get_api', unisender_test_api_correct_values)
    def test__delete_message_correct_values(self):
        self.message.delete_message()

    @patch.object(EmailMessage, 'get_api', unisender_test_api_correct_values)
    def test__create_email_message_correct_values(self):
        self.message.create_email_message()


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
        self.assertEquals(self.campaign.create_campaign(), 1)

    @patch.object(Campaign, 'get_api', unisender_test_api_correct_values)
    def test__create_campaign_correct_values(self):
        self.campaign.create_campaign()

    @patch.object(Campaign, 'get_api', unisender_test_api_errors)
    def test__create_campaign_error(self):
        self.campaign.create_campaign()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'],
            self.campaign.get_last_error())

    def test__get_success_count(self):
        self.campaign.ok_delivered = 5
        self.campaign.ok_link_visited = 2
        self.campaign.ok_unsubscribed = 3
        self.campaign.ok_read = 1
        self.campaign.ok_spam_folder =4
        self.campaign.save()
        self.assertEquals(self.campaign.get_success_count(), 15)

    def test__get_error_count(self):
        self.campaign.err_user_unknown = 1
        self.campaign.err_user_inactive = 2
        self.campaign.err_mailbox_full = 1
        self.campaign.err_spam_rejected = 3
        self.campaign.err_spam_folder = 1
        self.campaign.err_delivery_failed = 1
        self.campaign.err_will_retry = 1
        self.campaign.err_resend = 1
        self.campaign.err_domain_inactive = 7
        self.campaign.err_skip_letter = 1
        self.campaign.err_spam_skipped = 1
        self.campaign.err_spam_retry = 1
        self.campaign.err_unsubscribed = 1
        self.campaign.err_src_invalid = 1
        self.campaign.err_dest_invalid = 1
        self.campaign.err_not_allowed = 9
        self.campaign.err_not_available = 1
        self.campaign.err_lost = 1
        self.campaign.err_internal = 10
        self.campaign.save()
        self.assertEquals(self.campaign.get_error_count(), 45)

    @patch.object(Campaign, 'get_api', unisender_test_api)
    def test__get_campaign_status(self):
        self.campaign.get_campaign_status()
        self.assertEquals(self.campaign.status, 'completed')
        self.assertEquals(self.campaign.creation_time, '2011-09-21 19:47:31')
        self.assertEquals(self.campaign.start_time, '2011-09-21 20:00:00')

    @patch.object(Campaign, 'get_api', unisender_test_api_correct_values)
    def test__get_campaign_status_correct_values(self):
        self.campaign.get_campaign_status()

    @patch.object(Campaign, 'get_api', unisender_test_api_errors)
    def test__get_campaign_status_error(self):
        self.campaign.get_campaign_status()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'],
            self.campaign.get_last_error())

    @patch.object(Campaign, 'get_api', unisender_test_api)
    def test__get_campaign_agregate_stats(self):
        self.campaign.get_campaign_agregate_status()
        self.assertEquals(self.campaign.total, 241)
        self.assertEquals(self.campaign.ok_read, 239)
        self.assertEquals(self.campaign.err_will_retry, 2)

    @patch.object(Campaign, 'get_api', unisender_test_api_errors)
    def test__get_campaign_agregate_status_error(self):
        self.campaign.get_campaign_agregate_status()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'],
            self.campaign.get_last_error())

    @patch.object(Campaign, 'get_api', unisender_test_api_correct_values)
    def test__get_campaign_agregate_status_correct_values(self):
        self.campaign.get_campaign_agregate_status()

    @patch.object(Campaign, 'get_api', unisender_test_api)
    def test__get_visited_links(self):
        self.campaign.get_visited_links()
        link_1 = VisitedLink.objects.get(email='one@gmail.com')
        self.assertEquals(link_1.campaign, self.campaign)
        self.assertEquals(link_1.count, 2)
        self.assertEquals(link_1.ip, '127.0.0.1')
        self.assertEquals(link_1.url, 'http://yandex.ru')
        naive = datetime.strptime('2011-01-27 09:38:01', '%Y-%m-%d %H:%M:%S')
        aware = naive.replace(tzinfo=tzutc())
        self.assertEquals(link_1.request_time, aware)

        link_2 = VisitedLink.objects.get(email='two@hotmail.com')
        self.assertEquals(link_2.campaign, self.campaign)
        self.assertEquals(link_2.count, 2)
        self.assertEquals(link_2.ip, '127.0.0.1')
        self.assertEquals(link_2.url, 'http://google.com')
        naive = datetime.strptime('2011-01-27 09:38:02', '%Y-%m-%d %H:%M:%S')
        aware = naive.replace(tzinfo=tzutc())
        self.assertEquals(link_2.request_time, aware)

        link_3 = VisitedLink.objects.get(email='three@yandex.ru')
        self.assertEquals(link_3.campaign, self.campaign)
        self.assertEquals(link_3.count, 3)
        self.assertEquals(link_3.ip, '127.0.0.1')
        self.assertEquals(link_3.url, 'http://gmail.com')
        naive = datetime.strptime('2011-01-27 09:38:03', '%Y-%m-%d %H:%M:%S')
        aware = naive.replace(tzinfo=tzutc())
        self.assertEquals(link_3.request_time, aware)

    @patch.object(Campaign, 'get_api', unisender_test_api_errors)
    def test__get_visited_links_error(self):
        self.campaign.get_visited_links()
        self.assertEquals(
            UNISENDER_COMMON_ERRORS['invalid_arg'],
            self.campaign.get_last_error())

    @patch.object(Campaign, 'get_api', unisender_test_api_correct_values)
    def test__get_visited_links_values(self):
        self.campaign.get_visited_links()
