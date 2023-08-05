# coding: utf-8

"""
    Model Catalog

    This is MINT Model Catalog You can find out more about Model Catalog at [https://w3id.org/mint/modelCatalog/](https://w3id.org/mint/modelCatalog/)  # noqa: E501

    OpenAPI spec version: v1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import modelcatalog
from modelcatalog.api.emulator_api import EmulatorApi  # noqa: E501
from modelcatalog.rest import ApiException


class TestEmulatorApi(unittest.TestCase):
    """EmulatorApi unit test stubs"""

    def setUp(self):
        self.api = modelcatalog.api.emulator_api.EmulatorApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_emulators_get(self):
        """Test case for emulators_get

        List all Emulator entities  # noqa: E501
        """
        pass

    def test_emulators_id_delete(self):
        """Test case for emulators_id_delete

        Delete a Emulator  # noqa: E501
        """
        pass

    def test_emulators_id_get(self):
        """Test case for emulators_id_get

        Get a Emulator  # noqa: E501
        """
        pass

    def test_emulators_id_put(self):
        """Test case for emulators_id_put

        Update a Emulator  # noqa: E501
        """
        pass

    def test_emulators_post(self):
        """Test case for emulators_post

        Create a Emulator  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
