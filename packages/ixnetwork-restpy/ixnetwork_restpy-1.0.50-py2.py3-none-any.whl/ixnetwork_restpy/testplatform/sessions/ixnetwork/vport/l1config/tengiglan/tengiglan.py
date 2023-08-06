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


class TenGigLan(Base):
    """Layer 1 (physical) parameters for a 10 Gigabit Ethernet LAN port.
    The TenGigLan class encapsulates a required tenGigLan resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'tenGigLan'

    def __init__(self, parent):
        super(TenGigLan, self).__init__(parent)

    @property
    def Fcoe(self):
        """An instance of the Fcoe class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.fcoe.fcoe.Fcoe)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.fcoe.fcoe import Fcoe
        return Fcoe(self)._select()

    @property
    def Oam(self):
        """An instance of the Oam class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.oam.oam.Oam)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.oam.oam import Oam
        return Oam(self)._select()

    @property
    def TxLane(self):
        """An instance of the TxLane class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.txlane.txlane.TxLane)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.txlane.txlane import TxLane
        return TxLane(self)._select()

    @property
    def AutoInstrumentation(self):
        """The auto instrumentation mode.

        Returns:
            str(endOfFrame|floating)
        """
        return self._get_attribute('autoInstrumentation')
    @AutoInstrumentation.setter
    def AutoInstrumentation(self, value):
        self._set_attribute('autoInstrumentation', value)

    @property
    def AutoNegotiate(self):
        """NOT DEFINED

        Returns:
            str(asymmetric|both|fullDuplex|none)
        """
        return self._get_attribute('autoNegotiate')
    @AutoNegotiate.setter
    def AutoNegotiate(self, value):
        self._set_attribute('autoNegotiate', value)

    @property
    def EnableLASIMonitoring(self):
        """If selected, enables LASI monitoring.

        Returns:
            bool
        """
        return self._get_attribute('enableLASIMonitoring')
    @EnableLASIMonitoring.setter
    def EnableLASIMonitoring(self, value):
        self._set_attribute('enableLASIMonitoring', value)

    @property
    def EnablePPM(self):
        """If true, enables the portsppm.

        Returns:
            bool
        """
        return self._get_attribute('enablePPM')
    @EnablePPM.setter
    def EnablePPM(self, value):
        self._set_attribute('enablePPM', value)

    @property
    def EnabledFlowControl(self):
        """Enables the port's MAC Flow control mechanisms to listen for a directed address pause message.

        Returns:
            bool
        """
        return self._get_attribute('enabledFlowControl')
    @EnabledFlowControl.setter
    def EnabledFlowControl(self, value):
        self._set_attribute('enabledFlowControl', value)

    @property
    def FlowControlDirectedAddress(self):
        """This is the 48-bit MAC address that the port will listen on for a directed pause message.

        Returns:
            str
        """
        return self._get_attribute('flowControlDirectedAddress')
    @FlowControlDirectedAddress.setter
    def FlowControlDirectedAddress(self, value):
        self._set_attribute('flowControlDirectedAddress', value)

    @property
    def Loopback(self):
        """If enabled, the port is set to internally loopback from transmit to receive.

        Returns:
            bool
        """
        return self._get_attribute('loopback')
    @Loopback.setter
    def Loopback(self, value):
        self._set_attribute('loopback', value)

    @property
    def LoopbackMode(self):
        """NOT DEFINED

        Returns:
            str(internalLoopback|lineLoopback|none)
        """
        return self._get_attribute('loopbackMode')
    @LoopbackMode.setter
    def LoopbackMode(self, value):
        self._set_attribute('loopbackMode', value)

    @property
    def Ppm(self):
        """Indicates the value that needs to be adjusted for the line transmit frequency.

        Returns:
            number
        """
        return self._get_attribute('ppm')
    @Ppm.setter
    def Ppm(self, value):
        self._set_attribute('ppm', value)

    @property
    def TransmitClocking(self):
        """The transmit clocking type for the 10G LAN port.

        Returns:
            str(external|internal|recovered)
        """
        return self._get_attribute('transmitClocking')
    @TransmitClocking.setter
    def TransmitClocking(self, value):
        self._set_attribute('transmitClocking', value)

    @property
    def TxIgnoreRxLinkFaults(self):
        """If enabled, will allow transmission of packets even if the receive link is down.

        Returns:
            bool
        """
        return self._get_attribute('txIgnoreRxLinkFaults')
    @TxIgnoreRxLinkFaults.setter
    def TxIgnoreRxLinkFaults(self, value):
        self._set_attribute('txIgnoreRxLinkFaults', value)

    def update(self, AutoInstrumentation=None, AutoNegotiate=None, EnableLASIMonitoring=None, EnablePPM=None, EnabledFlowControl=None, FlowControlDirectedAddress=None, Loopback=None, LoopbackMode=None, Ppm=None, TransmitClocking=None, TxIgnoreRxLinkFaults=None):
        """Updates a child instance of tenGigLan on the server.

        Args:
            AutoInstrumentation (str(endOfFrame|floating)): The auto instrumentation mode.
            AutoNegotiate (str(asymmetric|both|fullDuplex|none)): NOT DEFINED
            EnableLASIMonitoring (bool): If selected, enables LASI monitoring.
            EnablePPM (bool): If true, enables the portsppm.
            EnabledFlowControl (bool): Enables the port's MAC Flow control mechanisms to listen for a directed address pause message.
            FlowControlDirectedAddress (str): This is the 48-bit MAC address that the port will listen on for a directed pause message.
            Loopback (bool): If enabled, the port is set to internally loopback from transmit to receive.
            LoopbackMode (str(internalLoopback|lineLoopback|none)): NOT DEFINED
            Ppm (number): Indicates the value that needs to be adjusted for the line transmit frequency.
            TransmitClocking (str(external|internal|recovered)): The transmit clocking type for the 10G LAN port.
            TxIgnoreRxLinkFaults (bool): If enabled, will allow transmission of packets even if the receive link is down.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())
