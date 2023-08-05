# coding: utf-8

"""
    Model Catalog

    This is the API of the  Software Description Ontology at [https://mintproject.github.io/Mint-ModelCatalog-Ontology/release/1.2.0/index-en.html](https://w3id.org/okn/o/sdm)  # noqa: E501

    OpenAPI spec version: v1.2.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import modelcatalog
from modelcatalog.api.intervention_api import InterventionApi  # noqa: E501
from modelcatalog.rest import ApiException


class TestInterventionApi(unittest.TestCase):
    """InterventionApi unit test stubs"""

    def setUp(self):
        self.api = modelcatalog.api.intervention_api.InterventionApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_interventions_get(self):
        """Test case for interventions_get

        List all Intervention entities  # noqa: E501
        """
        pass

    def test_interventions_id_delete(self):
        """Test case for interventions_id_delete

        Delete a Intervention  # noqa: E501
        """
        pass

    def test_interventions_id_get(self):
        """Test case for interventions_id_get

        Get a Intervention  # noqa: E501
        """
        pass

    def test_interventions_id_put(self):
        """Test case for interventions_id_put

        Update a Intervention  # noqa: E501
        """
        pass

    def test_interventions_post(self):
        """Test case for interventions_post

        Create a Intervention  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
