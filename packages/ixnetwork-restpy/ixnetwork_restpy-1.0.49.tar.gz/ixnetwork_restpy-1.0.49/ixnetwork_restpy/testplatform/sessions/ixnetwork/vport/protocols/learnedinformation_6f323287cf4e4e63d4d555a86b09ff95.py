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


class LearnedInformation(Base):
    """This object displays the information learned from each router.
    The LearnedInformation class encapsulates a required learnedInformation resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'learnedInformation'

    def __init__(self, parent):
        super(LearnedInformation, self).__init__(parent)

    @property
    def DmLearnedInfo(self):
        """An instance of the DmLearnedInfo class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.dmlearnedinfo_6335a4e11d3f828950198603b15528a6.DmLearnedInfo)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.dmlearnedinfo_6335a4e11d3f828950198603b15528a6 import DmLearnedInfo
        return DmLearnedInfo(self)

    @property
    def GeneralLearnedInfo(self):
        """An instance of the GeneralLearnedInfo class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.generallearnedinfo_a31e7a6a5a84a136f2fefec0d550e1ac.GeneralLearnedInfo)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.generallearnedinfo_a31e7a6a5a84a136f2fefec0d550e1ac import GeneralLearnedInfo
        return GeneralLearnedInfo(self)

    @property
    def LmLearnedInfo(self):
        """An instance of the LmLearnedInfo class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lmlearnedinfo_41dbcd2574057fe2a464f8f4bcff1e7e.LmLearnedInfo)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lmlearnedinfo_41dbcd2574057fe2a464f8f4bcff1e7e import LmLearnedInfo
        return LmLearnedInfo(self)

    @property
    def PingLearnedInfo(self):
        """An instance of the PingLearnedInfo class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pinglearnedinfo_7aa4302931c9457d45f2ff71274fbf48.PingLearnedInfo)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pinglearnedinfo_7aa4302931c9457d45f2ff71274fbf48 import PingLearnedInfo
        return PingLearnedInfo(self)

    @property
    def TraceRouteLearnedInfo(self):
        """An instance of the TraceRouteLearnedInfo class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.traceroutelearnedinfo_711c0b10747bbe05f7fcb418fed4e919.TraceRouteLearnedInfo)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.traceroutelearnedinfo_711c0b10747bbe05f7fcb418fed4e919 import TraceRouteLearnedInfo
        return TraceRouteLearnedInfo(self)

    @property
    def AlarmTrigger(self):
        """This signifies the alarm trigger. Possible values include Clear and Start.

        Returns:
            str(clear|start)
        """
        return self._get_attribute('alarmTrigger')
    @AlarmTrigger.setter
    def AlarmTrigger(self, value):
        self._set_attribute('alarmTrigger', value)

    @property
    def AlarmType(self):
        """This signifies the alarm type. Possible values include IETF and Y.1731.

        Returns:
            str(ietf|y1731)
        """
        return self._get_attribute('alarmType')
    @AlarmType.setter
    def AlarmType(self, value):
        self._set_attribute('alarmType', value)

    @property
    def ApsTriggerType(self):
        """This signifies the Trigger type. Possible values include Clear, Exercise, Forced Switch, Freeze, Lockout, Manual Switch To Protect and Manual Switch To Working.

        Returns:
            str(clear|forcedSwitch|manualSwitchToProtect|manualSwitchToWorking|lockout|exercise|freeze)
        """
        return self._get_attribute('apsTriggerType')
    @ApsTriggerType.setter
    def ApsTriggerType(self, value):
        self._set_attribute('apsTriggerType', value)

    @property
    def CccvPauseTriggerOption(self):
        """This signifies the cccv pause trigger option. Possible values include TX, RX and TXRX.

        Returns:
            str(tx|rx|txRx)
        """
        return self._get_attribute('cccvPauseTriggerOption')
    @CccvPauseTriggerOption.setter
    def CccvPauseTriggerOption(self, value):
        self._set_attribute('cccvPauseTriggerOption', value)

    @property
    def CccvResumeTriggerOption(self):
        """This signifies the cccv resume trigger option. Possible values include Tx, Rx and TxRx.

        Returns:
            str(tx|rx|txRx)
        """
        return self._get_attribute('cccvResumeTriggerOption')
    @CccvResumeTriggerOption.setter
    def CccvResumeTriggerOption(self, value):
        self._set_attribute('cccvResumeTriggerOption', value)

    @property
    def ChangeSessionParameters(self):
        """This specifies the minimum receive interval of cc messages in millisecond, at the source side that the user intends to set on the fly.

        Returns:
            bool
        """
        return self._get_attribute('changeSessionParameters')
    @ChangeSessionParameters.setter
    def ChangeSessionParameters(self, value):
        self._set_attribute('changeSessionParameters', value)

    @property
    def ClearMisconnectivityDefect(self):
        """If set true all the misconnectivity defects that have been triggered earlier with any type gets cleared.

        Returns:
            bool
        """
        return self._get_attribute('clearMisconnectivityDefect')
    @ClearMisconnectivityDefect.setter
    def ClearMisconnectivityDefect(self, value):
        self._set_attribute('clearMisconnectivityDefect', value)

    @property
    def CounterType(self):
        """This signifies the LM Counter Type. Possible values include 32 Bit (default) and 64 Bit.

        Returns:
            str(32Bit|64Bit)
        """
        return self._get_attribute('counterType')
    @CounterType.setter
    def CounterType(self, value):
        self._set_attribute('counterType', value)

    @property
    def DmInterval(self):
        """This signifies the DM interval in milliseconds.

        Returns:
            number
        """
        return self._get_attribute('dmInterval')
    @DmInterval.setter
    def DmInterval(self, value):
        self._set_attribute('dmInterval', value)

    @property
    def DmIterations(self):
        """This signifies the total number of DM queries to be sent.

        Returns:
            number
        """
        return self._get_attribute('dmIterations')
    @DmIterations.setter
    def DmIterations(self, value):
        self._set_attribute('dmIterations', value)

    @property
    def DmMode(self):
        """This signifies the DM mode. The possible values include Response Expected and No Response Expected.

        Returns:
            str(noResponseExpected|responseExpected)
        """
        return self._get_attribute('dmMode')
    @DmMode.setter
    def DmMode(self, value):
        self._set_attribute('dmMode', value)

    @property
    def DmPadLen(self):
        """This signifies the DM pad length.

        Returns:
            number
        """
        return self._get_attribute('dmPadLen')
    @DmPadLen.setter
    def DmPadLen(self, value):
        self._set_attribute('dmPadLen', value)

    @property
    def DmRequestPaddedReply(self):
        """This signifies the DM request as a padded reply.

        Returns:
            bool
        """
        return self._get_attribute('dmRequestPaddedReply')
    @DmRequestPaddedReply.setter
    def DmRequestPaddedReply(self, value):
        self._set_attribute('dmRequestPaddedReply', value)

    @property
    def DmTimeFormat(self):
        """This signifies the DM time format. The possible values include IEEE and NTP.

        Returns:
            str(ieee|ntp)
        """
        return self._get_attribute('dmTimeFormat')
    @DmTimeFormat.setter
    def DmTimeFormat(self, value):
        self._set_attribute('dmTimeFormat', value)

    @property
    def DmTrafficClass(self):
        """This signifies the DM traffic class value.

        Returns:
            number
        """
        return self._get_attribute('dmTrafficClass')
    @DmTrafficClass.setter
    def DmTrafficClass(self, value):
        self._set_attribute('dmTrafficClass', value)

    @property
    def DmType(self):
        """This signifies the DM Type. Possible values include IETF and Y.1731.

        Returns:
            str(ietf|y1731)
        """
        return self._get_attribute('dmType')
    @DmType.setter
    def DmType(self, value):
        self._set_attribute('dmType', value)

    @property
    def EnableAlarm(self):
        """This signifies the enablement of the Alarm and the fields under it.

        Returns:
            bool
        """
        return self._get_attribute('enableAlarm')
    @EnableAlarm.setter
    def EnableAlarm(self, value):
        self._set_attribute('enableAlarm', value)

    @property
    def EnableAlarmAis(self):
        """DEPRECATED This signifies the enablement of the Alarm AIS.

        Returns:
            bool
        """
        return self._get_attribute('enableAlarmAis')
    @EnableAlarmAis.setter
    def EnableAlarmAis(self, value):
        self._set_attribute('enableAlarmAis', value)

    @property
    def EnableAlarmFastClear(self):
        """Clears the Alarm State in 10 seconds

        Returns:
            bool
        """
        return self._get_attribute('enableAlarmFastClear')
    @EnableAlarmFastClear.setter
    def EnableAlarmFastClear(self, value):
        self._set_attribute('enableAlarmFastClear', value)

    @property
    def EnableAlarmLck(self):
        """This signifies the enablement of the Alarm lck.

        Returns:
            bool
        """
        return self._get_attribute('enableAlarmLck')
    @EnableAlarmLck.setter
    def EnableAlarmLck(self, value):
        self._set_attribute('enableAlarmLck', value)

    @property
    def EnableAlarmSetLdi(self):
        """This signifies the enablement of the Alarm Set LDI.

        Returns:
            bool
        """
        return self._get_attribute('enableAlarmSetLdi')
    @EnableAlarmSetLdi.setter
    def EnableAlarmSetLdi(self, value):
        self._set_attribute('enableAlarmSetLdi', value)

    @property
    def EnableApsTrigger(self):
        """This signifies the enablement of APS trigger.

        Returns:
            bool
        """
        return self._get_attribute('enableApsTrigger')
    @EnableApsTrigger.setter
    def EnableApsTrigger(self, value):
        self._set_attribute('enableApsTrigger', value)

    @property
    def EnableCccvPause(self):
        """This signifies the enabling of CCCV Pause.

        Returns:
            bool
        """
        return self._get_attribute('enableCccvPause')
    @EnableCccvPause.setter
    def EnableCccvPause(self, value):
        self._set_attribute('enableCccvPause', value)

    @property
    def EnableCccvResume(self):
        """This signifies the enablement of CCCV Resume.

        Returns:
            bool
        """
        return self._get_attribute('enableCccvResume')
    @EnableCccvResume.setter
    def EnableCccvResume(self, value):
        self._set_attribute('enableCccvResume', value)

    @property
    def EnableDmTrigger(self):
        """This signifies the enablement of the DM trigger.

        Returns:
            bool
        """
        return self._get_attribute('enableDmTrigger')
    @EnableDmTrigger.setter
    def EnableDmTrigger(self, value):
        self._set_attribute('enableDmTrigger', value)

    @property
    def EnableLmTrigger(self):
        """This signifies the enablement of the LM trigger.

        Returns:
            bool
        """
        return self._get_attribute('enableLmTrigger')
    @EnableLmTrigger.setter
    def EnableLmTrigger(self, value):
        self._set_attribute('enableLmTrigger', value)

    @property
    def EnableLspPing(self):
        """This signifies the enablement of the LSP Ping.

        Returns:
            bool
        """
        return self._get_attribute('enableLspPing')
    @EnableLspPing.setter
    def EnableLspPing(self, value):
        self._set_attribute('enableLspPing', value)

    @property
    def EnableLspPingFecStackValidation(self):
        """This signifies the enablement of the FEC Stack Validation.

        Returns:
            bool
        """
        return self._get_attribute('enableLspPingFecStackValidation')
    @EnableLspPingFecStackValidation.setter
    def EnableLspPingFecStackValidation(self, value):
        self._set_attribute('enableLspPingFecStackValidation', value)

    @property
    def EnableLspPingValidateReversePath(self):
        """If true validate reverse path bit is set in lsp ping message.

        Returns:
            bool
        """
        return self._get_attribute('enableLspPingValidateReversePath')
    @EnableLspPingValidateReversePath.setter
    def EnableLspPingValidateReversePath(self, value):
        self._set_attribute('enableLspPingValidateReversePath', value)

    @property
    def EnableLspTraceRoute(self):
        """This signifies the enablement of the lsp traceroute.

        Returns:
            bool
        """
        return self._get_attribute('enableLspTraceRoute')
    @EnableLspTraceRoute.setter
    def EnableLspTraceRoute(self, value):
        self._set_attribute('enableLspTraceRoute', value)

    @property
    def EnableLspTraceRouteFecStackValidation(self):
        """This signifies the enablement of the FEC Stack Validation.

        Returns:
            bool
        """
        return self._get_attribute('enableLspTraceRouteFecStackValidation')
    @EnableLspTraceRouteFecStackValidation.setter
    def EnableLspTraceRouteFecStackValidation(self, value):
        self._set_attribute('enableLspTraceRouteFecStackValidation', value)

    @property
    def EnablePwStatusClear(self):
        """This signifies the enablement of the PW Status Clear and the fields under it.

        Returns:
            bool
        """
        return self._get_attribute('enablePwStatusClear')
    @EnablePwStatusClear.setter
    def EnablePwStatusClear(self, value):
        self._set_attribute('enablePwStatusClear', value)

    @property
    def EnablePwStatusFault(self):
        """This signifies the enablement of the PW Status Fault.

        Returns:
            bool
        """
        return self._get_attribute('enablePwStatusFault')
    @EnablePwStatusFault.setter
    def EnablePwStatusFault(self, value):
        self._set_attribute('enablePwStatusFault', value)

    @property
    def IsDmLearnedInformationRefreshed(self):
        """This signifies the refresheing of the DM learned information.

        Returns:
            bool
        """
        return self._get_attribute('isDmLearnedInformationRefreshed')

    @property
    def IsGeneralLearnedInformationRefreshed(self):
        """This signifies the refereshing of the general learned information.

        Returns:
            bool
        """
        return self._get_attribute('isGeneralLearnedInformationRefreshed')

    @property
    def IsLmLearnedInformationRefreshed(self):
        """This signifies the refresheing of the LM learned information.

        Returns:
            bool
        """
        return self._get_attribute('isLmLearnedInformationRefreshed')

    @property
    def IsPingLearnedInformationRefreshed(self):
        """This signifies the refresheing of the Ping learned information.

        Returns:
            bool
        """
        return self._get_attribute('isPingLearnedInformationRefreshed')

    @property
    def IsTraceRouteLearnedInformationRefreshed(self):
        """This signifies the refresheing of the Trace Route learned information.

        Returns:
            bool
        """
        return self._get_attribute('isTraceRouteLearnedInformationRefreshed')

    @property
    def LastDmResponseTimeout(self):
        """This signifies the last DM Response Timeout.

        Returns:
            number
        """
        return self._get_attribute('lastDmResponseTimeout')
    @LastDmResponseTimeout.setter
    def LastDmResponseTimeout(self, value):
        self._set_attribute('lastDmResponseTimeout', value)

    @property
    def LastLmResponseTimeout(self):
        """This signifies the last LM response timeout.

        Returns:
            number
        """
        return self._get_attribute('lastLmResponseTimeout')
    @LastLmResponseTimeout.setter
    def LastLmResponseTimeout(self, value):
        self._set_attribute('lastLmResponseTimeout', value)

    @property
    def LmInitialRxValue(self):
        """This signifies the LM Initial Rx value.

        Returns:
            number
        """
        return self._get_attribute('lmInitialRxValue')
    @LmInitialRxValue.setter
    def LmInitialRxValue(self, value):
        self._set_attribute('lmInitialRxValue', value)

    @property
    def LmInitialTxValue(self):
        """This signifies the LM Initial Tx value.

        Returns:
            number
        """
        return self._get_attribute('lmInitialTxValue')
    @LmInitialTxValue.setter
    def LmInitialTxValue(self, value):
        self._set_attribute('lmInitialTxValue', value)

    @property
    def LmInterval(self):
        """This signifies the LM interval in milliseconds.

        Returns:
            number
        """
        return self._get_attribute('lmInterval')
    @LmInterval.setter
    def LmInterval(self, value):
        self._set_attribute('lmInterval', value)

    @property
    def LmIterations(self):
        """This signifies the number of LM queries to be sent.

        Returns:
            number
        """
        return self._get_attribute('lmIterations')
    @LmIterations.setter
    def LmIterations(self, value):
        self._set_attribute('lmIterations', value)

    @property
    def LmMode(self):
        """This signifies the LM mode. Possible values include Response Expected and No Response Expected.

        Returns:
            str(responseExpected|noResponseExpected)
        """
        return self._get_attribute('lmMode')
    @LmMode.setter
    def LmMode(self, value):
        self._set_attribute('lmMode', value)

    @property
    def LmRxStep(self):
        """This signifies the LM Rx step value.

        Returns:
            number
        """
        return self._get_attribute('lmRxStep')
    @LmRxStep.setter
    def LmRxStep(self, value):
        self._set_attribute('lmRxStep', value)

    @property
    def LmTrafficClass(self):
        """This signifies the LM Traffic Class.

        Returns:
            number
        """
        return self._get_attribute('lmTrafficClass')
    @LmTrafficClass.setter
    def LmTrafficClass(self, value):
        self._set_attribute('lmTrafficClass', value)

    @property
    def LmTxStep(self):
        """This signifies the LM Tx Step value.

        Returns:
            number
        """
        return self._get_attribute('lmTxStep')
    @LmTxStep.setter
    def LmTxStep(self, value):
        self._set_attribute('lmTxStep', value)

    @property
    def LmType(self):
        """This signifies the LM type. The possible values include IETF and Y.1731.

        Returns:
            str(ietf|y1731)
        """
        return self._get_attribute('lmType')
    @LmType.setter
    def LmType(self, value):
        self._set_attribute('lmType', value)

    @property
    def LspPingEncapsulationType(self):
        """This signifies the encapsulation type with which the lsp ping request message will be sent out. The possible values include UDP-IP-GAch and GAch.

        Returns:
            str(GAch|UDP over IP over GAch)
        """
        return self._get_attribute('lspPingEncapsulationType')
    @LspPingEncapsulationType.setter
    def LspPingEncapsulationType(self, value):
        self._set_attribute('lspPingEncapsulationType', value)

    @property
    def LspPingResponseTimeout(self):
        """This signifies the response timeout in milliseconds.

        Returns:
            number
        """
        return self._get_attribute('lspPingResponseTimeout')
    @LspPingResponseTimeout.setter
    def LspPingResponseTimeout(self, value):
        self._set_attribute('lspPingResponseTimeout', value)

    @property
    def LspPingTtlValue(self):
        """This signifies the LSP Ping Ttl value.

        Returns:
            number
        """
        return self._get_attribute('lspPingTtlValue')
    @LspPingTtlValue.setter
    def LspPingTtlValue(self, value):
        self._set_attribute('lspPingTtlValue', value)

    @property
    def LspTraceRouteEncapsulationType(self):
        """This signifies the encapsulation type with which the Trace route request message will be sen out. The possible values include UDP-IP-GAch and GAch.

        Returns:
            str(GAch|UDP over IP over GAch)
        """
        return self._get_attribute('lspTraceRouteEncapsulationType')
    @LspTraceRouteEncapsulationType.setter
    def LspTraceRouteEncapsulationType(self, value):
        self._set_attribute('lspTraceRouteEncapsulationType', value)

    @property
    def LspTraceRouteResponseTimeout(self):
        """This signifies the response timeout in milliseconds.

        Returns:
            number
        """
        return self._get_attribute('lspTraceRouteResponseTimeout')
    @LspTraceRouteResponseTimeout.setter
    def LspTraceRouteResponseTimeout(self, value):
        self._set_attribute('lspTraceRouteResponseTimeout', value)

    @property
    def LspTraceRouteTtlLimit(self):
        """This signifies the max TTL till which the Echo Request will be sent out as part of trace route process.

        Returns:
            number
        """
        return self._get_attribute('lspTraceRouteTtlLimit')
    @LspTraceRouteTtlLimit.setter
    def LspTraceRouteTtlLimit(self, value):
        self._set_attribute('lspTraceRouteTtlLimit', value)

    @property
    def MinRxInterval(self):
        """This signifies the minimum receive interval of cc messages in millisecond, at the source side that the user intends to set on the fly.

        Returns:
            str(10|100|1000|10000|3.33|60000|600000)
        """
        return self._get_attribute('minRxInterval')
    @MinRxInterval.setter
    def MinRxInterval(self, value):
        self._set_attribute('minRxInterval', value)

    @property
    def MinTxInterval(self):
        """This signifies the learned information minimum transmit interval, in milliseconds. This specifies the minimum transmit interval of cc messages in millisecond, at the source side that the user intends to set on the fly.

        Returns:
            str(10|100|1000|10000|3.33|60000|600000)
        """
        return self._get_attribute('minTxInterval')
    @MinTxInterval.setter
    def MinTxInterval(self, value):
        self._set_attribute('minTxInterval', value)

    @property
    def MisconnectivityDefect(self):
        """To enable misconnectivity defect on the fly by changing LSP/PW MEP/MEG Id parameter or Your Discriminator on the source side.

        Returns:
            bool
        """
        return self._get_attribute('misconnectivityDefect')
    @MisconnectivityDefect.setter
    def MisconnectivityDefect(self, value):
        self._set_attribute('misconnectivityDefect', value)

    @property
    def MisconnectivityDefectOption(self):
        """To enable misconnectivity defect on the fly by changing LSP/PW MEP/MEG Id parameter or Your Discriminator on the source side.

        Returns:
            str(unexpectedMepId|unexpectedYourDiscriminator)
        """
        return self._get_attribute('misconnectivityDefectOption')
    @MisconnectivityDefectOption.setter
    def MisconnectivityDefectOption(self, value):
        self._set_attribute('misconnectivityDefectOption', value)

    @property
    def OnDemandCvDownstreamAddressType(self):
        """This signifies the Address Type of the Downstream or Detailed Downstream Mapping TLV. This can be of three types.

        Returns:
            str(ipv4Numbered|ipv4Unnumbered|nonIp)
        """
        return self._get_attribute('onDemandCvDownstreamAddressType')
    @OnDemandCvDownstreamAddressType.setter
    def OnDemandCvDownstreamAddressType(self, value):
        self._set_attribute('onDemandCvDownstreamAddressType', value)

    @property
    def OnDemandCvDownstreamIpAddress(self):
        """This signifies the inclusion of the IP address in Downstream or Detailed Downstream Mapping TLV. This takes input in ip address format.

        Returns:
            str
        """
        return self._get_attribute('onDemandCvDownstreamIpAddress')
    @OnDemandCvDownstreamIpAddress.setter
    def OnDemandCvDownstreamIpAddress(self, value):
        self._set_attribute('onDemandCvDownstreamIpAddress', value)

    @property
    def OnDemandCvDsIflag(self):
        """This signifies the setting of I bit in the DS Flag of Downstream or Detailed Downstream Mapping TLV.

        Returns:
            bool
        """
        return self._get_attribute('onDemandCvDsIflag')
    @OnDemandCvDsIflag.setter
    def OnDemandCvDsIflag(self, value):
        self._set_attribute('onDemandCvDsIflag', value)

    @property
    def OnDemandCvDsNflag(self):
        """If set true, N bit is set in the DS Flag of Downstream or Detailed Downstream Mapping TLV.

        Returns:
            bool
        """
        return self._get_attribute('onDemandCvDsNflag')
    @OnDemandCvDsNflag.setter
    def OnDemandCvDsNflag(self, value):
        self._set_attribute('onDemandCvDsNflag', value)

    @property
    def OnDemandCvEgressIfNumber(self):
        """This signifies the Egress If Number, if address type of Downstream or Detailed Downstream Mapping TLV is set to nonIP.

        Returns:
            number
        """
        return self._get_attribute('onDemandCvEgressIfNumber')
    @OnDemandCvEgressIfNumber.setter
    def OnDemandCvEgressIfNumber(self, value):
        self._set_attribute('onDemandCvEgressIfNumber', value)

    @property
    def OnDemandCvIncludeDestinationIdentifierTlv(self):
        """If channel type is set to GAch, this signifies the inclusion of Destination Identifier TLV in the On Demand CV message. Possible values are true or false.

        Returns:
            bool
        """
        return self._get_attribute('onDemandCvIncludeDestinationIdentifierTlv')
    @OnDemandCvIncludeDestinationIdentifierTlv.setter
    def OnDemandCvIncludeDestinationIdentifierTlv(self, value):
        self._set_attribute('onDemandCvIncludeDestinationIdentifierTlv', value)

    @property
    def OnDemandCvIncludeDetailedDownstreamMappingTlv(self):
        """This signifies the inclusion of the Detailed Downstream Mapping TLV in on demand cv message. Possible values are true or false.

        Returns:
            bool
        """
        return self._get_attribute('onDemandCvIncludeDetailedDownstreamMappingTlv')
    @OnDemandCvIncludeDetailedDownstreamMappingTlv.setter
    def OnDemandCvIncludeDetailedDownstreamMappingTlv(self, value):
        self._set_attribute('onDemandCvIncludeDetailedDownstreamMappingTlv', value)

    @property
    def OnDemandCvIncludeDownstreamMappingTlv(self):
        """This signifies the inclusion of Downstream Mapping TLV in on demand cv messages.

        Returns:
            bool
        """
        return self._get_attribute('onDemandCvIncludeDownstreamMappingTlv')
    @OnDemandCvIncludeDownstreamMappingTlv.setter
    def OnDemandCvIncludeDownstreamMappingTlv(self, value):
        self._set_attribute('onDemandCvIncludeDownstreamMappingTlv', value)

    @property
    def OnDemandCvIncludePadTlv(self):
        """This signifies the inclusion of Pad TLV in on demand cv messages (ping or traceroute).

        Returns:
            bool
        """
        return self._get_attribute('onDemandCvIncludePadTlv')
    @OnDemandCvIncludePadTlv.setter
    def OnDemandCvIncludePadTlv(self, value):
        self._set_attribute('onDemandCvIncludePadTlv', value)

    @property
    def OnDemandCvIncludeReplyTosByteTlv(self):
        """This signifies the inclusion of Reply Tos Byte TLV in on demand cv messages, if channel type is configured ip-udp-gach.

        Returns:
            bool
        """
        return self._get_attribute('onDemandCvIncludeReplyTosByteTlv')
    @OnDemandCvIncludeReplyTosByteTlv.setter
    def OnDemandCvIncludeReplyTosByteTlv(self, value):
        self._set_attribute('onDemandCvIncludeReplyTosByteTlv', value)

    @property
    def OnDemandCvIncludeSourceIdentifierTlv(self):
        """If channel type is set to GAch, this signifies the inclusion of Source Identifier TLV in the On Demand CV message. Possible values are true or false.

        Returns:
            bool
        """
        return self._get_attribute('onDemandCvIncludeSourceIdentifierTlv')
    @OnDemandCvIncludeSourceIdentifierTlv.setter
    def OnDemandCvIncludeSourceIdentifierTlv(self, value):
        self._set_attribute('onDemandCvIncludeSourceIdentifierTlv', value)

    @property
    def OnDemandCvIngressIfNumber(self):
        """This signifies the Ingress If Number, if address type of Downstream or Detailed Downstream Mapping TLV is set to nonIP.

        Returns:
            number
        """
        return self._get_attribute('onDemandCvIngressIfNumber')
    @OnDemandCvIngressIfNumber.setter
    def OnDemandCvIngressIfNumber(self, value):
        self._set_attribute('onDemandCvIngressIfNumber', value)

    @property
    def OnDemandCvNumberedDownstreamInterfaceAddress(self):
        """If the address type of Downstream Address TLV is set to ipv4Numbered, it signifies the numbered Interface Address. This takes value in ip address format.

        Returns:
            str
        """
        return self._get_attribute('onDemandCvNumberedDownstreamInterfaceAddress')
    @OnDemandCvNumberedDownstreamInterfaceAddress.setter
    def OnDemandCvNumberedDownstreamInterfaceAddress(self, value):
        self._set_attribute('onDemandCvNumberedDownstreamInterfaceAddress', value)

    @property
    def OnDemandCvPadTlvFirstOctet(self):
        """This signifies the value of first octet of Pad TLV. The possible values are copy or drop.

        Returns:
            str(drop|copy)
        """
        return self._get_attribute('onDemandCvPadTlvFirstOctet')
    @OnDemandCvPadTlvFirstOctet.setter
    def OnDemandCvPadTlvFirstOctet(self, value):
        self._set_attribute('onDemandCvPadTlvFirstOctet', value)

    @property
    def OnDemandCvPadTlvLength(self):
        """This signifies the inclusion of Pad TLV length in On Demand CV message.

        Returns:
            number
        """
        return self._get_attribute('onDemandCvPadTlvLength')
    @OnDemandCvPadTlvLength.setter
    def OnDemandCvPadTlvLength(self, value):
        self._set_attribute('onDemandCvPadTlvLength', value)

    @property
    def OnDemandCvTosByte(self):
        """If channel type is set ip-udp-Gach, this signifies the value of Tos Byte field within Reply TOS Byte TLV, included in on demand cv messages.

        Returns:
            number
        """
        return self._get_attribute('onDemandCvTosByte')
    @OnDemandCvTosByte.setter
    def OnDemandCvTosByte(self, value):
        self._set_attribute('onDemandCvTosByte', value)

    @property
    def OnDemandCvUnnumberedDownstreamInterfaceAddress(self):
        """If the address type of Downstream Address TLV is set to ipv4Unnumbered, this signifies the unnumbered Interface Address. This takes value in integer format. The max value can be 4294967295.

        Returns:
            number
        """
        return self._get_attribute('onDemandCvUnnumberedDownstreamInterfaceAddress')
    @OnDemandCvUnnumberedDownstreamInterfaceAddress.setter
    def OnDemandCvUnnumberedDownstreamInterfaceAddress(self, value):
        self._set_attribute('onDemandCvUnnumberedDownstreamInterfaceAddress', value)

    @property
    def Periodicity(self):
        """This signifies the periodicity of the alarm.

        Returns:
            number
        """
        return self._get_attribute('periodicity')
    @Periodicity.setter
    def Periodicity(self, value):
        self._set_attribute('periodicity', value)

    @property
    def PwStatusClearLabelTtl(self):
        """This signifies the PW status clear label Ttl.

        Returns:
            number
        """
        return self._get_attribute('pwStatusClearLabelTtl')
    @PwStatusClearLabelTtl.setter
    def PwStatusClearLabelTtl(self, value):
        self._set_attribute('pwStatusClearLabelTtl', value)

    @property
    def PwStatusClearTransmitInterval(self):
        """This signifies the transmit interval in seconds.

        Returns:
            number
        """
        return self._get_attribute('pwStatusClearTransmitInterval')
    @PwStatusClearTransmitInterval.setter
    def PwStatusClearTransmitInterval(self, value):
        self._set_attribute('pwStatusClearTransmitInterval', value)

    @property
    def PwStatusCode(self):
        """This signifies the selecting of the relevant option from the drop-down on the right hand side.

        Returns:
            number
        """
        return self._get_attribute('pwStatusCode')
    @PwStatusCode.setter
    def PwStatusCode(self, value):
        self._set_attribute('pwStatusCode', value)

    @property
    def PwStatusFaultLabelTtl(self):
        """This signifies the TTL value to be set in the PW label header while sending out PW Status message.

        Returns:
            number
        """
        return self._get_attribute('pwStatusFaultLabelTtl')
    @PwStatusFaultLabelTtl.setter
    def PwStatusFaultLabelTtl(self, value):
        self._set_attribute('pwStatusFaultLabelTtl', value)

    @property
    def PwStatusFaultTransmitInterval(self):
        """This signifies the PW Status Fault Transmit Interval in seconds.

        Returns:
            number
        """
        return self._get_attribute('pwStatusFaultTransmitInterval')
    @PwStatusFaultTransmitInterval.setter
    def PwStatusFaultTransmitInterval(self, value):
        self._set_attribute('pwStatusFaultTransmitInterval', value)

    def update(self, AlarmTrigger=None, AlarmType=None, ApsTriggerType=None, CccvPauseTriggerOption=None, CccvResumeTriggerOption=None, ChangeSessionParameters=None, ClearMisconnectivityDefect=None, CounterType=None, DmInterval=None, DmIterations=None, DmMode=None, DmPadLen=None, DmRequestPaddedReply=None, DmTimeFormat=None, DmTrafficClass=None, DmType=None, EnableAlarm=None, EnableAlarmAis=None, EnableAlarmFastClear=None, EnableAlarmLck=None, EnableAlarmSetLdi=None, EnableApsTrigger=None, EnableCccvPause=None, EnableCccvResume=None, EnableDmTrigger=None, EnableLmTrigger=None, EnableLspPing=None, EnableLspPingFecStackValidation=None, EnableLspPingValidateReversePath=None, EnableLspTraceRoute=None, EnableLspTraceRouteFecStackValidation=None, EnablePwStatusClear=None, EnablePwStatusFault=None, LastDmResponseTimeout=None, LastLmResponseTimeout=None, LmInitialRxValue=None, LmInitialTxValue=None, LmInterval=None, LmIterations=None, LmMode=None, LmRxStep=None, LmTrafficClass=None, LmTxStep=None, LmType=None, LspPingEncapsulationType=None, LspPingResponseTimeout=None, LspPingTtlValue=None, LspTraceRouteEncapsulationType=None, LspTraceRouteResponseTimeout=None, LspTraceRouteTtlLimit=None, MinRxInterval=None, MinTxInterval=None, MisconnectivityDefect=None, MisconnectivityDefectOption=None, OnDemandCvDownstreamAddressType=None, OnDemandCvDownstreamIpAddress=None, OnDemandCvDsIflag=None, OnDemandCvDsNflag=None, OnDemandCvEgressIfNumber=None, OnDemandCvIncludeDestinationIdentifierTlv=None, OnDemandCvIncludeDetailedDownstreamMappingTlv=None, OnDemandCvIncludeDownstreamMappingTlv=None, OnDemandCvIncludePadTlv=None, OnDemandCvIncludeReplyTosByteTlv=None, OnDemandCvIncludeSourceIdentifierTlv=None, OnDemandCvIngressIfNumber=None, OnDemandCvNumberedDownstreamInterfaceAddress=None, OnDemandCvPadTlvFirstOctet=None, OnDemandCvPadTlvLength=None, OnDemandCvTosByte=None, OnDemandCvUnnumberedDownstreamInterfaceAddress=None, Periodicity=None, PwStatusClearLabelTtl=None, PwStatusClearTransmitInterval=None, PwStatusCode=None, PwStatusFaultLabelTtl=None, PwStatusFaultTransmitInterval=None):
        """Updates a child instance of learnedInformation on the server.

        Args:
            AlarmTrigger (str(clear|start)): This signifies the alarm trigger. Possible values include Clear and Start.
            AlarmType (str(ietf|y1731)): This signifies the alarm type. Possible values include IETF and Y.1731.
            ApsTriggerType (str(clear|forcedSwitch|manualSwitchToProtect|manualSwitchToWorking|lockout|exercise|freeze)): This signifies the Trigger type. Possible values include Clear, Exercise, Forced Switch, Freeze, Lockout, Manual Switch To Protect and Manual Switch To Working.
            CccvPauseTriggerOption (str(tx|rx|txRx)): This signifies the cccv pause trigger option. Possible values include TX, RX and TXRX.
            CccvResumeTriggerOption (str(tx|rx|txRx)): This signifies the cccv resume trigger option. Possible values include Tx, Rx and TxRx.
            ChangeSessionParameters (bool): This specifies the minimum receive interval of cc messages in millisecond, at the source side that the user intends to set on the fly.
            ClearMisconnectivityDefect (bool): If set true all the misconnectivity defects that have been triggered earlier with any type gets cleared.
            CounterType (str(32Bit|64Bit)): This signifies the LM Counter Type. Possible values include 32 Bit (default) and 64 Bit.
            DmInterval (number): This signifies the DM interval in milliseconds.
            DmIterations (number): This signifies the total number of DM queries to be sent.
            DmMode (str(noResponseExpected|responseExpected)): This signifies the DM mode. The possible values include Response Expected and No Response Expected.
            DmPadLen (number): This signifies the DM pad length.
            DmRequestPaddedReply (bool): This signifies the DM request as a padded reply.
            DmTimeFormat (str(ieee|ntp)): This signifies the DM time format. The possible values include IEEE and NTP.
            DmTrafficClass (number): This signifies the DM traffic class value.
            DmType (str(ietf|y1731)): This signifies the DM Type. Possible values include IETF and Y.1731.
            EnableAlarm (bool): This signifies the enablement of the Alarm and the fields under it.
            EnableAlarmAis (bool): This signifies the enablement of the Alarm AIS.
            EnableAlarmFastClear (bool): Clears the Alarm State in 10 seconds
            EnableAlarmLck (bool): This signifies the enablement of the Alarm lck.
            EnableAlarmSetLdi (bool): This signifies the enablement of the Alarm Set LDI.
            EnableApsTrigger (bool): This signifies the enablement of APS trigger.
            EnableCccvPause (bool): This signifies the enabling of CCCV Pause.
            EnableCccvResume (bool): This signifies the enablement of CCCV Resume.
            EnableDmTrigger (bool): This signifies the enablement of the DM trigger.
            EnableLmTrigger (bool): This signifies the enablement of the LM trigger.
            EnableLspPing (bool): This signifies the enablement of the LSP Ping.
            EnableLspPingFecStackValidation (bool): This signifies the enablement of the FEC Stack Validation.
            EnableLspPingValidateReversePath (bool): If true validate reverse path bit is set in lsp ping message.
            EnableLspTraceRoute (bool): This signifies the enablement of the lsp traceroute.
            EnableLspTraceRouteFecStackValidation (bool): This signifies the enablement of the FEC Stack Validation.
            EnablePwStatusClear (bool): This signifies the enablement of the PW Status Clear and the fields under it.
            EnablePwStatusFault (bool): This signifies the enablement of the PW Status Fault.
            LastDmResponseTimeout (number): This signifies the last DM Response Timeout.
            LastLmResponseTimeout (number): This signifies the last LM response timeout.
            LmInitialRxValue (number): This signifies the LM Initial Rx value.
            LmInitialTxValue (number): This signifies the LM Initial Tx value.
            LmInterval (number): This signifies the LM interval in milliseconds.
            LmIterations (number): This signifies the number of LM queries to be sent.
            LmMode (str(responseExpected|noResponseExpected)): This signifies the LM mode. Possible values include Response Expected and No Response Expected.
            LmRxStep (number): This signifies the LM Rx step value.
            LmTrafficClass (number): This signifies the LM Traffic Class.
            LmTxStep (number): This signifies the LM Tx Step value.
            LmType (str(ietf|y1731)): This signifies the LM type. The possible values include IETF and Y.1731.
            LspPingEncapsulationType (str(GAch|UDP over IP over GAch)): This signifies the encapsulation type with which the lsp ping request message will be sent out. The possible values include UDP-IP-GAch and GAch.
            LspPingResponseTimeout (number): This signifies the response timeout in milliseconds.
            LspPingTtlValue (number): This signifies the LSP Ping Ttl value.
            LspTraceRouteEncapsulationType (str(GAch|UDP over IP over GAch)): This signifies the encapsulation type with which the Trace route request message will be sen out. The possible values include UDP-IP-GAch and GAch.
            LspTraceRouteResponseTimeout (number): This signifies the response timeout in milliseconds.
            LspTraceRouteTtlLimit (number): This signifies the max TTL till which the Echo Request will be sent out as part of trace route process.
            MinRxInterval (str(10|100|1000|10000|3.33|60000|600000)): This signifies the minimum receive interval of cc messages in millisecond, at the source side that the user intends to set on the fly.
            MinTxInterval (str(10|100|1000|10000|3.33|60000|600000)): This signifies the learned information minimum transmit interval, in milliseconds. This specifies the minimum transmit interval of cc messages in millisecond, at the source side that the user intends to set on the fly.
            MisconnectivityDefect (bool): To enable misconnectivity defect on the fly by changing LSP/PW MEP/MEG Id parameter or Your Discriminator on the source side.
            MisconnectivityDefectOption (str(unexpectedMepId|unexpectedYourDiscriminator)): To enable misconnectivity defect on the fly by changing LSP/PW MEP/MEG Id parameter or Your Discriminator on the source side.
            OnDemandCvDownstreamAddressType (str(ipv4Numbered|ipv4Unnumbered|nonIp)): This signifies the Address Type of the Downstream or Detailed Downstream Mapping TLV. This can be of three types.
            OnDemandCvDownstreamIpAddress (str): This signifies the inclusion of the IP address in Downstream or Detailed Downstream Mapping TLV. This takes input in ip address format.
            OnDemandCvDsIflag (bool): This signifies the setting of I bit in the DS Flag of Downstream or Detailed Downstream Mapping TLV.
            OnDemandCvDsNflag (bool): If set true, N bit is set in the DS Flag of Downstream or Detailed Downstream Mapping TLV.
            OnDemandCvEgressIfNumber (number): This signifies the Egress If Number, if address type of Downstream or Detailed Downstream Mapping TLV is set to nonIP.
            OnDemandCvIncludeDestinationIdentifierTlv (bool): If channel type is set to GAch, this signifies the inclusion of Destination Identifier TLV in the On Demand CV message. Possible values are true or false.
            OnDemandCvIncludeDetailedDownstreamMappingTlv (bool): This signifies the inclusion of the Detailed Downstream Mapping TLV in on demand cv message. Possible values are true or false.
            OnDemandCvIncludeDownstreamMappingTlv (bool): This signifies the inclusion of Downstream Mapping TLV in on demand cv messages.
            OnDemandCvIncludePadTlv (bool): This signifies the inclusion of Pad TLV in on demand cv messages (ping or traceroute).
            OnDemandCvIncludeReplyTosByteTlv (bool): This signifies the inclusion of Reply Tos Byte TLV in on demand cv messages, if channel type is configured ip-udp-gach.
            OnDemandCvIncludeSourceIdentifierTlv (bool): If channel type is set to GAch, this signifies the inclusion of Source Identifier TLV in the On Demand CV message. Possible values are true or false.
            OnDemandCvIngressIfNumber (number): This signifies the Ingress If Number, if address type of Downstream or Detailed Downstream Mapping TLV is set to nonIP.
            OnDemandCvNumberedDownstreamInterfaceAddress (str): If the address type of Downstream Address TLV is set to ipv4Numbered, it signifies the numbered Interface Address. This takes value in ip address format.
            OnDemandCvPadTlvFirstOctet (str(drop|copy)): This signifies the value of first octet of Pad TLV. The possible values are copy or drop.
            OnDemandCvPadTlvLength (number): This signifies the inclusion of Pad TLV length in On Demand CV message.
            OnDemandCvTosByte (number): If channel type is set ip-udp-Gach, this signifies the value of Tos Byte field within Reply TOS Byte TLV, included in on demand cv messages.
            OnDemandCvUnnumberedDownstreamInterfaceAddress (number): If the address type of Downstream Address TLV is set to ipv4Unnumbered, this signifies the unnumbered Interface Address. This takes value in integer format. The max value can be 4294967295.
            Periodicity (number): This signifies the periodicity of the alarm.
            PwStatusClearLabelTtl (number): This signifies the PW status clear label Ttl.
            PwStatusClearTransmitInterval (number): This signifies the transmit interval in seconds.
            PwStatusCode (number): This signifies the selecting of the relevant option from the drop-down on the right hand side.
            PwStatusFaultLabelTtl (number): This signifies the TTL value to be set in the PW label header while sending out PW Status message.
            PwStatusFaultTransmitInterval (number): This signifies the PW Status Fault Transmit Interval in seconds.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def ClearRecordsForTrigger(self):
        """Executes the clearRecordsForTrigger operation on the server.

        This option is used to clear the selected learned information using the command addRecordForTrigger

            Returns:
                bool: NOT DEFINED

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('clearRecordsForTrigger', payload=payload, response_object=None)

    def RefreshLearnedInformation(self):
        """Executes the refreshLearnedInformation operation on the server.

        This signifies the refreshing of the learned information of MPLSTP router.

            Returns:
                bool: NOT DEFINED

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('refreshLearnedInformation', payload=payload, response_object=None)

    def Trigger(self):
        """Executes the trigger operation on the server.

        This signifies the learned info trigger settings.

            Returns:
                bool: NOT DEFINED

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('trigger', payload=payload, response_object=None)
