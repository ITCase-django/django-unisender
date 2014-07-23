# -*- coding: utf-8 -*-
import unittest
import urllib
from unisender.unisender_urls import (
    EMAIL_MESSAGES_LIST, EMAIL_MESSAGES_DETAIL, TAG_LIST, FIELD_LIST,
    CAMPAIGN_LIST, CAMPAIGN_DETAIL, SUBSCRIBELIST_LIST, SUBSCRIBELIST_DETAIL
    )

class LinkOpenedTestCase(unittest.TestCase):

    def test_email_message_list(self):
        self.assertEquals(urllib.urlopen(EMAIL_MESSAGES_LIST).getcode(), 200)

    def test_email_message_detail(self):
        detail_url = EMAIL_MESSAGES_DETAIL + '1'
        self.assertEquals(urllib.urlopen(detail_url).getcode(), 200)

    def test_tag_list(self):
        self.assertEquals(urllib.urlopen(TAG_LIST).getcode(), 200)

    def test_field_list(self):
        self.assertEquals(urllib.urlopen(FIELD_LIST).getcode(), 200)

    def test_campaign_list(self):
        self.assertEquals(urllib.urlopen(CAMPAIGN_LIST).getcode(), 200)

    def test_campaign_detail(self):
        detail_url = CAMPAIGN_DETAIL + '1'
        self.assertEquals(urllib.urlopen(detail_url).getcode(), 200)

    def test_subscribe_list(self):
        self.assertEquals(urllib.urlopen(SUBSCRIBELIST_LIST).getcode(), 200)

    def test_subscribe_list_detail(self):
        detail_url = SUBSCRIBELIST_DETAIL + '1'
        self.assertEquals(urllib.urlopen(detail_url).getcode(), 200)
