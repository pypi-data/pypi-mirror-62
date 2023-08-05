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
from modelcatalog.api.geo_coordinates_api import GeoCoordinatesApi  # noqa: E501
from modelcatalog.rest import ApiException


class TestGeoCoordinatesApi(unittest.TestCase):
    """GeoCoordinatesApi unit test stubs"""

    def setUp(self):
        self.api = modelcatalog.api.geo_coordinates_api.GeoCoordinatesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_geocoordinatess_get(self):
        """Test case for geocoordinatess_get

        List all GeoCoordinates entities  # noqa: E501
        """
        pass

    def test_geocoordinatess_id_delete(self):
        """Test case for geocoordinatess_id_delete

        Delete a GeoCoordinates  # noqa: E501
        """
        pass

    def test_geocoordinatess_id_get(self):
        """Test case for geocoordinatess_id_get

        Get a GeoCoordinates  # noqa: E501
        """
        pass

    def test_geocoordinatess_id_put(self):
        """Test case for geocoordinatess_id_put

        Update a GeoCoordinates  # noqa: E501
        """
        pass

    def test_geocoordinatess_post(self):
        """Test case for geocoordinatess_post

        Create a GeoCoordinates  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
