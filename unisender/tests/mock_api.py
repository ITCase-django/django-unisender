# -*- coding: utf-8 -*-


def unisender_test_api(UnisenderModel):
    class UnisenderMockAPI(object):

        def createField(self, **kwargs):
            return {'result': {'id': 1}}

        def updateField(self, **kwargs):
            return {'id': 1}

        def deleteField(self, **kwargs):
            return {'result': {}}

        def deleteList(self, **kwargs):
            return {'result': {}}

        def updateList(self, **kwargs):
            return {'result': {}}

        def createList(self, **kwargs):
            return {'result': {'id': 1}}

        def subscribe(self, **kwargs):
            return {'result': {'person_id': 1}}

        def unsubscribe(self, **kwargs):
            return {'result': {}}

        def exclude(self, **kwargs):
            return {'result': {}}

        def deleteMessage(self, **kwargs):
            return {'result': {}}

        def createEmailMessage(self, **kwargs):
            return {'result': {'message_id': 1}}

        def createCampaign(self, **kwargs):
            return {'result': {'campaign_id': 1, 'status': 'scheduled',
                               'count': 2}}

        def getCampaignStatus(self, **kwargs):
            return {'result': {'status': 'completed',
                               'creation_time': '2011-09-21 19:47:31',
                               'start_time': '2011-09-21 20:00:00'}}

        def getCampaignAggregateStats(self, **kwargs):
            return {'result': {'total': 241, 'data': {
                'ok_read': 239, 'err_will_retry': 2}}
            }

        def getVisitedLinks(self, **kwargs):
            return {
                'result': {
                    'fields': ['email', 'url', 'request_time', 'ip', 'count'],
                    'data': [
                        ['one@gmail.com', 'http://yandex.ru',
                            '2011-01-27 09:38:01', '127.0.0.1', '1'],
                        ['one@gmail.com', 'http://yandex.ru',
                            '2011-01-27 09:38:01', '127.0.0.1', '1'],
                        ['two@hotmail.com', 'http://google.com',
                         '2011-01-27 09:38:02', '127.0.0.1', '2'],
                        ['three@yandex.ru', 'http://gmail.com',
                         '2011-01-27 09:38:03', '127.0.0.1', '3'],
                    ]
                }
            }

        def updateOptInEmail(self, **kwargs):
            return {}

    return UnisenderMockAPI()


def unisender_test_api_errors(UnisenderModel):

    class UnisenderMockAPI(object):
        error_result = {'result': '', 'error': 'invalid_arg'}

        def createField(self, **kwargs):
            return self.error_result

        def updateField(self, **kwargs):
            return self.error_result

        def deleteField(self, **kwargs):
            return self.error_result

        def deleteList(self, **kwargs):
            return self.error_result

        def updateList(self, **kwargs):
            return self.error_result

        def createList(self, **kwargs):
            return self.error_result

        def subscribe(self, **kwargs):
            return self.error_result

        def unsubscribe(self, **kwargs):
            return self.error_result

        def exclude(self, **kwargs):
            return self.error_result

        def deleteMessage(self, **kwargs):
            return self.error_result

        def createEmailMessage(self, **kwargs):
            return self.error_result

        def createCampaign(self, **kwargs):
            return self.error_result

        def getCampaignStatus(self, **kwargs):
            return self.error_result

        def getCampaignAggregateStats(self, **kwargs):
            return self.error_result

        def getVisitedLinks(self, **kwargs):
            return self.error_result

        def updateOptInEmail(self, **kwargs):
            return self.error_result

    return UnisenderMockAPI()


def unisender_test_api_correct_values(UnisenderModel):

    class UnisenderMockAPI(object):

        def all_requirement_fields_present(self, requirement_fields, kwargs):
            for item in requirement_fields:
                if item not in kwargs:
                    raise NameError(
                        'В передаваемых значениях отсутствует обязательное поле < %s >' % item)

        def not_documented_fields_not_present(self, requirement_fields, fields, kwargs):
            all_fields = requirement_fields + fields
            for item in kwargs.keys():
                if item not in all_fields:
                    raise NameError(
                        'В передаваемых значениях присутствует поле < %s > котрое не указано в документации' % item)

        def createField(self, **kwargs):
            requirement_fields = ['name', 'type']
            fields = ['is_visible', 'view_pos']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, fields, kwargs)
            return {}

        def updateField(self, **kwargs):
            requirement_fields = ['id']
            fields = ['name', 'type', 'is_visible', 'view_pos', ]
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, fields, kwargs)
            return {}

        def deleteField(self, **kwargs):
            requirement_fields = ['id']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, [], kwargs)
            return {}

        def deleteList(self, **kwargs):
            requirement_fields = ['list_id']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, [], kwargs)
            return {}

        def updateList(self, **kwargs):
            requirement_fields = ['list_id']
            fields = ['title', 'before_subscribe_url', 'after_subscribe_url']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, fields, kwargs)
            return {}

        def createList(self, **kwargs):
            requirement_fields = ['title']
            fields = ['before_subscribe_url', 'after_subscribe_url']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, fields, kwargs)
            return {}

        def subscribe(self, **kwargs):
            requirement_fields = ['list_ids', 'fields']
            fields = ['tags', 'request_ip', 'request_time ', 'double_optin',
                      'confirm_ip', 'confirm_time', 'overwrite']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, fields, kwargs)
            return {}

        def unsubscribe(self, **kwargs):
            requirement_fields = ['contact_type', 'contact']
            fields = ['list_ids']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, fields, kwargs)
            return {}

        def exclude(self, **kwargs):
            requirement_fields = ['contact_type', 'contact']
            fields = ['list_ids']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, fields, kwargs)
            return {}

        def deleteMessage(self, **kwargs):
            requirement_fields = ['message_id']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, [], kwargs)
            return {}

        def createEmailMessage(self, **kwargs):
            requirement_fields = ['sender_name', 'sender_email', 'subject',
                                  'body', 'list_id']
            fields = ['text_body', 'generate_text', 'tag', 'attachments',
                      'lang', 'series_day', 'series_time', 'wrap_type',
                      'categories']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, fields, kwargs)
            return {}

        def createCampaign(self, **kwargs):
            fields = [
                'message_id', 'start_time', 'timezone', 'track_read',
                'track_links', 'contacts', 'contacts_url', 'defer', 'track_ga',
                'payment_limit', 'payment_currency', 'ga_medium', 'ga_source',
                'ga_campaign', 'ga_content', 'ga_term']
            self.not_documented_fields_not_present([], fields, kwargs)
            return {}

        def getCampaignStatus(self, **kwargs):
            requirement_fields = ['campaign_id']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, [], kwargs)
            return {}

        def getCampaignAggregateStats(self, **kwargs):
            requirement_fields = ['campaign_id']
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, [], kwargs)
            return {}

        def getVisitedLinks(self, **kwargs):
            requirement_fields = ['campaign_id',]
            fields = ['group',]
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, fields, kwargs)
            return {}

        def updateOptInEmail(self, **kwargs):
            requirement_fields = ['sender_name', 'sender_email', 'subject',
                                  'body', 'list_id',]
            self.all_requirement_fields_present(requirement_fields, kwargs)
            self.not_documented_fields_not_present(
                requirement_fields, [], kwargs)
            return {}

    return UnisenderMockAPI()


def mock_messages(request, message):
    return None
