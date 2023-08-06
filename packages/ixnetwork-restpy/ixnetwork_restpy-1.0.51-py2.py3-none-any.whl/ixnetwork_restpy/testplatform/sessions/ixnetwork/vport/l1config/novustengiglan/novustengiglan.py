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


class NovusTenGigLan(Base):
    """Novus 10GE LAN Port
    The NovusTenGigLan class encapsulates a required novusTenGigLan resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'novusTenGigLan'

    def __init__(self, parent):
        super(NovusTenGigLan, self).__init__(parent)

    @property
    def Fcoe(self):
        """An instance of the Fcoe class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.novustengiglan.fcoe.fcoe.Fcoe)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.novustengiglan.fcoe.fcoe import Fcoe
        return Fcoe(self)._select()

    @property
    def TxLane(self):
        """An instance of the TxLane class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.novustengiglan.txlane.txlane.TxLane)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.novustengiglan.txlane.txlane import TxLane
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
        """If enabled, allows autonegotiation between ports for speed.

        Returns:
            bool
        """
        return self._get_attribute('autoNegotiate')
    @AutoNegotiate.setter
    def AutoNegotiate(self, value):
        self._set_attribute('autoNegotiate', value)

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
        """If true, enables the port's MAC flow control and mechanisms to listen for a directed address pause message.

        Returns:
            bool
        """
        return self._get_attribute('enabledFlowControl')
    @EnabledFlowControl.setter
    def EnabledFlowControl(self, value):
        self._set_attribute('enabledFlowControl', value)

    @property
    def FlowControlDirectedAddress(self):
        """The 48-bit MAC address that the port listens on for a directed pause.

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
    def MasterSlaveMode(self):
        """

        Returns:
            str(master|slave)
        """
        return self._get_attribute('masterSlaveMode')
    @MasterSlaveMode.setter
    def MasterSlaveMode(self, value):
        self._set_attribute('masterSlaveMode', value)

    @property
    def Media(self):
        """Available only for cards that support this dual-PHY capability.

        Returns:
            str(copper|fiber|sgmii)
        """
        return self._get_attribute('media')
    @Media.setter
    def Media(self, value):
        self._set_attribute('media', value)

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
    def Speed(self):
        """NOT DEFINED

        Returns:
            str(speed1000|speed100fd|speed10g|speed2.5g|speed5g)
        """
        return self._get_attribute('speed')
    @Speed.setter
    def Speed(self, value):
        self._set_attribute('speed', value)

    @property
    def SpeedAuto(self):
        """

        Returns:
            list(str[speed1000|speed100fd|speed10g|speed2.5g|speed5g])
        """
        return self._get_attribute('speedAuto')
    @SpeedAuto.setter
    def SpeedAuto(self, value):
        self._set_attribute('speedAuto', value)

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

    def update(self, AutoInstrumentation=None, AutoNegotiate=None, EnablePPM=None, EnabledFlowControl=None, FlowControlDirectedAddress=None, Loopback=None, LoopbackMode=None, MasterSlaveMode=None, Media=None, Ppm=None, Speed=None, SpeedAuto=None, TxIgnoreRxLinkFaults=None):
        """Updates a child instance of novusTenGigLan on the server.

        Args:
            AutoInstrumentation (str(endOfFrame|floating)): The auto instrumentation mode.
            AutoNegotiate (bool): If enabled, allows autonegotiation between ports for speed.
            EnablePPM (bool): If true, enables the portsppm.
            EnabledFlowControl (bool): If true, enables the port's MAC flow control and mechanisms to listen for a directed address pause message.
            FlowControlDirectedAddress (str): The 48-bit MAC address that the port listens on for a directed pause.
            Loopback (bool): If enabled, the port is set to internally loopback from transmit to receive.
            LoopbackMode (str(internalLoopback|lineLoopback|none)): NOT DEFINED
            MasterSlaveMode (str(master|slave)): 
            Media (str(copper|fiber|sgmii)): Available only for cards that support this dual-PHY capability.
            Ppm (number): Indicates the value that needs to be adjusted for the line transmit frequency.
            Speed (str(speed1000|speed100fd|speed10g|speed2.5g|speed5g)): NOT DEFINED
            SpeedAuto (list(str[speed1000|speed100fd|speed10g|speed2.5g|speed5g])): 
            TxIgnoreRxLinkFaults (bool): If enabled, will allow transmission of packets even if the receive link is down.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())
