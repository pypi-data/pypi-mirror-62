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


class ReportInputItemV1(object):
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
        'link_url': 'str',
        'screenshot_url': 'str',
        'worksheet_id': 'str'
    }

    attribute_map = {
        'link_url': 'linkURL',
        'screenshot_url': 'screenshotURL',
        'worksheet_id': 'worksheetId'
    }

    def __init__(self, link_url=None, screenshot_url=None, worksheet_id=None):
        """
        ReportInputItemV1 - a model defined in Swagger
        """

        self._link_url = None
        self._screenshot_url = None
        self._worksheet_id = None

        if link_url is not None:
          self.link_url = link_url
        if screenshot_url is not None:
          self.screenshot_url = screenshot_url
        if worksheet_id is not None:
          self.worksheet_id = worksheet_id

    @property
    def link_url(self):
        """
        Gets the link_url of this ReportInputItemV1.
        Link URL to use for this Worksheet. If empty, no link will be included

        :return: The link_url of this ReportInputItemV1.
        :rtype: str
        """
        return self._link_url

    @link_url.setter
    def link_url(self, link_url):
        """
        Sets the link_url of this ReportInputItemV1.
        Link URL to use for this Worksheet. If empty, no link will be included

        :param link_url: The link_url of this ReportInputItemV1.
        :type: str
        """

        self._link_url = link_url

    @property
    def screenshot_url(self):
        """
        Gets the screenshot_url of this ReportInputItemV1.
        URL from which to generate a screenshot for this Worksheet. If empty, no screenshot will be included

        :return: The screenshot_url of this ReportInputItemV1.
        :rtype: str
        """
        return self._screenshot_url

    @screenshot_url.setter
    def screenshot_url(self, screenshot_url):
        """
        Sets the screenshot_url of this ReportInputItemV1.
        URL from which to generate a screenshot for this Worksheet. If empty, no screenshot will be included

        :param screenshot_url: The screenshot_url of this ReportInputItemV1.
        :type: str
        """

        self._screenshot_url = screenshot_url

    @property
    def worksheet_id(self):
        """
        Gets the worksheet_id of this ReportInputItemV1.
        Worksheet ID to include in the report

        :return: The worksheet_id of this ReportInputItemV1.
        :rtype: str
        """
        return self._worksheet_id

    @worksheet_id.setter
    def worksheet_id(self, worksheet_id):
        """
        Sets the worksheet_id of this ReportInputItemV1.
        Worksheet ID to include in the report

        :param worksheet_id: The worksheet_id of this ReportInputItemV1.
        :type: str
        """
        if worksheet_id is None:
            raise ValueError("Invalid value for `worksheet_id`, must not be `None`")

        self._worksheet_id = worksheet_id

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
        if not isinstance(other, ReportInputItemV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
