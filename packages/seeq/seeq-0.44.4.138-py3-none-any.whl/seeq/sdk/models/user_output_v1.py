# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 0.44.04
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class UserOutputV1(object):
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
        'datasource_name': 'str',
        'description': 'str',
        'email': 'str',
        'first_name': 'str',
        'href': 'str',
        'id': 'str',
        'is_active': 'bool',
        'is_admin': 'bool',
        'is_archived': 'bool',
        'is_enabled': 'bool',
        'is_password_settable': 'bool',
        'last_login_at': 'str',
        'last_name': 'str',
        'name': 'str',
        'status_message': 'str',
        'type': 'str',
        'username': 'str',
        'workbench': 'str'
    }

    attribute_map = {
        'created_at': 'createdAt',
        'datasource_name': 'datasourceName',
        'description': 'description',
        'email': 'email',
        'first_name': 'firstName',
        'href': 'href',
        'id': 'id',
        'is_active': 'isActive',
        'is_admin': 'isAdmin',
        'is_archived': 'isArchived',
        'is_enabled': 'isEnabled',
        'is_password_settable': 'isPasswordSettable',
        'last_login_at': 'lastLoginAt',
        'last_name': 'lastName',
        'name': 'name',
        'status_message': 'statusMessage',
        'type': 'type',
        'username': 'username',
        'workbench': 'workbench'
    }

    def __init__(self, created_at=None, datasource_name=None, description=None, email=None, first_name=None, href=None, id=None, is_active=False, is_admin=False, is_archived=False, is_enabled=False, is_password_settable=False, last_login_at=None, last_name=None, name=None, status_message=None, type=None, username=None, workbench=None):
        """
        UserOutputV1 - a model defined in Swagger
        """

        self._created_at = None
        self._datasource_name = None
        self._description = None
        self._email = None
        self._first_name = None
        self._href = None
        self._id = None
        self._is_active = None
        self._is_admin = None
        self._is_archived = None
        self._is_enabled = None
        self._is_password_settable = None
        self._last_login_at = None
        self._last_name = None
        self._name = None
        self._status_message = None
        self._type = None
        self._username = None
        self._workbench = None

        if created_at is not None:
          self.created_at = created_at
        if datasource_name is not None:
          self.datasource_name = datasource_name
        if description is not None:
          self.description = description
        if email is not None:
          self.email = email
        if first_name is not None:
          self.first_name = first_name
        if href is not None:
          self.href = href
        if id is not None:
          self.id = id
        if is_active is not None:
          self.is_active = is_active
        if is_admin is not None:
          self.is_admin = is_admin
        if is_archived is not None:
          self.is_archived = is_archived
        if is_enabled is not None:
          self.is_enabled = is_enabled
        if is_password_settable is not None:
          self.is_password_settable = is_password_settable
        if last_login_at is not None:
          self.last_login_at = last_login_at
        if last_name is not None:
          self.last_name = last_name
        if name is not None:
          self.name = name
        if status_message is not None:
          self.status_message = status_message
        if type is not None:
          self.type = type
        if username is not None:
          self.username = username
        if workbench is not None:
          self.workbench = workbench

    @property
    def created_at(self):
        """
        Gets the created_at of this UserOutputV1.
        The ISO 8601 date of when the user was created (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :return: The created_at of this UserOutputV1.
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this UserOutputV1.
        The ISO 8601 date of when the user was created (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :param created_at: The created_at of this UserOutputV1.
        :type: str
        """

        self._created_at = created_at

    @property
    def datasource_name(self):
        """
        Gets the datasource_name of this UserOutputV1.
        The name of the data source (authentication directory) containing the user

        :return: The datasource_name of this UserOutputV1.
        :rtype: str
        """
        return self._datasource_name

    @datasource_name.setter
    def datasource_name(self, datasource_name):
        """
        Sets the datasource_name of this UserOutputV1.
        The name of the data source (authentication directory) containing the user

        :param datasource_name: The datasource_name of this UserOutputV1.
        :type: str
        """

        self._datasource_name = datasource_name

    @property
    def description(self):
        """
        Gets the description of this UserOutputV1.
        Clarifying information or other plain language description of this item

        :return: The description of this UserOutputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UserOutputV1.
        Clarifying information or other plain language description of this item

        :param description: The description of this UserOutputV1.
        :type: str
        """

        self._description = description

    @property
    def email(self):
        """
        Gets the email of this UserOutputV1.
        The email address of the user

        :return: The email of this UserOutputV1.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this UserOutputV1.
        The email address of the user

        :param email: The email of this UserOutputV1.
        :type: str
        """

        self._email = email

    @property
    def first_name(self):
        """
        Gets the first_name of this UserOutputV1.
        The first name of the user

        :return: The first_name of this UserOutputV1.
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """
        Sets the first_name of this UserOutputV1.
        The first name of the user

        :param first_name: The first_name of this UserOutputV1.
        :type: str
        """

        self._first_name = first_name

    @property
    def href(self):
        """
        Gets the href of this UserOutputV1.
        The href that can be used to interact with the item

        :return: The href of this UserOutputV1.
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """
        Sets the href of this UserOutputV1.
        The href that can be used to interact with the item

        :param href: The href of this UserOutputV1.
        :type: str
        """
        if href is None:
            raise ValueError("Invalid value for `href`, must not be `None`")

        self._href = href

    @property
    def id(self):
        """
        Gets the id of this UserOutputV1.
        The ID that can be used to interact with the item

        :return: The id of this UserOutputV1.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this UserOutputV1.
        The ID that can be used to interact with the item

        :param id: The id of this UserOutputV1.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def is_active(self):
        """
        Gets the is_active of this UserOutputV1.
        Whether the user is actively using Seeq

        :return: The is_active of this UserOutputV1.
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """
        Sets the is_active of this UserOutputV1.
        Whether the user is actively using Seeq

        :param is_active: The is_active of this UserOutputV1.
        :type: bool
        """

        self._is_active = is_active

    @property
    def is_admin(self):
        """
        Gets the is_admin of this UserOutputV1.
        Whether the user has administrator capabilities in Seeq

        :return: The is_admin of this UserOutputV1.
        :rtype: bool
        """
        return self._is_admin

    @is_admin.setter
    def is_admin(self, is_admin):
        """
        Sets the is_admin of this UserOutputV1.
        Whether the user has administrator capabilities in Seeq

        :param is_admin: The is_admin of this UserOutputV1.
        :type: bool
        """

        self._is_admin = is_admin

    @property
    def is_archived(self):
        """
        Gets the is_archived of this UserOutputV1.
        Whether item is isArchived

        :return: The is_archived of this UserOutputV1.
        :rtype: bool
        """
        return self._is_archived

    @is_archived.setter
    def is_archived(self, is_archived):
        """
        Sets the is_archived of this UserOutputV1.
        Whether item is isArchived

        :param is_archived: The is_archived of this UserOutputV1.
        :type: bool
        """

        self._is_archived = is_archived

    @property
    def is_enabled(self):
        """
        Gets the is_enabled of this UserOutputV1.
        Whether the user is enabled

        :return: The is_enabled of this UserOutputV1.
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """
        Sets the is_enabled of this UserOutputV1.
        Whether the user is enabled

        :param is_enabled: The is_enabled of this UserOutputV1.
        :type: bool
        """

        self._is_enabled = is_enabled

    @property
    def is_password_settable(self):
        """
        Gets the is_password_settable of this UserOutputV1.
        Whether the user's password may be updated

        :return: The is_password_settable of this UserOutputV1.
        :rtype: bool
        """
        return self._is_password_settable

    @is_password_settable.setter
    def is_password_settable(self, is_password_settable):
        """
        Sets the is_password_settable of this UserOutputV1.
        Whether the user's password may be updated

        :param is_password_settable: The is_password_settable of this UserOutputV1.
        :type: bool
        """

        self._is_password_settable = is_password_settable

    @property
    def last_login_at(self):
        """
        Gets the last_login_at of this UserOutputV1.
        The ISO 8601 date of when the user last logged in (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :return: The last_login_at of this UserOutputV1.
        :rtype: str
        """
        return self._last_login_at

    @last_login_at.setter
    def last_login_at(self, last_login_at):
        """
        Sets the last_login_at of this UserOutputV1.
        The ISO 8601 date of when the user last logged in (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :param last_login_at: The last_login_at of this UserOutputV1.
        :type: str
        """

        self._last_login_at = last_login_at

    @property
    def last_name(self):
        """
        Gets the last_name of this UserOutputV1.
        The last name of the user

        :return: The last_name of this UserOutputV1.
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """
        Sets the last_name of this UserOutputV1.
        The last name of the user

        :param last_name: The last_name of this UserOutputV1.
        :type: str
        """

        self._last_name = last_name

    @property
    def name(self):
        """
        Gets the name of this UserOutputV1.
        The human readable name

        :return: The name of this UserOutputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this UserOutputV1.
        The human readable name

        :param name: The name of this UserOutputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def status_message(self):
        """
        Gets the status_message of this UserOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :return: The status_message of this UserOutputV1.
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """
        Sets the status_message of this UserOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :param status_message: The status_message of this UserOutputV1.
        :type: str
        """

        self._status_message = status_message

    @property
    def type(self):
        """
        Gets the type of this UserOutputV1.
        The type of the item

        :return: The type of this UserOutputV1.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this UserOutputV1.
        The type of the item

        :param type: The type of this UserOutputV1.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")

        self._type = type

    @property
    def username(self):
        """
        Gets the username of this UserOutputV1.
        The username of the user

        :return: The username of this UserOutputV1.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this UserOutputV1.
        The username of the user

        :param username: The username of this UserOutputV1.
        :type: str
        """

        self._username = username

    @property
    def workbench(self):
        """
        Gets the workbench of this UserOutputV1.
        The workbench configuration of the user

        :return: The workbench of this UserOutputV1.
        :rtype: str
        """
        return self._workbench

    @workbench.setter
    def workbench(self, workbench):
        """
        Sets the workbench of this UserOutputV1.
        The workbench configuration of the user

        :param workbench: The workbench of this UserOutputV1.
        :type: str
        """

        self._workbench = workbench

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
        if not isinstance(other, UserOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
