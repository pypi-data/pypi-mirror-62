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


class ExportItemsV1(object):
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
        'autoupdate_time_range': 'bool',
        'capsule_time': 'bool',
        'export_capsules': 'bool',
        'export_name': 'str',
        'format': 'str',
        'grid_enabled': 'bool',
        'grid_size': 'str',
        'items': 'list[ExportItemV1]',
        'original_timestamps_enabled': 'bool',
        'scoped_to': 'str',
        'statistics_enabled': 'bool',
        'swap_in': 'str',
        'swap_out': 'str'
    }

    attribute_map = {
        'autoupdate_time_range': 'autoupdateTimeRange',
        'capsule_time': 'capsuleTime',
        'export_capsules': 'exportCapsules',
        'export_name': 'exportName',
        'format': 'format',
        'grid_enabled': 'gridEnabled',
        'grid_size': 'gridSize',
        'items': 'items',
        'original_timestamps_enabled': 'originalTimestampsEnabled',
        'scoped_to': 'scopedTo',
        'statistics_enabled': 'statisticsEnabled',
        'swap_in': 'swapIn',
        'swap_out': 'swapOut'
    }

    def __init__(self, autoupdate_time_range=False, capsule_time=False, export_capsules=False, export_name=None, format=None, grid_enabled=True, grid_size=None, items=None, original_timestamps_enabled=False, scoped_to=None, statistics_enabled=True, swap_in=None, swap_out=None):
        """
        ExportItemsV1 - a model defined in Swagger
        """

        self._autoupdate_time_range = None
        self._capsule_time = None
        self._export_capsules = None
        self._export_name = None
        self._format = None
        self._grid_enabled = None
        self._grid_size = None
        self._items = None
        self._original_timestamps_enabled = None
        self._scoped_to = None
        self._statistics_enabled = None
        self._swap_in = None
        self._swap_out = None

        if autoupdate_time_range is not None:
          self.autoupdate_time_range = autoupdate_time_range
        if capsule_time is not None:
          self.capsule_time = capsule_time
        if export_capsules is not None:
          self.export_capsules = export_capsules
        if export_name is not None:
          self.export_name = export_name
        if format is not None:
          self.format = format
        if grid_enabled is not None:
          self.grid_enabled = grid_enabled
        if grid_size is not None:
          self.grid_size = grid_size
        if items is not None:
          self.items = items
        if original_timestamps_enabled is not None:
          self.original_timestamps_enabled = original_timestamps_enabled
        if scoped_to is not None:
          self.scoped_to = scoped_to
        if statistics_enabled is not None:
          self.statistics_enabled = statistics_enabled
        if swap_in is not None:
          self.swap_in = swap_in
        if swap_out is not None:
          self.swap_out = swap_out

    @property
    def autoupdate_time_range(self):
        """
        Gets the autoupdate_time_range of this ExportItemsV1.
        Boolean indicating if the time range for export should be updated to 'now' when the export is started.

        :return: The autoupdate_time_range of this ExportItemsV1.
        :rtype: bool
        """
        return self._autoupdate_time_range

    @autoupdate_time_range.setter
    def autoupdate_time_range(self, autoupdate_time_range):
        """
        Sets the autoupdate_time_range of this ExportItemsV1.
        Boolean indicating if the time range for export should be updated to 'now' when the export is started.

        :param autoupdate_time_range: The autoupdate_time_range of this ExportItemsV1.
        :type: bool
        """

        self._autoupdate_time_range = autoupdate_time_range

    @property
    def capsule_time(self):
        """
        Gets the capsule_time of this ExportItemsV1.
        True if capsule time is displayed, false otherwise.

        :return: The capsule_time of this ExportItemsV1.
        :rtype: bool
        """
        return self._capsule_time

    @capsule_time.setter
    def capsule_time(self, capsule_time):
        """
        Sets the capsule_time of this ExportItemsV1.
        True if capsule time is displayed, false otherwise.

        :param capsule_time: The capsule_time of this ExportItemsV1.
        :type: bool
        """

        self._capsule_time = capsule_time

    @property
    def export_capsules(self):
        """
        Gets the export_capsules of this ExportItemsV1.
        True if the capsule table should be exported, false otherwise.

        :return: The export_capsules of this ExportItemsV1.
        :rtype: bool
        """
        return self._export_capsules

    @export_capsules.setter
    def export_capsules(self, export_capsules):
        """
        Sets the export_capsules of this ExportItemsV1.
        True if the capsule table should be exported, false otherwise.

        :param export_capsules: The export_capsules of this ExportItemsV1.
        :type: bool
        """

        self._export_capsules = export_capsules

    @property
    def export_name(self):
        """
        Gets the export_name of this ExportItemsV1.
        The desired name for the export. This name is used to create an OData endpoint for accessing the data being exported.

        :return: The export_name of this ExportItemsV1.
        :rtype: str
        """
        return self._export_name

    @export_name.setter
    def export_name(self, export_name):
        """
        Sets the export_name of this ExportItemsV1.
        The desired name for the export. This name is used to create an OData endpoint for accessing the data being exported.

        :param export_name: The export_name of this ExportItemsV1.
        :type: str
        """
        if export_name is None:
            raise ValueError("Invalid value for `export_name`, must not be `None`")

        self._export_name = export_name

    @property
    def format(self):
        """
        Gets the format of this ExportItemsV1.
        The desired export output format. Currently only 'xlsx' and 'odata' are supported.

        :return: The format of this ExportItemsV1.
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """
        Sets the format of this ExportItemsV1.
        The desired export output format. Currently only 'xlsx' and 'odata' are supported.

        :param format: The format of this ExportItemsV1.
        :type: str
        """
        if format is None:
            raise ValueError("Invalid value for `format`, must not be `None`")

        self._format = format

    @property
    def grid_enabled(self):
        """
        Gets the grid_enabled of this ExportItemsV1.
        Boolean indicating whether the data grid should be included.

        :return: The grid_enabled of this ExportItemsV1.
        :rtype: bool
        """
        return self._grid_enabled

    @grid_enabled.setter
    def grid_enabled(self, grid_enabled):
        """
        Sets the grid_enabled of this ExportItemsV1.
        Boolean indicating whether the data grid should be included.

        :param grid_enabled: The grid_enabled of this ExportItemsV1.
        :type: bool
        """

        self._grid_enabled = grid_enabled

    @property
    def grid_size(self):
        """
        Gets the grid_size of this ExportItemsV1.
        The desired sample period for the export. An automatic grid size is used when gridSize is set to 'false'.

        :return: The grid_size of this ExportItemsV1.
        :rtype: str
        """
        return self._grid_size

    @grid_size.setter
    def grid_size(self, grid_size):
        """
        Sets the grid_size of this ExportItemsV1.
        The desired sample period for the export. An automatic grid size is used when gridSize is set to 'false'.

        :param grid_size: The grid_size of this ExportItemsV1.
        :type: str
        """

        self._grid_size = grid_size

    @property
    def items(self):
        """
        Gets the items of this ExportItemsV1.
        A list of Series and Capsules to be exported

        :return: The items of this ExportItemsV1.
        :rtype: list[ExportItemV1]
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this ExportItemsV1.
        A list of Series and Capsules to be exported

        :param items: The items of this ExportItemsV1.
        :type: list[ExportItemV1]
        """
        if items is None:
            raise ValueError("Invalid value for `items`, must not be `None`")

        self._items = items

    @property
    def original_timestamps_enabled(self):
        """
        Gets the original_timestamps_enabled of this ExportItemsV1.
        True if the original sample period should be used. A manual or automatic grid size may be used when false.

        :return: The original_timestamps_enabled of this ExportItemsV1.
        :rtype: bool
        """
        return self._original_timestamps_enabled

    @original_timestamps_enabled.setter
    def original_timestamps_enabled(self, original_timestamps_enabled):
        """
        Sets the original_timestamps_enabled of this ExportItemsV1.
        True if the original sample period should be used. A manual or automatic grid size may be used when false.

        :param original_timestamps_enabled: The original_timestamps_enabled of this ExportItemsV1.
        :type: bool
        """

        self._original_timestamps_enabled = original_timestamps_enabled

    @property
    def scoped_to(self):
        """
        Gets the scoped_to of this ExportItemsV1.
        The ID of the workbook to which this item will be scoped. Only valid for OData exports. If not provided, the export will have global scope.

        :return: The scoped_to of this ExportItemsV1.
        :rtype: str
        """
        return self._scoped_to

    @scoped_to.setter
    def scoped_to(self, scoped_to):
        """
        Sets the scoped_to of this ExportItemsV1.
        The ID of the workbook to which this item will be scoped. Only valid for OData exports. If not provided, the export will have global scope.

        :param scoped_to: The scoped_to of this ExportItemsV1.
        :type: str
        """

        self._scoped_to = scoped_to

    @property
    def statistics_enabled(self):
        """
        Gets the statistics_enabled of this ExportItemsV1.
        Boolean indicating whether the summary statistics should be included. This flag only applies to Excel exports.

        :return: The statistics_enabled of this ExportItemsV1.
        :rtype: bool
        """
        return self._statistics_enabled

    @statistics_enabled.setter
    def statistics_enabled(self, statistics_enabled):
        """
        Sets the statistics_enabled of this ExportItemsV1.
        Boolean indicating whether the summary statistics should be included. This flag only applies to Excel exports.

        :param statistics_enabled: The statistics_enabled of this ExportItemsV1.
        :type: bool
        """

        self._statistics_enabled = statistics_enabled

    @property
    def swap_in(self):
        """
        Gets the swap_in of this ExportItemsV1.
        The ID of an asset to swap in. Any parameters in the formula that are named the same in both the swapIn and swapOut assets will be swapped.

        :return: The swap_in of this ExportItemsV1.
        :rtype: str
        """
        return self._swap_in

    @swap_in.setter
    def swap_in(self, swap_in):
        """
        Sets the swap_in of this ExportItemsV1.
        The ID of an asset to swap in. Any parameters in the formula that are named the same in both the swapIn and swapOut assets will be swapped.

        :param swap_in: The swap_in of this ExportItemsV1.
        :type: str
        """

        self._swap_in = swap_in

    @property
    def swap_out(self):
        """
        Gets the swap_out of this ExportItemsV1.
        The ID of an asset to swap out. Any parameters in the formula that are named the same in both the swapIn and swapOut assets will be swapped.

        :return: The swap_out of this ExportItemsV1.
        :rtype: str
        """
        return self._swap_out

    @swap_out.setter
    def swap_out(self, swap_out):
        """
        Sets the swap_out of this ExportItemsV1.
        The ID of an asset to swap out. Any parameters in the formula that are named the same in both the swapIn and swapOut assets will be swapped.

        :param swap_out: The swap_out of this ExportItemsV1.
        :type: str
        """

        self._swap_out = swap_out

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
        if not isinstance(other, ExportItemsV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
