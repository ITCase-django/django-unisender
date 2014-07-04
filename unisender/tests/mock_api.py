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

    return UnisenderMockAPI()
