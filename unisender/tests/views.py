# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from mock import Mock, patch

from unisender.models import (
    Tag, Field, SubscribeList, Subscriber, EmailMessage, Campaign)

from unisender.views import (
    GetCampaignStatistic, GetTags, GetFields, GetLists, GetCampaigns
)


class UnisenderGetCampaignStatisticTestCase(TestCase):

    def test_admin_auth_open_page(self):
        username = 'test_user'
        pwd = 'secret'

        user = User.objects.create_user(username, '', pwd)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.assertTrue(self.client.login(username=username, password=pwd),
                        "Logging in user %s, pwd %s failed." % (username, pwd))

        subscribe_list = SubscribeList.objects.create(title='test')
        message = EmailMessage.objects.create(
            sender_name='test', sender_email='mail@example.com', subject='test',
            body='test', lang='ru', generate_text=1, wrap_type='skip',
            list_id=subscribe_list, sync=True
        )
        Campaign.get_campaign_status = Mock(return_value=None)
        Campaign.get_campaign_agregate_status = Mock(return_value=None)
        Campaign.get_visited_links = Mock(return_value=None)
        campaign = Campaign.objects.create(
            name='test', email_message=message, unisender_id=1)

        response = self.client.get(
            reverse('admin:unisender_campaign_get_statistic',
                    kwargs={'pk': campaign.pk}))
        self.assertRedirects(response, reverse(
            'admin:unisender_campaign_change', args=(str(campaign.pk))))
        self.assertTrue(Campaign.get_campaign_status.called)
        self.assertEqual(Campaign.get_campaign_status.call_count, 1)
        self.assertTrue(Campaign.get_campaign_agregate_status.called)
        self.assertEqual(Campaign.get_campaign_agregate_status.call_count, 1)
        self.assertTrue(Campaign.get_visited_links.called)
        self.assertEqual(Campaign.get_visited_links.call_count, 1)

    def test_admin_not_auth_open_page(self):
        subscribe_list = SubscribeList.objects.create(title='test')
        message = EmailMessage.objects.create(
            sender_name='test', sender_email='mail@example.com', subject='test',
            body='test', lang='ru', generate_text=1, wrap_type='skip',
            list_id=subscribe_list, sync=True
        )
        campaign = Campaign.objects.create(
            name='test', email_message=message, unisender_id=1)
        response = self.client.get(
            reverse('admin:unisender_campaign_get_statistic',
                    kwargs={'pk': campaign.pk}))
        self.assertEquals(response.status_code, 200)


class UnisenderGetTagsTestCase(TestCase):

    def test_admin_auth_open_page(self):
        username = 'test_user'
        pwd = 'secret'

        user = User.objects.create_user(username, '', pwd)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.assertTrue(self.client.login(username=username, password=pwd),
                        "Logging in user %s, pwd %s failed." % (username, pwd))
        Tag.unisender.get_and_update_tags = Mock(return_value=None)

        response = self.client.get(reverse('admin:unisender_get_tags'))
        self.assertRedirects(
            response, reverse('admin:unisender_tag_changelist'))
        self.assertTrue(Tag.unisender.get_and_update_tags.called)
        self.assertEqual(Tag.unisender.get_and_update_tags.call_count, 1)

    def test_admin_not_auth_open_page(self):
        response = self.client.get(reverse('admin:unisender_get_tags'))
        self.assertEquals(response.status_code, 200)


class UnisenderGetFieldsTestCase(TestCase):

    def test_admin_auth_open_page(self):
        username = 'test_user'
        pwd = 'secret'

        user = User.objects.create_user(username, '', pwd)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.assertTrue(self.client.login(username=username, password=pwd),
                        "Logging in user %s, pwd %s failed." % (username, pwd))
        Field.unisender.get_and_update_fields = Mock(return_value=None)

        response = self.client.get(reverse('admin:unisender_get_fields'))
        self.assertRedirects(
            response, reverse('admin:unisender_field_changelist'))
        self.assertTrue(Field.unisender.get_and_update_fields.called)
        self.assertEqual(Field.unisender.get_and_update_fields.call_count, 1)

    def test_admin_not_auth_open_page(self):
        response = self.client.get(reverse('admin:unisender_get_fields'))
        self.assertEquals(response.status_code, 200)


class UnisenderGetListsTestCase(TestCase):

    def test_admin_auth_open_page(self):
        username = 'test_user'
        pwd = 'secret'

        user = User.objects.create_user(username, '', pwd)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.assertTrue(self.client.login(username=username, password=pwd),
                        "Logging in user %s, pwd %s failed." % (username, pwd))
        SubscribeList.unisender.get_and_update_lists = Mock(return_value=None)

        response = self.client.get(reverse('admin:unisender_get_lists'))
        self.assertRedirects(
            response, reverse('admin:unisender_subscribelist_changelist'))
        self.assertTrue(SubscribeList.unisender.get_and_update_lists.called)
        self.assertEqual(SubscribeList.unisender.get_and_update_lists.call_count, 1)

    def test_admin_not_auth_open_page(self):
        response = self.client.get(reverse('admin:unisender_get_lists'))
        self.assertEquals(response.status_code, 200)


class UnisenderGetCampaignsTestCase(TestCase):

    def test_admin_auth_open_page(self):
        username = 'test_user'
        pwd = 'secret'

        user = User.objects.create_user(username, '', pwd)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.assertTrue(self.client.login(username=username, password=pwd),
                        "Logging in user %s, pwd %s failed." % (username, pwd))
        Campaign.unisender.get_and_update_campaigns = Mock(return_value=None)

        response = self.client.get(reverse('admin:unisender_get_campaigns'))
        self.assertRedirects(
            response, reverse('admin:unisender_campaign_changelist'))
        self.assertTrue(Campaign.unisender.get_and_update_campaigns.called)
        self.assertEqual(Campaign.unisender.get_and_update_campaigns.call_count, 1)

    def test_admin_not_auth_open_page(self):
        response = self.client.get(reverse('admin:unisender_get_campaigns'))
        self.assertEquals(response.status_code, 200)
