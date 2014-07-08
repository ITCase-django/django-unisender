# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.admin.sites import AdminSite

from mock import Mock

from unisender.models import (
    Tag, Field, SubscribeList, Subscriber, SubscriberFields,
    EmailMessage, Campaign,)

from unisender.admin import (
    FieldAdmin, SubscribeListAdmin, SubscriberAdmin, EmailMessageAdmin
    )


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

    def test_open_unisender_page(self):
        """Открываем страницу Tags в админке"""
        response = self.client.get(reverse('admin:unisender_field_changelist'))
        self.assertEqual(response.status_code, 200)

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

    def test_delete_model(self):
        start_unisender_count = Field.objects.count()
        field = Field.objects.create(name='test')
        field.delete_field = Mock(return_value=None)
        self.admin.delete_model(self.request, field)
        self.assertEqual(Field.objects.count(), start_unisender_count)
        self.assertTrue(field.delete_field.called)
        self.assertEqual(field.delete_field.call_count, 1)


class SubscribeListAdminTestCase(TestCase):

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
        self.admin = SubscribeListAdmin(SubscribeList, site)
        self.request = RequestFactory().get(reverse('admin:index'))


    def test_open_unisender_page(self):
        """Открываем страницу Tags в админке"""
        response = self.client.get(
            reverse('admin:unisender_subscribelist_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_add_subscribe_list(self):
        """Добавляем список рассылки"""
        start_subscribe_list_count = SubscribeList.objects.count()
        url = reverse('admin:unisender_subscribelist_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'title': u'test_subscribe_list',
                     'csrfmiddlewaretoken': csrf,
                     }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('admin:unisender_subscribelist_changelist'))
        self.assertEqual(SubscribeList.objects.count(), start_subscribe_list_count + 1)

    def test_update_subscribe_list(self):
        """Редактируем список рассылки"""
        subscribe_list = SubscribeList.objects.create(title='test')
        url = reverse('admin:unisender_subscribelist_change', args=(subscribe_list.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'title': u'test_subscribe_list',
                     'csrfmiddlewaretoken': csrf,
                     }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('admin:unisender_subscribelist_changelist'))
        self.assertTrue(SubscribeList.objects.filter(title='test_subscribe_list').exists())

    def test_delete_subscribe_list(self):
        """Удаляем список рассылки"""
        start_unisender_count = SubscribeList.objects.count()
        subscribe_list = SubscribeList.objects.create(title='test')
        url = reverse('admin:unisender_subscribelist_delete', args=(subscribe_list.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'csrfmiddlewaretoken': csrf}
        response = self.client.post(url, post_data)
        self.assertRedirects(
            response, reverse('admin:unisender_subscribelist_changelist'))
        self.assertEqual(SubscribeList.objects.count(), start_unisender_count)

    def test_admin_get_actions(self):
        actions = self.admin.get_actions(self.request)
        self.assertEqual(len(actions.keys()), 1)
        self.assertIn('delete_selected_subscribe_list', actions)

    def test_delete_selected_lists(self):
        start_unisender_count = SubscribeList.objects.count()
        SubscribeList.delete_list = Mock(return_value=None)
        for x in xrange(3):
            SubscribeList.objects.create(title='test_%s' % x)
        queryset = SubscribeList.objects.all()
        self.admin.delete_selected_subscribe_list(self.request, queryset)
        self.assertTrue(SubscribeList.delete_list.called)
        self.assertEqual(SubscribeList.delete_list.call_count, 3)
        self.assertEqual(SubscribeList.objects.count(), start_unisender_count)

    def test_save_model(self):
        start_unisender_count = SubscribeList.objects.count()
        subscribe_list = SubscribeList.objects.create(title='test', unisender_id=1)
        subscribe_list.update_list = Mock(return_value=None)
        self.admin.save_model(self.request, subscribe_list, None, None)
        self.assertEqual(SubscribeList.objects.count(), start_unisender_count + 1)
        self.assertTrue(subscribe_list.update_list.called)
        self.assertEqual(subscribe_list.update_list.call_count, 1)

        subscribe_list_2 = SubscribeList.objects.create(title='test_2')
        subscribe_list_2.create_list = Mock(return_value=None)
        self.admin.save_model(self.request, subscribe_list_2, None, None)
        self.assertEqual(SubscribeList.objects.count(), start_unisender_count + 2)
        self.assertTrue(subscribe_list_2.create_list.called)
        self.assertEqual(subscribe_list_2.create_list.call_count, 1)

    def test_delete_model(self):
        start_unisender_count = SubscribeList.objects.count()
        subscribe_list = SubscribeList.objects.create(title='test')
        subscribe_list.delete_list = Mock(return_value=None)
        self.admin.delete_model(self.request, subscribe_list)
        self.assertEqual(SubscribeList.objects.count(), start_unisender_count)
        self.assertTrue(subscribe_list.delete_list.called)
        self.assertEqual(subscribe_list.delete_list.call_count, 1)


class SubscriberAdminTestCase(TestCase):

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
        self.admin = SubscriberAdmin(Subscriber, site)
        self.request = RequestFactory().get(reverse('admin:index'))


    def test_open_unisender_page(self):
        """Открываем страницу подписчиков в админке"""
        response = self.client.get(
            reverse('admin:unisender_subscriber_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_add_subscribe_list(self):
        """Добавляем подписчика через админку"""
        start_subscriber_count = Subscriber.objects.count()
        url = reverse('admin:unisender_subscriber_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        subscribe_list = SubscribeList.objects.create(title='test')
        post_data = {'list_ids': subscribe_list.pk,
                     'csrfmiddlewaretoken': csrf,
                     'contact_type': 'email',
                     'contact': 'email@example.com',
                     'fields-TOTAL_FORMS': 0,
                     'fields-INITIAL_FORMS': 0,
                     'fields-MAX_NUM_FORMS': 1000,
                     'double_optin': 1,
                     }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('admin:unisender_subscriber_changelist'))
        self.assertEqual(Subscriber.objects.count(), start_subscriber_count + 1)

    def test_update_subscribe_list(self):
        """Редактируем получателя"""
        subscriber = Subscriber.objects.create(contact='email@example.com')
        url = reverse('admin:unisender_subscriber_change', args=(subscriber.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        subscribe_list = SubscribeList.objects.create(title='test')
        post_data = {'list_ids': subscribe_list.pk,
                     'csrfmiddlewaretoken': csrf,
                     'contact_type': 'email',
                     'contact': 'email@example.com',
                     'fields-TOTAL_FORMS': 0,
                     'fields-INITIAL_FORMS': 0,
                     'fields-MAX_NUM_FORMS': 1000,
                     'double_optin': 1,
                     }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('admin:unisender_subscriber_changelist'))
        self.assertTrue(Subscriber.objects.filter(contact='email@example.com').exists())

    def test_delete_subscribe_list(self):
        """Удаляем получателя"""
        start_unisender_count = Subscriber.objects.count()
        subscriber = Subscriber.objects.create(contact='email@example.com')
        url = reverse('admin:unisender_subscriber_delete', args=(subscriber.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'csrfmiddlewaretoken': csrf}
        response = self.client.post(url, post_data)
        self.assertRedirects(
            response, reverse('admin:unisender_subscriber_changelist'))
        self.assertEqual(Subscriber.objects.count(), start_unisender_count)

    def test_admin_get_actions(self):
        actions = self.admin.get_actions(self.request)
        self.assertEqual(len(actions.keys()), 1)
        self.assertIn('delete_selected_subscribers', actions)

    def test_delete_selected_subscribers(self):
        start_unisender_count = Subscriber.objects.count()
        Subscriber.exclude = Mock(return_value=None)
        for x in xrange(3):
            Subscriber.objects.create(contact='email@example.com')
        queryset = Subscriber.objects.all()
        self.admin.delete_selected_subscribers(self.request, queryset)
        self.assertTrue(Subscriber.exclude.called)
        self.assertEqual(Subscriber.exclude.call_count, 3)
        self.assertEqual(Subscriber.objects.count(), start_unisender_count)

    def test_save_model(self):
        start_unisender_count = Subscriber.objects.count()
        subscriber = Subscriber.objects.create(contact='email@example.com')
        subscriber.subscribe = Mock(return_value=None)
        self.admin.save_model(self.request, subscriber, None, None)
        self.assertEqual(Subscriber.objects.count(), start_unisender_count + 1)
        self.assertTrue(subscriber.subscribe.called)
        self.assertEqual(subscriber.subscribe.call_count, 1)

    def test_delete_model(self):
        start_unisender_count = Subscriber.objects.count()
        subscriber = Subscriber.objects.create(contact='email@example.com')
        subscriber.exclude = Mock(return_value=None)
        self.admin.delete_model(self.request, subscriber)
        self.assertEqual(Subscriber.objects.count(), start_unisender_count)
        self.assertTrue(subscriber.exclude.called)
        self.assertEqual(subscriber.exclude.call_count, 1)

class EmailMessageAdminTestCase(TestCase):

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
        self.admin = EmailMessageAdmin(EmailMessage, site)
        self.request = RequestFactory().get(reverse('admin:index'))


    def test_open_unisender_page(self):
        """Открываем страницу подписчиков в админке"""
        response = self.client.get(
            reverse('admin:unisender_emailmessage_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_add_subscribe_list(self):
        """Добавляем email сообщение через админку"""
        start_subscriber_count = EmailMessage.objects.count()
        url = reverse('admin:unisender_emailmessage_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        subscribe_list = SubscribeList.objects.create(title='test')
        post_data = {'list_id': subscribe_list.pk,
                     'csrfmiddlewaretoken': csrf,
                     'sender_name': 'test',
                     'sender_email': 'mail@example.com',
                     'subject': 'test',
                     'body': 'test',
                     'lang': 'ru',
                     'generate_text': 1,
                     'wrap_type': 'skip',
                     'double_optin': 1,
                     'series_time': '11:00'
                     }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('admin:unisender_emailmessage_changelist'))
        self.assertEqual(EmailMessage.objects.count(), start_subscriber_count + 1)

    def test_update_subscribe_list(self):
        """Редактируем email сообщение"""
        subscribe_list = SubscribeList.objects.create(title='test')
        email = EmailMessage.objects.create(
            sender_name='test', sender_email='mail@example.com', subject='test',
            body='test', lang='ru', generate_text=1, wrap_type='skip',
            list_id=subscribe_list
            )
        url = reverse('admin:unisender_emailmessage_change', args=(email.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'list_id': subscribe_list.pk,
                     'csrfmiddlewaretoken': csrf,
                     'sender_name': 'test',
                     'sender_email': 'mail@example.com',
                     'subject': 'test',
                     'body': 'test',
                     'lang': 'ru',
                     'generate_text': 1,
                     'wrap_type': 'skip',
                     'double_optin': 1,
                     'series_time': '11:00'
                     }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('admin:unisender_emailmessage_changelist'))
        self.assertTrue(EmailMessage.objects.filter(
            sender_email='mail@example.com').exists())

    def test_delete_subscribe_list(self):
        """Удаляем email сообщение"""
        start_unisender_count = EmailMessage.objects.count()
        subscribe_list = SubscribeList.objects.create(title='test')
        message = EmailMessage.objects.create(
            sender_name='test', sender_email='mail@example.com', subject='test',
            body='test', lang='ru', generate_text=1, wrap_type='skip',
            list_id=subscribe_list
            )
        url = reverse('admin:unisender_emailmessage_delete', args=(message.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf = get_csrf_token(response)
        post_data = {'csrfmiddlewaretoken': csrf}
        response = self.client.post(url, post_data)
        self.assertRedirects(
            response, reverse('admin:unisender_emailmessage_changelist'))
        self.assertEqual(EmailMessage.objects.count(), start_unisender_count)

    def test_admin_get_actions(self):
        actions = self.admin.get_actions(self.request)
        self.assertEqual(len(actions.keys()), 1)
        self.assertIn('delete_selected_emails', actions)

    def test_delete_selected_emails(self):
        start_unisender_count = EmailMessage.objects.count()
        EmailMessage.delete_message = Mock(return_value=None)
        subscribe_list = SubscribeList.objects.create(title='test')
        for x in xrange(3):
            EmailMessage.objects.create(
                sender_name='test', sender_email='mail@example.com', subject='test',
                body='test', lang='ru', generate_text=1, wrap_type='skip',
                list_id=subscribe_list
                )
        queryset = EmailMessage.objects.all()
        self.admin.delete_selected_emails(self.request, queryset)
        self.assertTrue(EmailMessage.delete_message.called)
        self.assertEqual(EmailMessage.delete_message.call_count, 3)
        self.assertEqual(EmailMessage.objects.count(), start_unisender_count)

    def test_save_model(self):
        start_unisender_count = Subscriber.objects.count()
        subscribe_list = SubscribeList.objects.create(title='test')
        message = EmailMessage.objects.create(
            sender_name='test', sender_email='mail@example.com', subject='test',
            body='test', lang='ru', generate_text=1, wrap_type='skip',
            list_id=subscribe_list
            )
        message.create_email_message = Mock(return_value=None)
        self.admin.save_model(self.request, message, None, None)
        self.assertEqual(EmailMessage.objects.count(), start_unisender_count + 1)
        self.assertTrue(message.create_email_message.called)
        self.assertEqual(message.create_email_message.call_count, 1)

        message_2 = EmailMessage.objects.create(
            sender_name='test', sender_email='mail@example.com', subject='test',
            body='test', lang='ru', generate_text=1, wrap_type='skip',
            list_id=subscribe_list, unisender_id=1
            )
        message_2.create_email_message = Mock(return_value=None)
        self.admin.save_model(self.request, message_2, None, None)
        self.assertEqual(EmailMessage.objects.count(),
                         start_unisender_count + 2)
        self.assertFalse(message_2.create_email_message.called)

    def test_delete_model(self):
        start_unisender_count = EmailMessage.objects.count()
        subscribe_list = SubscribeList.objects.create(title='test')
        message = EmailMessage.objects.create(
            sender_name='test', sender_email='mail@example.com', subject='test',
            body='test', lang='ru', generate_text=1, wrap_type='skip',
            list_id=subscribe_list
            )
        message.delete_message = Mock(return_value=None)
        self.admin.delete_model(self.request, message)
        self.assertEqual(EmailMessage.objects.count(), start_unisender_count)
        self.assertTrue(message.delete_message.called)
        self.assertEqual(message.delete_message.call_count, 1)


    def test_get_readonly_fields(self):
        readonly_fields_initial = ['unisender_id', 'sync', 'get_last_error']
        self.assertListEqual(
            readonly_fields_initial,
            self.admin.get_readonly_fields(self.request))
        subscribe_list = SubscribeList.objects.create(title='test')
        message = EmailMessage.objects.create(
            sender_name='test', sender_email='mail@example.com', subject='test',
            body='test', lang='ru', generate_text=1, wrap_type='skip',
            list_id=subscribe_list, sync=True
            )
        readonly_fields_all = readonly_fields_initial
        readonly_fields_all.extend([
            'sender_name', 'sender_email', 'subject', 'body', 'list_id', 'lang',
            'text_body', 'generate_text', 'wrap_type', 'categories', 'tag',
            'read_only_body', 'series_day', 'last_error', 'series_time', 'id'])
        self.assertItemsEqual(
            readonly_fields_all,
            self.admin.get_readonly_fields(self.request, message))

