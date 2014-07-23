# -*- coding: utf-8 -*-
import unittest
from unisender.tests.mock_api import unisender_test_api_correct_values

class MockApiTestCase(unittest.TestCase):

    def setUp(self):
        self.api = unisender_test_api_correct_values(object)

    def test__all_requirement_fields_present(self):
        kwargs = {'test': 1, 'test_1': 2}
        requirement_fields = ['test']
        self.assertIsNone(self.api.all_requirement_fields_present(
            requirement_fields, kwargs))
        self.assertRaises(NameError, self.api.all_requirement_fields_present,
                          ['test_3'], kwargs)

    def test__not_documented_fields_not_present(self):
        kwargs = {'test': 1, 'test_1': 2}
        requirement_fields = ['test']
        all_fields = ['test_1']
        self.assertIsNone(self.api.not_documented_fields_not_present(
            requirement_fields, all_fields, kwargs))
        self.assertRaises(NameError, self.api.not_documented_fields_not_present,
                          all_fields, ['test_3'], kwargs)
