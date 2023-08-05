# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 0.45.02
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class WorkstepOutputV1(object):
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
        'created_at': 'str',
        'data': 'str',
        'description': 'str',
        'effective_permissions': 'PermissionsV1',
        'href': 'str',
        'id': 'str',
        'is_archived': 'bool',
        'is_redacted': 'bool',
        'last': 'str',
        'name': 'str',
        'next': 'str',
        'previous': 'str',
        'status_message': 'str',
        'type': 'str'
    }

    attribute_map = {
        'created_at': 'createdAt',
        'data': 'data',
        'description': 'description',
        'effective_permissions': 'effectivePermissions',
        'href': 'href',
        'id': 'id',
        'is_archived': 'isArchived',
        'is_redacted': 'isRedacted',
        'last': 'last',
        'name': 'name',
        'next': 'next',
        'previous': 'previous',
        'status_message': 'statusMessage',
        'type': 'type'
    }

    def __init__(self, created_at=None, data=None, description=None, effective_permissions=None, href=None, id=None, is_archived=False, is_redacted=False, last=None, name=None, next=None, previous=None, status_message=None, type=None):
        """
        WorkstepOutputV1 - a model defined in Swagger
        """

        self._created_at = None
        self._data = None
        self._description = None
        self._effective_permissions = None
        self._href = None
        self._id = None
        self._is_archived = None
        self._is_redacted = None
        self._last = None
        self._name = None
        self._next = None
        self._previous = None
        self._status_message = None
        self._type = None

        if created_at is not None:
          self.created_at = created_at
        if data is not None:
          self.data = data
        if description is not None:
          self.description = description
        if effective_permissions is not None:
          self.effective_permissions = effective_permissions
        if href is not None:
          self.href = href
        if id is not None:
          self.id = id
        if is_archived is not None:
          self.is_archived = is_archived
        if is_redacted is not None:
          self.is_redacted = is_redacted
        if last is not None:
          self.last = last
        if name is not None:
          self.name = name
        if next is not None:
          self.next = next
        if previous is not None:
          self.previous = previous
        if status_message is not None:
          self.status_message = status_message
        if type is not None:
          self.type = type

    @property
    def created_at(self):
        """
        Gets the created_at of this WorkstepOutputV1.
        The ISO 8601 date of when the workstep was created (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :return: The created_at of this WorkstepOutputV1.
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this WorkstepOutputV1.
        The ISO 8601 date of when the workstep was created (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :param created_at: The created_at of this WorkstepOutputV1.
        :type: str
        """

        self._created_at = created_at

    @property
    def data(self):
        """
        Gets the data of this WorkstepOutputV1.
        JSON-encoded state for this workstep

        :return: The data of this WorkstepOutputV1.
        :rtype: str
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Sets the data of this WorkstepOutputV1.
        JSON-encoded state for this workstep

        :param data: The data of this WorkstepOutputV1.
        :type: str
        """
        if data is None:
            raise ValueError("Invalid value for `data`, must not be `None`")

        self._data = data

    @property
    def description(self):
        """
        Gets the description of this WorkstepOutputV1.
        Clarifying information or other plain language description of this item

        :return: The description of this WorkstepOutputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this WorkstepOutputV1.
        Clarifying information or other plain language description of this item

        :param description: The description of this WorkstepOutputV1.
        :type: str
        """

        self._description = description

    @property
    def effective_permissions(self):
        """
        Gets the effective_permissions of this WorkstepOutputV1.
        The permissions the current user has to the item.

        :return: The effective_permissions of this WorkstepOutputV1.
        :rtype: PermissionsV1
        """
        return self._effective_permissions

    @effective_permissions.setter
    def effective_permissions(self, effective_permissions):
        """
        Sets the effective_permissions of this WorkstepOutputV1.
        The permissions the current user has to the item.

        :param effective_permissions: The effective_permissions of this WorkstepOutputV1.
        :type: PermissionsV1
        """

        self._effective_permissions = effective_permissions

    @property
    def href(self):
        """
        Gets the href of this WorkstepOutputV1.
        The href that can be used to interact with the item

        :return: The href of this WorkstepOutputV1.
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """
        Sets the href of this WorkstepOutputV1.
        The href that can be used to interact with the item

        :param href: The href of this WorkstepOutputV1.
        :type: str
        """
        if href is None:
            raise ValueError("Invalid value for `href`, must not be `None`")

        self._href = href

    @property
    def id(self):
        """
        Gets the id of this WorkstepOutputV1.
        The ID that can be used to interact with the item

        :return: The id of this WorkstepOutputV1.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WorkstepOutputV1.
        The ID that can be used to interact with the item

        :param id: The id of this WorkstepOutputV1.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def is_archived(self):
        """
        Gets the is_archived of this WorkstepOutputV1.
        Whether item is archived

        :return: The is_archived of this WorkstepOutputV1.
        :rtype: bool
        """
        return self._is_archived

    @is_archived.setter
    def is_archived(self, is_archived):
        """
        Sets the is_archived of this WorkstepOutputV1.
        Whether item is archived

        :param is_archived: The is_archived of this WorkstepOutputV1.
        :type: bool
        """

        self._is_archived = is_archived

    @property
    def is_redacted(self):
        """
        Gets the is_redacted of this WorkstepOutputV1.
        Whether item is redacted

        :return: The is_redacted of this WorkstepOutputV1.
        :rtype: bool
        """
        return self._is_redacted

    @is_redacted.setter
    def is_redacted(self, is_redacted):
        """
        Sets the is_redacted of this WorkstepOutputV1.
        Whether item is redacted

        :param is_redacted: The is_redacted of this WorkstepOutputV1.
        :type: bool
        """

        self._is_redacted = is_redacted

    @property
    def last(self):
        """
        Gets the last of this WorkstepOutputV1.
        The href that can be used to interact with the last workstep or null if there is not one

        :return: The last of this WorkstepOutputV1.
        :rtype: str
        """
        return self._last

    @last.setter
    def last(self, last):
        """
        Sets the last of this WorkstepOutputV1.
        The href that can be used to interact with the last workstep or null if there is not one

        :param last: The last of this WorkstepOutputV1.
        :type: str
        """

        self._last = last

    @property
    def name(self):
        """
        Gets the name of this WorkstepOutputV1.
        The human readable name

        :return: The name of this WorkstepOutputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this WorkstepOutputV1.
        The human readable name

        :param name: The name of this WorkstepOutputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def next(self):
        """
        Gets the next of this WorkstepOutputV1.
        The href that can be used to interact with the next workstep or null if there is not one

        :return: The next of this WorkstepOutputV1.
        :rtype: str
        """
        return self._next

    @next.setter
    def next(self, next):
        """
        Sets the next of this WorkstepOutputV1.
        The href that can be used to interact with the next workstep or null if there is not one

        :param next: The next of this WorkstepOutputV1.
        :type: str
        """

        self._next = next

    @property
    def previous(self):
        """
        Gets the previous of this WorkstepOutputV1.
        The href that can be used to interact with the previous workstep or null if there is not one

        :return: The previous of this WorkstepOutputV1.
        :rtype: str
        """
        return self._previous

    @previous.setter
    def previous(self, previous):
        """
        Sets the previous of this WorkstepOutputV1.
        The href that can be used to interact with the previous workstep or null if there is not one

        :param previous: The previous of this WorkstepOutputV1.
        :type: str
        """

        self._previous = previous

    @property
    def status_message(self):
        """
        Gets the status_message of this WorkstepOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :return: The status_message of this WorkstepOutputV1.
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """
        Sets the status_message of this WorkstepOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :param status_message: The status_message of this WorkstepOutputV1.
        :type: str
        """

        self._status_message = status_message

    @property
    def type(self):
        """
        Gets the type of this WorkstepOutputV1.
        The type of the item

        :return: The type of this WorkstepOutputV1.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this WorkstepOutputV1.
        The type of the item

        :param type: The type of this WorkstepOutputV1.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")

        self._type = type

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
        if not isinstance(other, WorkstepOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
