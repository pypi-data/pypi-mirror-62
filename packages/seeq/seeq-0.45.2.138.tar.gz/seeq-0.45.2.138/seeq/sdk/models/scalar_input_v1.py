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


class ScalarInputV1(object):
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
        'data_id': 'str',
        'description': 'str',
        'formula': 'str',
        'name': 'str',
        'number_format': 'str',
        'parameters': 'list[str]',
        'properties': 'list[ScalarPropertyV1]',
        'scoped_to': 'str',
        'security_string': 'str',
        'source_security_string': 'str',
        'sync_token': 'str',
        'unit_of_measure': 'str'
    }

    attribute_map = {
        'data_id': 'dataId',
        'description': 'description',
        'formula': 'formula',
        'name': 'name',
        'number_format': 'numberFormat',
        'parameters': 'parameters',
        'properties': 'properties',
        'scoped_to': 'scopedTo',
        'security_string': 'securityString',
        'source_security_string': 'sourceSecurityString',
        'sync_token': 'syncToken',
        'unit_of_measure': 'unitOfMeasure'
    }

    def __init__(self, data_id=None, description=None, formula=None, name=None, number_format=None, parameters=None, properties=None, scoped_to=None, security_string=None, source_security_string=None, sync_token=None, unit_of_measure=None):
        """
        ScalarInputV1 - a model defined in Swagger
        """

        self._data_id = None
        self._description = None
        self._formula = None
        self._name = None
        self._number_format = None
        self._parameters = None
        self._properties = None
        self._scoped_to = None
        self._security_string = None
        self._source_security_string = None
        self._sync_token = None
        self._unit_of_measure = None

        if data_id is not None:
          self.data_id = data_id
        if description is not None:
          self.description = description
        if formula is not None:
          self.formula = formula
        if name is not None:
          self.name = name
        if number_format is not None:
          self.number_format = number_format
        if parameters is not None:
          self.parameters = parameters
        if properties is not None:
          self.properties = properties
        if scoped_to is not None:
          self.scoped_to = scoped_to
        if security_string is not None:
          self.security_string = security_string
        if source_security_string is not None:
          self.source_security_string = source_security_string
        if sync_token is not None:
          self.sync_token = sync_token
        if unit_of_measure is not None:
          self.unit_of_measure = unit_of_measure

    @property
    def data_id(self):
        """
        Gets the data_id of this ScalarInputV1.
        The data ID of this asset. Note: This is not the Seeq ID, but the unique identifier that the remote datasource uses.

        :return: The data_id of this ScalarInputV1.
        :rtype: str
        """
        return self._data_id

    @data_id.setter
    def data_id(self, data_id):
        """
        Sets the data_id of this ScalarInputV1.
        The data ID of this asset. Note: This is not the Seeq ID, but the unique identifier that the remote datasource uses.

        :param data_id: The data_id of this ScalarInputV1.
        :type: str
        """
        if data_id is None:
            raise ValueError("Invalid value for `data_id`, must not be `None`")

        self._data_id = data_id

    @property
    def description(self):
        """
        Gets the description of this ScalarInputV1.
        Clarifying information or other plain language description of this asset. An input of just whitespace is equivalent to a null input.

        :return: The description of this ScalarInputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ScalarInputV1.
        Clarifying information or other plain language description of this asset. An input of just whitespace is equivalent to a null input.

        :param description: The description of this ScalarInputV1.
        :type: str
        """

        self._description = description

    @property
    def formula(self):
        """
        Gets the formula of this ScalarInputV1.
        Information about the formula used to create a calculated scalar

        :return: The formula of this ScalarInputV1.
        :rtype: str
        """
        return self._formula

    @formula.setter
    def formula(self, formula):
        """
        Sets the formula of this ScalarInputV1.
        Information about the formula used to create a calculated scalar

        :param formula: The formula of this ScalarInputV1.
        :type: str
        """
        if formula is None:
            raise ValueError("Invalid value for `formula`, must not be `None`")

        self._formula = formula

    @property
    def name(self):
        """
        Gets the name of this ScalarInputV1.
        Human readable name. Null or whitespace names are not permitted.

        :return: The name of this ScalarInputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ScalarInputV1.
        Human readable name. Null or whitespace names are not permitted.

        :param name: The name of this ScalarInputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def number_format(self):
        """
        Gets the number_format of this ScalarInputV1.
        The format string used for numbers associated with this signal. The format for the string follows ECMA-376 spreadsheet format standards.

        :return: The number_format of this ScalarInputV1.
        :rtype: str
        """
        return self._number_format

    @number_format.setter
    def number_format(self, number_format):
        """
        Sets the number_format of this ScalarInputV1.
        The format string used for numbers associated with this signal. The format for the string follows ECMA-376 spreadsheet format standards.

        :param number_format: The number_format of this ScalarInputV1.
        :type: str
        """

        self._number_format = number_format

    @property
    def parameters(self):
        """
        Gets the parameters of this ScalarInputV1.
        The parameters for the formula used to create a calculated scalar. Each parameter should have a format of 'name=id' where 'name' is the variable identifier, without the leading $ sign, and 'id' is the ID of the item referenced by the variable

        :return: The parameters of this ScalarInputV1.
        :rtype: list[str]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this ScalarInputV1.
        The parameters for the formula used to create a calculated scalar. Each parameter should have a format of 'name=id' where 'name' is the variable identifier, without the leading $ sign, and 'id' is the ID of the item referenced by the variable

        :param parameters: The parameters of this ScalarInputV1.
        :type: list[str]
        """
        if parameters is None:
            raise ValueError("Invalid value for `parameters`, must not be `None`")

        self._parameters = parameters

    @property
    def properties(self):
        """
        Gets the properties of this ScalarInputV1.
        Properties to set on this scalar. A property consists of a name, a value, and a unit of measure.

        :return: The properties of this ScalarInputV1.
        :rtype: list[ScalarPropertyV1]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this ScalarInputV1.
        Properties to set on this scalar. A property consists of a name, a value, and a unit of measure.

        :param properties: The properties of this ScalarInputV1.
        :type: list[ScalarPropertyV1]
        """

        self._properties = properties

    @property
    def scoped_to(self):
        """
        Gets the scoped_to of this ScalarInputV1.
        The ID of the workbook to which this scalar will be scoped.

        :return: The scoped_to of this ScalarInputV1.
        :rtype: str
        """
        return self._scoped_to

    @scoped_to.setter
    def scoped_to(self, scoped_to):
        """
        Sets the scoped_to of this ScalarInputV1.
        The ID of the workbook to which this scalar will be scoped.

        :param scoped_to: The scoped_to of this ScalarInputV1.
        :type: str
        """

        self._scoped_to = scoped_to

    @property
    def security_string(self):
        """
        Gets the security_string of this ScalarInputV1.
        Security string containing all identities and their permissions for the item. If set, permissions can only be managed by the connector and not in Seeq.

        :return: The security_string of this ScalarInputV1.
        :rtype: str
        """
        return self._security_string

    @security_string.setter
    def security_string(self, security_string):
        """
        Sets the security_string of this ScalarInputV1.
        Security string containing all identities and their permissions for the item. If set, permissions can only be managed by the connector and not in Seeq.

        :param security_string: The security_string of this ScalarInputV1.
        :type: str
        """

        self._security_string = security_string

    @property
    def source_security_string(self):
        """
        Gets the source_security_string of this ScalarInputV1.
        The security string as it was originally found on the source (for debugging ACLs only)

        :return: The source_security_string of this ScalarInputV1.
        :rtype: str
        """
        return self._source_security_string

    @source_security_string.setter
    def source_security_string(self, source_security_string):
        """
        Sets the source_security_string of this ScalarInputV1.
        The security string as it was originally found on the source (for debugging ACLs only)

        :param source_security_string: The source_security_string of this ScalarInputV1.
        :type: str
        """

        self._source_security_string = source_security_string

    @property
    def sync_token(self):
        """
        Gets the sync_token of this ScalarInputV1.
        An arbitrary token (often a date or random ID) that is used during metadata syncs. At the end of a full sync, items with mismatching sync tokens are identified as stale and may be archived using the Datasources clean-up API.

        :return: The sync_token of this ScalarInputV1.
        :rtype: str
        """
        return self._sync_token

    @sync_token.setter
    def sync_token(self, sync_token):
        """
        Sets the sync_token of this ScalarInputV1.
        An arbitrary token (often a date or random ID) that is used during metadata syncs. At the end of a full sync, items with mismatching sync tokens are identified as stale and may be archived using the Datasources clean-up API.

        :param sync_token: The sync_token of this ScalarInputV1.
        :type: str
        """

        self._sync_token = sync_token

    @property
    def unit_of_measure(self):
        """
        Gets the unit_of_measure of this ScalarInputV1.
        The unit of measure for this Scalar. Added to its formula if parsable by Seeq

        :return: The unit_of_measure of this ScalarInputV1.
        :rtype: str
        """
        return self._unit_of_measure

    @unit_of_measure.setter
    def unit_of_measure(self, unit_of_measure):
        """
        Sets the unit_of_measure of this ScalarInputV1.
        The unit of measure for this Scalar. Added to its formula if parsable by Seeq

        :param unit_of_measure: The unit_of_measure of this ScalarInputV1.
        :type: str
        """

        self._unit_of_measure = unit_of_measure

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
        if not isinstance(other, ScalarInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
