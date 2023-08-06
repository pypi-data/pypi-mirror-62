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


class SupportedActions(Base):
    """This object allows to define the Bitmap of supported actions.
    The SupportedActions class encapsulates a required supportedActions resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'supportedActions'

    def __init__(self, parent):
        super(SupportedActions, self).__init__(parent)

    @property
    def Enqueue(self):
        """Indicates that the supported action of the switch includes Output to queue.

        Returns:
            bool
        """
        return self._get_attribute('enqueue')
    @Enqueue.setter
    def Enqueue(self, value):
        self._set_attribute('enqueue', value)

    @property
    def EthernetDestination(self):
        """Indicates that the supported action of the switch includes setting Ethernet destination address.

        Returns:
            bool
        """
        return self._get_attribute('ethernetDestination')
    @EthernetDestination.setter
    def EthernetDestination(self, value):
        self._set_attribute('ethernetDestination', value)

    @property
    def EthernetSource(self):
        """Indicates that the supported action of the switch includes setting Ethernet source address.

        Returns:
            bool
        """
        return self._get_attribute('ethernetSource')
    @EthernetSource.setter
    def EthernetSource(self, value):
        self._set_attribute('ethernetSource', value)

    @property
    def IpDscp(self):
        """Indicates that the supported action of the switch includes setting IP ToS, DSCP field, 6 bits.

        Returns:
            bool
        """
        return self._get_attribute('ipDscp')
    @IpDscp.setter
    def IpDscp(self, value):
        self._set_attribute('ipDscp', value)

    @property
    def Ipv4Destination(self):
        """Indicates that the supported action of the switch includes setting IP destination address.

        Returns:
            bool
        """
        return self._get_attribute('ipv4Destination')
    @Ipv4Destination.setter
    def Ipv4Destination(self, value):
        self._set_attribute('ipv4Destination', value)

    @property
    def Ipv4Source(self):
        """Indicates that the supported action of the switch includes setting IP source address.

        Returns:
            bool
        """
        return self._get_attribute('ipv4Source')
    @Ipv4Source.setter
    def Ipv4Source(self, value):
        self._set_attribute('ipv4Source', value)

    @property
    def Output(self):
        """Indicates that the supported action of the switch includes Output to switch port.

        Returns:
            bool
        """
        return self._get_attribute('output')
    @Output.setter
    def Output(self, value):
        self._set_attribute('output', value)

    @property
    def StripVlanHeader(self):
        """Indicates that the supported action of the switch includes stripping the 802.1q header.

        Returns:
            bool
        """
        return self._get_attribute('stripVlanHeader')
    @StripVlanHeader.setter
    def StripVlanHeader(self, value):
        self._set_attribute('stripVlanHeader', value)

    @property
    def TransportDestination(self):
        """Indicates that the supported action of the switch includes setting TCP/UDP destination port.

        Returns:
            bool
        """
        return self._get_attribute('transportDestination')
    @TransportDestination.setter
    def TransportDestination(self, value):
        self._set_attribute('transportDestination', value)

    @property
    def TransportSource(self):
        """Indicates that the supported action of the switch includes setting TCP/UDP source port.

        Returns:
            bool
        """
        return self._get_attribute('transportSource')
    @TransportSource.setter
    def TransportSource(self, value):
        self._set_attribute('transportSource', value)

    @property
    def VlanId(self):
        """Indicates that the supported action of the switch includes setting the 802.1q VLAN id.

        Returns:
            bool
        """
        return self._get_attribute('vlanId')
    @VlanId.setter
    def VlanId(self, value):
        self._set_attribute('vlanId', value)

    @property
    def VlanPriority(self):
        """Indicates that the supported action of the switch includes setting the 802.1q priority.

        Returns:
            bool
        """
        return self._get_attribute('vlanPriority')
    @VlanPriority.setter
    def VlanPriority(self, value):
        self._set_attribute('vlanPriority', value)

    def update(self, Enqueue=None, EthernetDestination=None, EthernetSource=None, IpDscp=None, Ipv4Destination=None, Ipv4Source=None, Output=None, StripVlanHeader=None, TransportDestination=None, TransportSource=None, VlanId=None, VlanPriority=None):
        """Updates a child instance of supportedActions on the server.

        Args:
            Enqueue (bool): Indicates that the supported action of the switch includes Output to queue.
            EthernetDestination (bool): Indicates that the supported action of the switch includes setting Ethernet destination address.
            EthernetSource (bool): Indicates that the supported action of the switch includes setting Ethernet source address.
            IpDscp (bool): Indicates that the supported action of the switch includes setting IP ToS, DSCP field, 6 bits.
            Ipv4Destination (bool): Indicates that the supported action of the switch includes setting IP destination address.
            Ipv4Source (bool): Indicates that the supported action of the switch includes setting IP source address.
            Output (bool): Indicates that the supported action of the switch includes Output to switch port.
            StripVlanHeader (bool): Indicates that the supported action of the switch includes stripping the 802.1q header.
            TransportDestination (bool): Indicates that the supported action of the switch includes setting TCP/UDP destination port.
            TransportSource (bool): Indicates that the supported action of the switch includes setting TCP/UDP source port.
            VlanId (bool): Indicates that the supported action of the switch includes setting the 802.1q VLAN id.
            VlanPriority (bool): Indicates that the supported action of the switch includes setting the 802.1q priority.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())
