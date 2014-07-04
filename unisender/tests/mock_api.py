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
    return UnisenderMockAPI()


def unisender_test_api_errors(UnisenderModel):
    class UnisenderMockAPI(object):

        def createField(self, **kwargs):
            return {'result': '', 'error': 'invalid_arg'}

        def deleteMessage(self, **kwargs):
            return {'error': 'message not found', 'result': ''}

    return UnisenderMockAPI()
