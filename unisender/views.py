# -*- coding: utf-8 -*-
# django
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

#app
from unisender.models import Campaign, Tag, Field


class GetCampaignStatistic(RedirectView):
    permanent = False
    pattern_name = 'admin:unisender_campaign_changelist'

    def get_redirect_url(self, *args, **kwargs):
        campaign = get_object_or_404(Campaign, pk=self.kwargs['pk'])
        campaign.get_campaign_status()
        if campaign.get_last_error() is None:
            campaign.get_campaign_agregate_status()
        campaign.save()
        self.url = reverse_lazy(
            'admin:unisender_campaign_change', args=(self.kwargs['pk']))
        return super(GetCampaignStatistic, self).get_redirect_url(
            *args, **kwargs)


class GetTags(RedirectView):
    permanent = False
    pattern_name = 'admin:unisender_tag_changelist'

    def get_redirect_url(self, *args, **kwargs):
        Tag.unisender.get_and_update_tags(self.request)
        return super(GetTags, self).get_redirect_url(*args, **kwargs)


class GetFields(RedirectView):
    permanent = False
    pattern_name = 'admin:unisender_field_changelist'

    def get_redirect_url(self, *args, **kwargs):
        Field.unisender.get_and_update_fields(self.request)
        return super(GetFields, self).get_redirect_url(*args, **kwargs)
