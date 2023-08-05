# coding: utf-8

"""
    Red Rover API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1
    Contact: contact@edustaff.org
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from redrover_api.configuration import Configuration


class AttributeDto(object):
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
        'id': 'int',
        'name': 'str',
        'external_id': 'str',
        'active': 'bool',
        'description': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'external_id': 'externalId',
        'active': 'active',
        'description': 'description'
    }

    def __init__(self, id=None, name=None, external_id=None, active=None, description=None, local_vars_configuration=None):  # noqa: E501
        """AttributeDto - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._external_id = None
        self._active = None
        self._description = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if external_id is not None:
            self.external_id = external_id
        if active is not None:
            self.active = active
        if description is not None:
            self.description = description

    @property
    def id(self):
        """Gets the id of this AttributeDto.  # noqa: E501


        :return: The id of this AttributeDto.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AttributeDto.


        :param id: The id of this AttributeDto.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this AttributeDto.  # noqa: E501


        :return: The name of this AttributeDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AttributeDto.


        :param name: The name of this AttributeDto.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def external_id(self):
        """Gets the external_id of this AttributeDto.  # noqa: E501


        :return: The external_id of this AttributeDto.  # noqa: E501
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """Sets the external_id of this AttributeDto.


        :param external_id: The external_id of this AttributeDto.  # noqa: E501
        :type: str
        """

        self._external_id = external_id

    @property
    def active(self):
        """Gets the active of this AttributeDto.  # noqa: E501


        :return: The active of this AttributeDto.  # noqa: E501
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this AttributeDto.


        :param active: The active of this AttributeDto.  # noqa: E501
        :type: bool
        """

        self._active = active

    @property
    def description(self):
        """Gets the description of this AttributeDto.  # noqa: E501


        :return: The description of this AttributeDto.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AttributeDto.


        :param description: The description of this AttributeDto.  # noqa: E501
        :type: str
        """

        self._description = description

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
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
        if not isinstance(other, AttributeDto):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AttributeDto):
            return True

        return self.to_dict() != other.to_dict()
