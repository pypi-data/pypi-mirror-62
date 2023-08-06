# MIT LICENSE
#
# Copyright 1997 - 2019 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE. 
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpUmhImportRouteTargetList(Base):
    """Import RouteTarget
    The BgpUmhImportRouteTargetList class encapsulates a list of bgpUmhImportRouteTargetList resources that is managed by the system.
    A list of resources can be retrieved from the server using the BgpUmhImportRouteTargetList.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'bgpUmhImportRouteTargetList'

    def __init__(self, parent):
        super(BgpUmhImportRouteTargetList, self).__init__(parent)

    @property
    def Count(self):
        """Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.

        Returns:
            number
        """
        return self._get_attribute('count')

    @property
    def DescriptiveName(self):
        """Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context

        Returns:
            str
        """
        return self._get_attribute('descriptiveName')

    @property
    def Name(self):
        """Name of NGPF element, guaranteed to be unique in Scenario

        Returns:
            str
        """
        return self._get_attribute('name')
    @Name.setter
    def Name(self, value):
        self._set_attribute('name', value)

    @property
    def TargetAs4Number(self):
        """Import Route Target AS4 Number

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('targetAs4Number')

    @property
    def TargetAsNumber(self):
        """Import Route Target AS Number

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('targetAsNumber')

    @property
    def TargetAssignedNumber(self):
        """Import Route Target Assigned Number

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('targetAssignedNumber')

    @property
    def TargetIpAddress(self):
        """Import Route Target IP Address

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('targetIpAddress')

    @property
    def TargetType(self):
        """Import Route Target Type

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('targetType')

    def update(self, Name=None):
        """Updates a child instance of bgpUmhImportRouteTargetList on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args:
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def find(self, Count=None, DescriptiveName=None, Name=None):
        """Finds and retrieves bgpUmhImportRouteTargetList data from the server.

        All named parameters support regex and can be used to selectively retrieve bgpUmhImportRouteTargetList data from the server.
        By default the find method takes no parameters and will retrieve all bgpUmhImportRouteTargetList data from the server.

        Args:
            Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
            DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Returns:
            self: This instance with matching bgpUmhImportRouteTargetList data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of bgpUmhImportRouteTargetList data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the bgpUmhImportRouteTargetList data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def get_device_ids(self, PortNames=None, TargetAs4Number=None, TargetAsNumber=None, TargetAssignedNumber=None, TargetIpAddress=None, TargetType=None):
        """Base class infrastructure that gets a list of bgpUmhImportRouteTargetList device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args:
            PortNames (str): optional regex of port names
            TargetAs4Number (str): optional regex of targetAs4Number
            TargetAsNumber (str): optional regex of targetAsNumber
            TargetAssignedNumber (str): optional regex of targetAssignedNumber
            TargetIpAddress (str): optional regex of targetIpAddress
            TargetType (str): optional regex of targetType

        Returns:
            list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())
