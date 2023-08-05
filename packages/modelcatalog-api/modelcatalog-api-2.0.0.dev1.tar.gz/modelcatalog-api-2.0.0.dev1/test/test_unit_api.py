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
from modelcatalog.api.unit_api import UnitApi  # noqa: E501
from modelcatalog.rest import ApiException


class TestUnitApi(unittest.TestCase):
    """UnitApi unit test stubs"""

    def setUp(self):
        self.api = modelcatalog.api.unit_api.UnitApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_units_get(self):
        """Test case for units_get

        List all Unit entities  # noqa: E501
        """
        pass

    def test_units_id_delete(self):
        """Test case for units_id_delete

        Delete a Unit  # noqa: E501
        """
        pass

    def test_units_id_get(self):
        """Test case for units_id_get

        Get a Unit  # noqa: E501
        """
        pass

    def test_units_id_put(self):
        """Test case for units_id_put

        Update a Unit  # noqa: E501
        """
        pass

    def test_units_post(self):
        """Test case for units_post

        Create a Unit  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
