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


class DceNodeTopologyList(Base):
    """Fabric-Path Node Topology
    The DceNodeTopologyList class encapsulates a required dceNodeTopologyList resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'dceNodeTopologyList'

    def __init__(self, parent):
        super(DceNodeTopologyList, self).__init__(parent)

    @property
    def InterestedVlanList(self):
        """An instance of the InterestedVlanList class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interestedvlanlist.InterestedVlanList)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interestedvlanlist import InterestedVlanList
        return InterestedVlanList(self)._select()

    @property
    def Active(self):
        """Activate/Deactivate Configuration

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('active')

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
    def EnableFTAG(self):
        """Enable FTAG

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('enableFTAG')

    @property
    def InterestedVlanRangeCount(self):
        """Interested VLAN Range Count(multiplier)

        Returns:
            number
        """
        return self._get_attribute('interestedVlanRangeCount')
    @InterestedVlanRangeCount.setter
    def InterestedVlanRangeCount(self, value):
        self._set_attribute('interestedVlanRangeCount', value)

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
    def NoOfTreesToCompute(self):
        """No. of Trees to Compute

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('noOfTreesToCompute')

    @property
    def StartFTAGValue(self):
        """Start FTAG Value

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('startFTAGValue')

    @property
    def TopologyId(self):
        """Topology Id

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('topologyId')

    def update(self, InterestedVlanRangeCount=None, Name=None):
        """Updates a child instance of dceNodeTopologyList on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args:
            InterestedVlanRangeCount (number): Interested VLAN Range Count(multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def get_device_ids(self, PortNames=None, Active=None, EnableFTAG=None, NoOfTreesToCompute=None, StartFTAGValue=None, TopologyId=None):
        """Base class infrastructure that gets a list of dceNodeTopologyList device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args:
            PortNames (str): optional regex of port names
            Active (str): optional regex of active
            EnableFTAG (str): optional regex of enableFTAG
            NoOfTreesToCompute (str): optional regex of noOfTreesToCompute
            StartFTAGValue (str): optional regex of startFTAGValue
            TopologyId (str): optional regex of topologyId

        Returns:
            list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())
