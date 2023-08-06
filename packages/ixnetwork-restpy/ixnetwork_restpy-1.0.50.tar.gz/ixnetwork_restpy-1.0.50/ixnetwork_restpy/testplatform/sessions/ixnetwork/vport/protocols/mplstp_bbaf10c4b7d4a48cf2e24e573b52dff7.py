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


class MplsTp(Base):
    """This object contains the MPLSTP protocol configuration.
    The MplsTp class encapsulates a required mplsTp resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'mplsTp'

    def __init__(self, parent):
        super(MplsTp, self).__init__(parent)

    @property
    def Router(self):
        """An instance of the Router class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.router_8bb274b34003209d4965465d50800ded.Router)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.router_8bb274b34003209d4965465d50800ded import Router
        return Router(self)

    @property
    def ApsChannelType(self):
        """DEPRECATED This signifies the Automatic Protection Switching Channel Type in hexadecimal format.

        Returns:
            str
        """
        return self._get_attribute('apsChannelType')
    @ApsChannelType.setter
    def ApsChannelType(self, value):
        self._set_attribute('apsChannelType', value)

    @property
    def BfdCcChannelType(self):
        """DEPRECATED This signifies the BFD Continuity Check Channel Type in hexadecimal format.

        Returns:
            str
        """
        return self._get_attribute('bfdCcChannelType')
    @BfdCcChannelType.setter
    def BfdCcChannelType(self, value):
        self._set_attribute('bfdCcChannelType', value)

    @property
    def DelayManagementChannelType(self):
        """DEPRECATED This signifies the Delay Measurement Channel Type in hexadecimal format.

        Returns:
            str
        """
        return self._get_attribute('delayManagementChannelType')
    @DelayManagementChannelType.setter
    def DelayManagementChannelType(self, value):
        self._set_attribute('delayManagementChannelType', value)

    @property
    def EnableHighPerformanceMode(self):
        """This signifies select the checkbox to enable high performance mode.

        Returns:
            bool
        """
        return self._get_attribute('enableHighPerformanceMode')
    @EnableHighPerformanceMode.setter
    def EnableHighPerformanceMode(self, value):
        self._set_attribute('enableHighPerformanceMode', value)

    @property
    def Enabled(self):
        """This signifies that the mplsTp protocol is enabled.

        Returns:
            bool
        """
        return self._get_attribute('enabled')
    @Enabled.setter
    def Enabled(self, value):
        self._set_attribute('enabled', value)

    @property
    def FaultManagementChannelType(self):
        """DEPRECATED This signifies the Fault Management Channel Type in hexadecimal format.

        Returns:
            str
        """
        return self._get_attribute('faultManagementChannelType')
    @FaultManagementChannelType.setter
    def FaultManagementChannelType(self, value):
        self._set_attribute('faultManagementChannelType', value)

    @property
    def LossMeasurementChannelType(self):
        """DEPRECATED This signifies the Loss Measurement Channel Type in hexadecimal format.

        Returns:
            str
        """
        return self._get_attribute('lossMeasurementChannelType')
    @LossMeasurementChannelType.setter
    def LossMeasurementChannelType(self, value):
        self._set_attribute('lossMeasurementChannelType', value)

    @property
    def OnDemandCvChannelType(self):
        """DEPRECATED This signifies the On Demand Connectivity Verification Channel Type in hexadecimal format.

        Returns:
            str
        """
        return self._get_attribute('onDemandCvChannelType')
    @OnDemandCvChannelType.setter
    def OnDemandCvChannelType(self, value):
        self._set_attribute('onDemandCvChannelType', value)

    @property
    def PwStatusChannelType(self):
        """DEPRECATED This signifies the Pseudowire Status Channel Type.

        Returns:
            str
        """
        return self._get_attribute('pwStatusChannelType')
    @PwStatusChannelType.setter
    def PwStatusChannelType(self, value):
        self._set_attribute('pwStatusChannelType', value)

    @property
    def RunningState(self):
        """This signifies the running state of the protocol. Possible values include Started, Starting, Unknown, Stopping and Stopped.

        Returns:
            str(unknown|stopped|stopping|starting|started)
        """
        return self._get_attribute('runningState')

    @property
    def Y1731ChannelType(self):
        """DEPRECATED This signifies the Y.1731 Channel Type in hexadecimal format.

        Returns:
            str
        """
        return self._get_attribute('y1731ChannelType')
    @Y1731ChannelType.setter
    def Y1731ChannelType(self, value):
        self._set_attribute('y1731ChannelType', value)

    def update(self, ApsChannelType=None, BfdCcChannelType=None, DelayManagementChannelType=None, EnableHighPerformanceMode=None, Enabled=None, FaultManagementChannelType=None, LossMeasurementChannelType=None, OnDemandCvChannelType=None, PwStatusChannelType=None, Y1731ChannelType=None):
        """Updates a child instance of mplsTp on the server.

        Args:
            ApsChannelType (str): This signifies the Automatic Protection Switching Channel Type in hexadecimal format.
            BfdCcChannelType (str): This signifies the BFD Continuity Check Channel Type in hexadecimal format.
            DelayManagementChannelType (str): This signifies the Delay Measurement Channel Type in hexadecimal format.
            EnableHighPerformanceMode (bool): This signifies select the checkbox to enable high performance mode.
            Enabled (bool): This signifies that the mplsTp protocol is enabled.
            FaultManagementChannelType (str): This signifies the Fault Management Channel Type in hexadecimal format.
            LossMeasurementChannelType (str): This signifies the Loss Measurement Channel Type in hexadecimal format.
            OnDemandCvChannelType (str): This signifies the On Demand Connectivity Verification Channel Type in hexadecimal format.
            PwStatusChannelType (str): This signifies the Pseudowire Status Channel Type.
            Y1731ChannelType (str): This signifies the Y.1731 Channel Type in hexadecimal format.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def Start(self):
        """Executes the start operation on the server.

        This signifies the starting of the MPLSTP protocol on a port or group of ports.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('start', payload=payload, response_object=None)

    def Stop(self):
        """Executes the stop operation on the server.

        This signifies the stopping of the MPLSTP protocol on a port or group of ports.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('stop', payload=payload, response_object=None)
