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


class IsisPseudoSRv6AdjSIDList(Base):
    """ISIS SRv6 Adj SID
    The IsisPseudoSRv6AdjSIDList class encapsulates a required isisPseudoSRv6AdjSIDList resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'isisPseudoSRv6AdjSIDList'

    def __init__(self, parent):
        super(IsisPseudoSRv6AdjSIDList, self).__init__(parent)

    @property
    def Active(self):
        """Activate/Deactivate Configuration

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('active')

    @property
    def AdvertiseCustomSubTLV(self):
        """Advertise Custom Sub-TLV

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('advertiseCustomSubTLV')

    @property
    def Algorithm(self):
        """Algorithm

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('algorithm')

    @property
    def BFlag(self):
        """B-Flag

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('bFlag')

    @property
    def Count(self):
        """Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.

        Returns:
            number
        """
        return self._get_attribute('count')

    @property
    def CustomSubTlv(self):
        """Custom Sub-TLV

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('customSubTlv')

    @property
    def DescriptiveName(self):
        """Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context

        Returns:
            str
        """
        return self._get_attribute('descriptiveName')

    @property
    def EndPointFunction(self):
        """End-Point Function

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('endPointFunction')

    @property
    def Ipv6AdjSid(self):
        """IPv6 Adj SID

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('ipv6AdjSid')

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
    def PFlag(self):
        """P-Flag

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('pFlag')

    @property
    def Reserved(self):
        """Reserved

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('reserved')

    @property
    def SFlag(self):
        """S-Flag

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('sFlag')

    @property
    def Weight(self):
        """Weight

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('weight')

    def update(self, Name=None):
        """Updates a child instance of isisPseudoSRv6AdjSIDList on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args:
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def get_device_ids(self, PortNames=None, Active=None, AdvertiseCustomSubTLV=None, Algorithm=None, BFlag=None, CustomSubTlv=None, EndPointFunction=None, Ipv6AdjSid=None, PFlag=None, Reserved=None, SFlag=None, Weight=None):
        """Base class infrastructure that gets a list of isisPseudoSRv6AdjSIDList device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args:
            PortNames (str): optional regex of port names
            Active (str): optional regex of active
            AdvertiseCustomSubTLV (str): optional regex of advertiseCustomSubTLV
            Algorithm (str): optional regex of algorithm
            BFlag (str): optional regex of bFlag
            CustomSubTlv (str): optional regex of customSubTlv
            EndPointFunction (str): optional regex of endPointFunction
            Ipv6AdjSid (str): optional regex of ipv6AdjSid
            PFlag (str): optional regex of pFlag
            Reserved (str): optional regex of reserved
            SFlag (str): optional regex of sFlag
            Weight (str): optional regex of weight

        Returns:
            list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())

    def Start(self):
        """Executes the start operation on the server.

        Start CPF control plane (equals to promote to negotiated state).

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        return self._execute('start', payload=payload, response_object=None)

    def Stop(self):
        """Executes the stop operation on the server.

        Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        return self._execute('stop', payload=payload, response_object=None)
