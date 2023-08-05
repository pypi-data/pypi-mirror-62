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
from modelcatalog.api.sample_resource_api import SampleResourceApi  # noqa: E501
from modelcatalog.rest import ApiException


class TestSampleResourceApi(unittest.TestCase):
    """SampleResourceApi unit test stubs"""

    def setUp(self):
        self.api = modelcatalog.api.sample_resource_api.SampleResourceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_sampleresources_get(self):
        """Test case for sampleresources_get

        List all SampleResource entities  # noqa: E501
        """
        pass

    def test_sampleresources_id_delete(self):
        """Test case for sampleresources_id_delete

        Delete a SampleResource  # noqa: E501
        """
        pass

    def test_sampleresources_id_get(self):
        """Test case for sampleresources_id_get

        Get a SampleResource  # noqa: E501
        """
        pass

    def test_sampleresources_id_put(self):
        """Test case for sampleresources_id_put

        Update a SampleResource  # noqa: E501
        """
        pass

    def test_sampleresources_post(self):
        """Test case for sampleresources_post

        Create a SampleResource  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
