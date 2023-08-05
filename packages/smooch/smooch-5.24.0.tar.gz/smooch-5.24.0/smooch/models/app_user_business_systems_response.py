# coding: utf-8

"""
    Smooch

    The Smooch API is a unified interface for powering messaging in your customer experiences across every channel. Our API speeds access to new markets, reduces time to ship, eliminates complexity, and helps you build the best experiences for your customers. For more information, visit our [official documentation](https://docs.smooch.io).

    OpenAPI spec version: 5.24
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class AppUserBusinessSystemsResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, business_systems=None):
        """
        AppUserBusinessSystemsResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'business_systems': 'list[BusinessSystemItem]'
        }

        self.attribute_map = {
            'business_systems': 'businessSystems'
        }

        self._business_systems = None

        # TODO: let required properties as mandatory parameter in the constructor.
        #       - to check if required property is not None (e.g. by calling setter)
        #       - ApiClient.__deserialize_model has to be adapted as well
        if business_systems is not None:
          self.business_systems = business_systems

    @property
    def business_systems(self):
        """
        Gets the business_systems of this AppUserBusinessSystemsResponse.
        An array of objects containing the business system type and the id.

        :return: The business_systems of this AppUserBusinessSystemsResponse.
        :rtype: list[BusinessSystemItem]
        """
        return self._business_systems

    @business_systems.setter
    def business_systems(self, business_systems):
        """
        Sets the business_systems of this AppUserBusinessSystemsResponse.
        An array of objects containing the business system type and the id.

        :param business_systems: The business_systems of this AppUserBusinessSystemsResponse.
        :type: list[BusinessSystemItem]
        """
        if business_systems is None:
            raise ValueError("Invalid value for `business_systems`, must not be `None`")

        self._business_systems = business_systems

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, AppUserBusinessSystemsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
