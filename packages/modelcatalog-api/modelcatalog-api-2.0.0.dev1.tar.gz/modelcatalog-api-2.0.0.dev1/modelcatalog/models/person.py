# coding: utf-8

"""
    Model Catalog

    This is the API of the  Software Description Ontology at [https://mintproject.github.io/Mint-ModelCatalog-Ontology/release/1.3.0/index-en.html](https://w3id.org/okn/o/sdm)  # noqa: E501

    OpenAPI spec version: v1.3.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class Person(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'identifier': 'list[str]',
        'website': 'list[str]',
        'description': 'list[str]',
        'id': 'str',
        'label': 'list[str]',
        'type': 'list[str]',
        'email': 'list[str]'
    }

    attribute_map = {
        'identifier': 'identifier',
        'website': 'website',
        'description': 'description',
        'id': 'id',
        'label': 'label',
        'type': 'type',
        'email': 'email'
    }

    def __init__(self, identifier=None, website=None, description=None, id=None, label=None, type=None, email=None):  # noqa: E501
        """Person - a model defined in OpenAPI"""  # noqa: E501

        self._identifier = None
        self._website = None
        self._description = None
        self._id = None
        self._label = None
        self._type = None
        self._email = None
        self.discriminator = None

        if identifier is not None:
            self.identifier = identifier
        else:
            if hasattr(self, '_identifier'): del self._identifier
            if hasattr(self.attribute_map, 'identifier'): del self.attribute_map['identifier']
            if hasattr(self.openapi_types, 'identifier'): del self.openapi_types['identifier']
        if website is not None:
            self.website = website
        else:
            if hasattr(self, '_website'): del self._website
            if hasattr(self.attribute_map, 'website'): del self.attribute_map['website']
            if hasattr(self.openapi_types, 'website'): del self.openapi_types['website']
        if description is not None:
            self.description = description
        else:
            if hasattr(self, '_description'): del self._description
            if hasattr(self.attribute_map, 'description'): del self.attribute_map['description']
            if hasattr(self.openapi_types, 'description'): del self.openapi_types['description']
        if id is not None:
            self.id = id
        if label is not None:
            self.label = label
        else:
            if hasattr(self, '_label'): del self._label
            if hasattr(self.attribute_map, 'label'): del self.attribute_map['label']
            if hasattr(self.openapi_types, 'label'): del self.openapi_types['label']
        if type is not None:
            self.type = type
        else:
            if hasattr(self, '_type'): del self._type
            if hasattr(self.attribute_map, 'type'): del self.attribute_map['type']
            if hasattr(self.openapi_types, 'type'): del self.openapi_types['type']
        if email is not None:
            self.email = email
        else:
            if hasattr(self, '_email'): del self._email
            if hasattr(self.attribute_map, 'email'): del self.attribute_map['email']
            if hasattr(self.openapi_types, 'email'): del self.openapi_types['email']

    @property
    def identifier(self):
        """Gets the identifier of this Person.  # noqa: E501


        :return: The identifier of this Person.  # noqa: E501
        :rtype: list[str]
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this Person.


        :param identifier: The identifier of this Person.  # noqa: E501
        :type: list[str]
        """

        self._identifier = identifier

    @property
    def website(self):
        """Gets the website of this Person.  # noqa: E501


        :return: The website of this Person.  # noqa: E501
        :rtype: list[str]
        """
        return self._website

    @website.setter
    def website(self, website):
        """Sets the website of this Person.


        :param website: The website of this Person.  # noqa: E501
        :type: list[str]
        """

        self._website = website

    @property
    def description(self):
        """Gets the description of this Person.  # noqa: E501


        :return: The description of this Person.  # noqa: E501
        :rtype: list[str]
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Person.


        :param description: The description of this Person.  # noqa: E501
        :type: list[str]
        """

        self._description = description

    @property
    def id(self):
        """Gets the id of this Person.  # noqa: E501


        :return: The id of this Person.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Person.


        :param id: The id of this Person.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def label(self):
        """Gets the label of this Person.  # noqa: E501


        :return: The label of this Person.  # noqa: E501
        :rtype: list[str]
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this Person.


        :param label: The label of this Person.  # noqa: E501
        :type: list[str]
        """

        self._label = label

    @property
    def type(self):
        """Gets the type of this Person.  # noqa: E501


        :return: The type of this Person.  # noqa: E501
        :rtype: list[str]
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Person.


        :param type: The type of this Person.  # noqa: E501
        :type: list[str]
        """

        self._type = type

    @property
    def email(self):
        """Gets the email of this Person.  # noqa: E501


        :return: The email of this Person.  # noqa: E501
        :rtype: list[str]
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this Person.


        :param email: The email of this Person.  # noqa: E501
        :type: list[str]
        """

        self._email = email

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            if hasattr(self, attr):
                value = getattr(self, attr)
            else:
                continue                
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Person):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
