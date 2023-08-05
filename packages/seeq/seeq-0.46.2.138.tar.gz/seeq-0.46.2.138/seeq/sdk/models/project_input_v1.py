# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 0.46.02-BETA
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ProjectInputV1(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'description': 'str',
        'folder_id': 'str',
        'name': 'str',
        'owner_id': 'str'
    }

    attribute_map = {
        'description': 'description',
        'folder_id': 'folderId',
        'name': 'name',
        'owner_id': 'ownerId'
    }

    def __init__(self, description=None, folder_id=None, name=None, owner_id=None):
        """
        ProjectInputV1 - a model defined in Swagger
        """

        self._description = None
        self._folder_id = None
        self._name = None
        self._owner_id = None

        if description is not None:
          self.description = description
        if folder_id is not None:
          self.folder_id = folder_id
        if name is not None:
          self.name = name
        if owner_id is not None:
          self.owner_id = owner_id

    @property
    def description(self):
        """
        Gets the description of this ProjectInputV1.
        Clarifying information or other plain language description of this asset. An input of just whitespace is equivalent to a null input.

        :return: The description of this ProjectInputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ProjectInputV1.
        Clarifying information or other plain language description of this asset. An input of just whitespace is equivalent to a null input.

        :param description: The description of this ProjectInputV1.
        :type: str
        """

        self._description = description

    @property
    def folder_id(self):
        """
        Gets the folder_id of this ProjectInputV1.
        The id of the folder to place the new project into. If null, the project will be created at the root level.

        :return: The folder_id of this ProjectInputV1.
        :rtype: str
        """
        return self._folder_id

    @folder_id.setter
    def folder_id(self, folder_id):
        """
        Sets the folder_id of this ProjectInputV1.
        The id of the folder to place the new project into. If null, the project will be created at the root level.

        :param folder_id: The folder_id of this ProjectInputV1.
        :type: str
        """

        self._folder_id = folder_id

    @property
    def name(self):
        """
        Gets the name of this ProjectInputV1.
        Human readable name. Null or whitespace names are not permitted.

        :return: The name of this ProjectInputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ProjectInputV1.
        Human readable name. Null or whitespace names are not permitted.

        :param name: The name of this ProjectInputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def owner_id(self):
        """
        Gets the owner_id of this ProjectInputV1.
        The ID of the User that owns this project. If omitted when creating a new project, the authenticated user is used by default.

        :return: The owner_id of this ProjectInputV1.
        :rtype: str
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id):
        """
        Sets the owner_id of this ProjectInputV1.
        The ID of the User that owns this project. If omitted when creating a new project, the authenticated user is used by default.

        :param owner_id: The owner_id of this ProjectInputV1.
        :type: str
        """

        self._owner_id = owner_id

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
        if not isinstance(other, ProjectInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
