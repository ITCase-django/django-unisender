# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.admin.sites import AdminSite

from mock import patch, Mock

from unisender.models import (
    Tag, Field, SubscribeList, Subscriber, SubscriberFields,
    EmailMessage, Campaign,)

from unisender.admin import (
    FieldAdmin
    )

from .mock_api import unisender_test_empty_api


def get_csrf_token(response):
    csrf = "name='csrfmiddlewaretoken' value='"
    start = response.content.find(csrf) + len(csrf)
    end = response.content.find("'", start)

    return response.content[start:end]

class UnisenderAdminTestCase(TestCase):

    def setUp(self):
        username = 'test_user'
        pwd = 'secret'

        self.user = User.objects.create_user(username, '', pwd)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        self.assertTrue(self.client.login(username=username, password=pwd),
                        "Logging in user %s, pwd %s failed." % (username, pwd))

    def test_open_unisender_app(self):
        """Открываем страницу приложения unisneder в админке"""
        response = self.client.get(
            reverse('admin:app_list', kwargs={'app_label': 'unisender'}))
        self.assertEqual(response.status_code, 200)


class TagAdminTestCase(TestCase):

    def setUp(self):
        username = 'test_user'
        pwd = 'secret'

        self.user = User.objects.create_user(username, '', pwd)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        self.assertTrue(self.client.login(username=username, password=pwd),
                        "Logging in user %s, pwd %s failed." % (username, pwd))

    def test_open_unisender_page(self):
        """Открываем страницу Tags в админке"""
        response = self.client.get(reverse('admin:unisender_tag_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_add_tag(self):
        """Добавляем тэг"""
        start_tag_count = Tag.objects.count()
        url = reverse('admin:unisender_tag_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'name': u'test_tag',
                     'csrfmiddlewaretoken': csrf,}
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('admin:unisender_tag_changelist'))
        self.assertEqual(Tag.objects.count(), start_tag_count + 1)

    def test_update_tag(self):
        """Редактируем тэг"""
        tag = Tag.objects.create(name='test')
        url = reverse('admin:unisender_tag_change', args=(tag.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'name': u'test_tag',
                     'csrfmiddlewaretoken': csrf,
                     }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('admin:unisender_tag_changelist'))
        self.assertTrue(Tag.objects.filter(name='test_tag').exists())

    def test_delete_tag(self):
        """Удаляем тэг"""
        start_unisender_count = Tag.objects.count()
        tag = Tag.objects.create(name='test')
        url = reverse('admin:unisender_tag_delete', args=(tag.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'csrfmiddlewaretoken': csrf}
        response = self.client.post(url, post_data)
        self.assertRedirects(
            response, reverse('admin:unisender_tag_changelist'))
        self.assertEqual(Tag.objects.count(), start_unisender_count)


class FieldAdminTestCase(TestCase):

    def setUp(self):
        username = 'test_user'
        pwd = 'secret'

        self.user = User.objects.create_user(username, '', pwd)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(self.client.login(username=username, password=pwd),
                        "Logging in user %s, pwd %s failed." % (username, pwd))
        site = AdminSite()
        self.admin = FieldAdmin(Field, site)
        self.request = RequestFactory().get(reverse('admin:index'))

    def test_add_field(self):
        """Добавляем поле"""
        start_field_count = Field.objects.count()
        url = reverse('admin:unisender_field_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'name': u'test_field',
                     'csrfmiddlewaretoken': csrf,
                     'sort': 1,
                     'field_type': 'string'}
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('admin:unisender_field_changelist'))
        self.assertEqual(Field.objects.count(), start_field_count + 1)

    def test_update_field(self):
        """Редактируем поле"""
        field = Field.objects.create(name='test')
        url = reverse('admin:unisender_field_change', args=(field.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'name': u'test_field',
                     'csrfmiddlewaretoken': csrf,
                     'sort': 1,
                     'field_type': 'string'
                     }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('admin:unisender_field_changelist'))
        self.assertTrue(Field.objects.filter(name='test_field').exists())

    def test_delete_field(self):
        """Удаляем поле"""
        start_unisender_count = Field.objects.count()
        field = Field.objects.create(name='test')
        url = reverse('admin:unisender_field_delete', args=(field.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'csrfmiddlewaretoken': csrf}
        response = self.client.post(url, post_data)
        self.assertRedirects(
            response, reverse('admin:unisender_field_changelist'))
        self.assertEqual(Field.objects.count(), start_unisender_count)

    def test_admin_get_actions(self):
        actions = self.admin.get_actions(self.request)
        self.assertEqual(len(actions.keys()), 1)
        self.assertIn('delete_selected_fields', actions)

    @patch.object(Field, 'get_api', unisender_test_empty_api)
    def test_delete_selected_fields(self):
        start_unisender_count = Field.objects.count()
        Field.delete_field = Mock(return_value=None)
        for x in xrange(3):
            Field.objects.create(name='test')
        queryset = Field.objects.all()
        self.admin.delete_selected_fields(self.request, queryset)
        self.assertTrue(Field.delete_field.called)
        self.assertEqual(Field.delete_field.call_count, 3)
        self.assertEqual(Field.objects.count(), start_unisender_count)

    @patch.object(Field, 'get_api', unisender_test_empty_api)
    def test_save_model(self):
        start_unisender_count = Field.objects.count()
        field = Field.objects.create(name='test', unisender_id=1)
        field.update_field = Mock(return_value=None)
        self.admin.save_model(self.request, field, None, None)
        self.assertEqual(Field.objects.count(), start_unisender_count + 1)
        self.assertTrue(field.update_field.called)
        self.assertEqual(field.update_field.call_count, 1)
        field_2 = Field.objects.create(name='test_2')
        field_2.create_field = Mock(return_value=None)
        self.admin.save_model(self.request, field_2, None, None)
        self.assertEqual(Field.objects.count(), start_unisender_count + 2)
        self.assertTrue(field_2.create_field.called)
        self.assertEqual(field_2.create_field.call_count, 1)

    @patch.object(Field, 'get_api', unisender_test_empty_api)
    def test_delete_model(self):
        start_unisender_count = Field.objects.count()
        field = Field.objects.create(name='test')
        field.delete_field = Mock(return_value=None)
        self.admin.delete_model(self.request, field)
        self.assertEqual(Field.objects.count(), start_unisender_count)
        self.assertTrue(field.delete_field.called)
        self.assertEqual(field.delete_field.call_count, 1)
