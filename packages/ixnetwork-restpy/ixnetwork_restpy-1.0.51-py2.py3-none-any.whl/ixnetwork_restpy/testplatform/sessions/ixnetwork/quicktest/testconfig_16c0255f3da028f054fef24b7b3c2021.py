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


class TestConfig(Base):
    """The IxNetwork Test Configuration feature provides the ability to run predefined tests and allows the user to set some global test parameters for the individual test types.
    The TestConfig class encapsulates a required testConfig resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'testConfig'

    def __init__(self, parent):
        super(TestConfig, self).__init__(parent)

    @property
    def ApplyMode(self):
        """NOT DEFINED

        Returns:
            str
        """
        return self._get_attribute('applyMode')
    @ApplyMode.setter
    def ApplyMode(self, value):
        self._set_attribute('applyMode', value)

    @property
    def AssignGroupType(self):
        """Assigns the group type.

        Returns:
            str(accumulated|distributed)
        """
        return self._get_attribute('assignGroupType')
    @AssignGroupType.setter
    def AssignGroupType(self, value):
        self._set_attribute('assignGroupType', value)

    @property
    def BidirectionalOptionEnabled(self):
        """If true, enables the bidirectional option.

        Returns:
            bool
        """
        return self._get_attribute('bidirectionalOptionEnabled')
    @BidirectionalOptionEnabled.setter
    def BidirectionalOptionEnabled(self, value):
        self._set_attribute('bidirectionalOptionEnabled', value)

    @property
    def BinaryBackoff(self):
        """NOT DEFINED

        Returns:
            number
        """
        return self._get_attribute('binaryBackoff')
    @BinaryBackoff.setter
    def BinaryBackoff(self, value):
        self._set_attribute('binaryBackoff', value)

    @property
    def BinaryFrameLossUnit(self):
        """NOT DEFINED

        Returns:
            str(%|frames)
        """
        return self._get_attribute('binaryFrameLossUnit')
    @BinaryFrameLossUnit.setter
    def BinaryFrameLossUnit(self, value):
        self._set_attribute('binaryFrameLossUnit', value)

    @property
    def BinaryResolution(self):
        """NOT DEFINED

        Returns:
            number
        """
        return self._get_attribute('binaryResolution')
    @BinaryResolution.setter
    def BinaryResolution(self, value):
        self._set_attribute('binaryResolution', value)

    @property
    def BinaryTolerance(self):
        """NOT DEFINED

        Returns:
            number
        """
        return self._get_attribute('binaryTolerance')
    @BinaryTolerance.setter
    def BinaryTolerance(self, value):
        self._set_attribute('binaryTolerance', value)

    @property
    def CalculateJitter(self):
        """If true, calculates jitter.

        Returns:
            bool
        """
        return self._get_attribute('calculateJitter')
    @CalculateJitter.setter
    def CalculateJitter(self, value):
        self._set_attribute('calculateJitter', value)

    @property
    def CalculateLatency(self):
        """If true, calculates the latency.

        Returns:
            bool
        """
        return self._get_attribute('calculateLatency')
    @CalculateLatency.setter
    def CalculateLatency(self, value):
        self._set_attribute('calculateLatency', value)

    @property
    def CountRandomFrameSize(self):
        """If true, frame sizes are counted at random.

        Returns:
            number
        """
        return self._get_attribute('countRandomFrameSize')
    @CountRandomFrameSize.setter
    def CountRandomFrameSize(self, value):
        self._set_attribute('countRandomFrameSize', value)

    @property
    def DelayAfterTransmit(self):
        """The amount of delay after every transmit.

        Returns:
            number
        """
        return self._get_attribute('delayAfterTransmit')
    @DelayAfterTransmit.setter
    def DelayAfterTransmit(self, value):
        self._set_attribute('delayAfterTransmit', value)

    @property
    def DummyTrafficId(self):
        """The id of the monitor traffic item

        Returns:
            str
        """
        return self._get_attribute('dummyTrafficId')
    @DummyTrafficId.setter
    def DummyTrafficId(self, value):
        self._set_attribute('dummyTrafficId', value)

    @property
    def Duration(self):
        """The duration of the test in hours, which is used to calculate the number of framesto transmit. (read only)

        Returns:
            number
        """
        return self._get_attribute('duration')
    @Duration.setter
    def Duration(self, value):
        self._set_attribute('duration', value)

    @property
    def EnableDataIntegrity(self):
        """If true, enables data integrity test.

        Returns:
            bool
        """
        return self._get_attribute('enableDataIntegrity')
    @EnableDataIntegrity.setter
    def EnableDataIntegrity(self, value):
        self._set_attribute('enableDataIntegrity', value)

    @property
    def EnableLayer1Rate(self):
        """NOT DEFINED

        Returns:
            bool
        """
        return self._get_attribute('enableLayer1Rate')
    @EnableLayer1Rate.setter
    def EnableLayer1Rate(self, value):
        self._set_attribute('enableLayer1Rate', value)

    @property
    def EnableLeaveGroup(self):
        """If true, the leave group is enabled.

        Returns:
            bool
        """
        return self._get_attribute('enableLeaveGroup')
    @EnableLeaveGroup.setter
    def EnableLeaveGroup(self, value):
        self._set_attribute('enableLeaveGroup', value)

    @property
    def EnableMinFrameSize(self):
        """If true, enables minimum frame size.

        Returns:
            bool
        """
        return self._get_attribute('enableMinFrameSize')
    @EnableMinFrameSize.setter
    def EnableMinFrameSize(self, value):
        self._set_attribute('enableMinFrameSize', value)

    @property
    def EnableMulticastQuerier(self):
        """Enable Multicast Querier Settings

        Returns:
            bool
        """
        return self._get_attribute('enableMulticastQuerier')
    @EnableMulticastQuerier.setter
    def EnableMulticastQuerier(self, value):
        self._set_attribute('enableMulticastQuerier', value)

    @property
    def EnableOldStatsForReef(self):
        """Enables old statistics for reef.

        Returns:
            bool
        """
        return self._get_attribute('enableOldStatsForReef')
    @EnableOldStatsForReef.setter
    def EnableOldStatsForReef(self, value):
        self._set_attribute('enableOldStatsForReef', value)

    @property
    def FloodedFramesEnabled(self):
        """Enables the flooded frames statistic

        Returns:
            bool
        """
        return self._get_attribute('floodedFramesEnabled')
    @FloodedFramesEnabled.setter
    def FloodedFramesEnabled(self, value):
        self._set_attribute('floodedFramesEnabled', value)

    @property
    def FloodedFramesProcessing(self):
        """NOT DEFINED

        Returns:
            bool
        """
        return self._get_attribute('floodedFramesProcessing')
    @FloodedFramesProcessing.setter
    def FloodedFramesProcessing(self, value):
        self._set_attribute('floodedFramesProcessing', value)

    @property
    def FloodedFramesTemp(self):
        """NOT DEFINED

        Returns:
            str
        """
        return self._get_attribute('floodedFramesTemp')
    @FloodedFramesTemp.setter
    def FloodedFramesTemp(self, value):
        self._set_attribute('floodedFramesTemp', value)

    @property
    def ForceRegenerate(self):
        """If true, forces regeneration.

        Returns:
            bool
        """
        return self._get_attribute('forceRegenerate')
    @ForceRegenerate.setter
    def ForceRegenerate(self, value):
        self._set_attribute('forceRegenerate', value)

    @property
    def FrameSizeMode(self):
        """This attribute is the frame size mode for the Quad Gaussian. The Quad Gaussianis the superposition of four Gaussian distributions.

        Returns:
            str(custom|increment|random)
        """
        return self._get_attribute('frameSizeMode')
    @FrameSizeMode.setter
    def FrameSizeMode(self, value):
        self._set_attribute('frameSizeMode', value)

    @property
    def FramesizeList(self):
        """The list of frame sizes.

        Returns:
            list(str)
        """
        return self._get_attribute('framesizeList')
    @FramesizeList.setter
    def FramesizeList(self, value):
        self._set_attribute('framesizeList', value)

    @property
    def Gap(self):
        """The gap in transmission of frames.

        Returns:
            number
        """
        return self._get_attribute('gap')
    @Gap.setter
    def Gap(self, value):
        self._set_attribute('gap', value)

    @property
    def GroupDistributionType(self):
        """Indicates the group distribution type.

        Returns:
            str(acrossHosts|acrossPorts)
        """
        return self._get_attribute('groupDistributionType')
    @GroupDistributionType.setter
    def GroupDistributionType(self, value):
        self._set_attribute('groupDistributionType', value)

    @property
    def IgmpV1Timeout(self):
        """The IGMPv1 timeout value.

        Returns:
            number
        """
        return self._get_attribute('igmpV1Timeout')
    @IgmpV1Timeout.setter
    def IgmpV1Timeout(self, value):
        self._set_attribute('igmpV1Timeout', value)

    @property
    def IgmpVersion(self):
        """The igmp version.

        Returns:
            number
        """
        return self._get_attribute('igmpVersion')
    @IgmpVersion.setter
    def IgmpVersion(self, value):
        self._set_attribute('igmpVersion', value)

    @property
    def Igmpv3MessageType(self):
        """It gives details about the igmpv3 message type in the test configuration

        Returns:
            str(exclude|include)
        """
        return self._get_attribute('igmpv3MessageType')
    @Igmpv3MessageType.setter
    def Igmpv3MessageType(self, value):
        self._set_attribute('igmpv3MessageType', value)

    @property
    def Igmpv3SourceAddrList(self):
        """It gives details about the igmpv3 source address list in the test configuration

        Returns:
            str
        """
        return self._get_attribute('igmpv3SourceAddrList')
    @Igmpv3SourceAddrList.setter
    def Igmpv3SourceAddrList(self, value):
        self._set_attribute('igmpv3SourceAddrList', value)

    @property
    def IncrAddresses(self):
        """If true, the MAC address is incremented.

        Returns:
            number
        """
        return self._get_attribute('incrAddresses')
    @IncrAddresses.setter
    def IncrAddresses(self, value):
        self._set_attribute('incrAddresses', value)

    @property
    def IncrementLoadUnit(self):
        """Signifies the incremented load unit.

        Returns:
            str(bpsRate|fpsRate|gbpsRate|gBpsRate|kbpsRate|kBpsRate|mbpsRate|mBpsRate|percentMaxRate)
        """
        return self._get_attribute('incrementLoadUnit')
    @IncrementLoadUnit.setter
    def IncrementLoadUnit(self, value):
        self._set_attribute('incrementLoadUnit', value)

    @property
    def InitialBinaryLoadIntegerValues(self):
        """NOT DEFINED

        Returns:
            number
        """
        return self._get_attribute('initialBinaryLoadIntegerValues')
    @InitialBinaryLoadIntegerValues.setter
    def InitialBinaryLoadIntegerValues(self, value):
        self._set_attribute('initialBinaryLoadIntegerValues', value)

    @property
    def InitialLoadRate(self):
        """The initial load rate.

        Returns:
            str
        """
        return self._get_attribute('initialLoadRate')
    @InitialLoadRate.setter
    def InitialLoadRate(self, value):
        self._set_attribute('initialLoadRate', value)

    @property
    def Ipv4Address(self):
        """The allocated IPv4 address for this interface.

        Returns:
            str
        """
        return self._get_attribute('ipv4Address')
    @Ipv4Address.setter
    def Ipv4Address(self, value):
        self._set_attribute('ipv4Address', value)

    @property
    def Ipv6Address(self):
        """The allocated IPv6address for this interface .

        Returns:
            str
        """
        return self._get_attribute('ipv6Address')
    @Ipv6Address.setter
    def Ipv6Address(self, value):
        self._set_attribute('ipv6Address', value)

    @property
    def IsIPv6(self):
        """It signifies the ipv6 traffic type.

        Returns:
            str
        """
        return self._get_attribute('isIPv6')
    @IsIPv6.setter
    def IsIPv6(self, value):
        self._set_attribute('isIPv6', value)

    @property
    def IsMulticastAutomaticFrameData(self):
        """It signifies the automatic frame data for multicast.

        Returns:
            str
        """
        return self._get_attribute('isMulticastAutomaticFrameData')
    @IsMulticastAutomaticFrameData.setter
    def IsMulticastAutomaticFrameData(self, value):
        self._set_attribute('isMulticastAutomaticFrameData', value)

    @property
    def JoinLeaveMultiplier(self):
        """NOT DEFINED

        Returns:
            number
        """
        return self._get_attribute('joinLeaveMultiplier')
    @JoinLeaveMultiplier.setter
    def JoinLeaveMultiplier(self, value):
        self._set_attribute('joinLeaveMultiplier', value)

    @property
    def JoinLeaveRate(self):
        """The leave rate.

        Returns:
            number
        """
        return self._get_attribute('joinLeaveRate')
    @JoinLeaveRate.setter
    def JoinLeaveRate(self, value):
        self._set_attribute('joinLeaveRate', value)

    @property
    def JoinLeaveWaitTime(self):
        """The wait time for thr leave.

        Returns:
            number
        """
        return self._get_attribute('joinLeaveWaitTime')
    @JoinLeaveWaitTime.setter
    def JoinLeaveWaitTime(self, value):
        self._set_attribute('joinLeaveWaitTime', value)

    @property
    def LatencyBins(self):
        """DEPRECATED Sets the latency bins statistics

        Returns:
            str
        """
        return self._get_attribute('latencyBins')
    @LatencyBins.setter
    def LatencyBins(self, value):
        self._set_attribute('latencyBins', value)

    @property
    def LatencyBinsEnabled(self):
        """Enables the latency bins statistics

        Returns:
            bool
        """
        return self._get_attribute('latencyBinsEnabled')
    @LatencyBinsEnabled.setter
    def LatencyBinsEnabled(self, value):
        self._set_attribute('latencyBinsEnabled', value)

    @property
    def LatencyType(self):
        """The type of latency.

        Returns:
            str(cutThrough|storeForward)
        """
        return self._get_attribute('latencyType')
    @LatencyType.setter
    def LatencyType(self, value):
        self._set_attribute('latencyType', value)

    @property
    def LoadInitialRate(self):
        """The initial rate of the load.

        Returns:
            number
        """
        return self._get_attribute('loadInitialRate')
    @LoadInitialRate.setter
    def LoadInitialRate(self, value):
        self._set_attribute('loadInitialRate', value)

    @property
    def LoadType(self):
        """The type of the payload setting.

        Returns:
            str(binary|step)
        """
        return self._get_attribute('loadType')
    @LoadType.setter
    def LoadType(self, value):
        self._set_attribute('loadType', value)

    @property
    def MapType(self):
        """The POS traffic map type.

        Returns:
            str
        """
        return self._get_attribute('mapType')
    @MapType.setter
    def MapType(self, value):
        self._set_attribute('mapType', value)

    @property
    def MaxBinaryLoadIntegerValue(self):
        """NOT DEFINED

        Returns:
            number
        """
        return self._get_attribute('maxBinaryLoadIntegerValue')
    @MaxBinaryLoadIntegerValue.setter
    def MaxBinaryLoadIntegerValue(self, value):
        self._set_attribute('maxBinaryLoadIntegerValue', value)

    @property
    def MaxIncrementFrameSize(self):
        """The integer that states the maximum amount to which the frame size can be incremented.

        Returns:
            number
        """
        return self._get_attribute('maxIncrementFrameSize')
    @MaxIncrementFrameSize.setter
    def MaxIncrementFrameSize(self, value):
        self._set_attribute('maxIncrementFrameSize', value)

    @property
    def MaxNumGroups(self):
        """NOT DEFINED

        Returns:
            str
        """
        return self._get_attribute('maxNumGroups')
    @MaxNumGroups.setter
    def MaxNumGroups(self, value):
        self._set_attribute('maxNumGroups', value)

    @property
    def MaxRandomFrameSize(self):
        """The integer that states the maximum random amount to which the frame size can be incremented.

        Returns:
            number
        """
        return self._get_attribute('maxRandomFrameSize')
    @MaxRandomFrameSize.setter
    def MaxRandomFrameSize(self, value):
        self._set_attribute('maxRandomFrameSize', value)

    @property
    def MinBinaryLoadIntegerValues(self):
        """NOT DEFINED

        Returns:
            number
        """
        return self._get_attribute('minBinaryLoadIntegerValues')
    @MinBinaryLoadIntegerValues.setter
    def MinBinaryLoadIntegerValues(self, value):
        self._set_attribute('minBinaryLoadIntegerValues', value)

    @property
    def MinIncrementFrameSize(self):
        """The integer that states the minimum amount to which the frame size can be incremented.

        Returns:
            number
        """
        return self._get_attribute('minIncrementFrameSize')
    @MinIncrementFrameSize.setter
    def MinIncrementFrameSize(self, value):
        self._set_attribute('minIncrementFrameSize', value)

    @property
    def MinRandomFrameSize(self):
        """The integer that states the minimum random amount to which the frame size can be incremented.

        Returns:
            number
        """
        return self._get_attribute('minRandomFrameSize')
    @MinRandomFrameSize.setter
    def MinRandomFrameSize(self, value):
        self._set_attribute('minRandomFrameSize', value)

    @property
    def MldVersion(self):
        """The version of the MLD messages.

        Returns:
            number
        """
        return self._get_attribute('mldVersion')
    @MldVersion.setter
    def MldVersion(self, value):
        self._set_attribute('mldVersion', value)

    @property
    def NumAddresses(self):
        """The integer value for the number of addresses.

        Returns:
            number
        """
        return self._get_attribute('numAddresses')
    @NumAddresses.setter
    def NumAddresses(self, value):
        self._set_attribute('numAddresses', value)

    @property
    def NumIterations(self):
        """The number of iterations.

        Returns:
            number
        """
        return self._get_attribute('numIterations')
    @NumIterations.setter
    def NumIterations(self, value):
        self._set_attribute('numIterations', value)

    @property
    def Numtrials(self):
        """Defines how many times each frame size will be tested.

        Returns:
            number
        """
        return self._get_attribute('numtrials')
    @Numtrials.setter
    def Numtrials(self, value):
        self._set_attribute('numtrials', value)

    @property
    def PortDelayEnabled(self):
        """Enables the Port Delay

        Returns:
            bool
        """
        return self._get_attribute('portDelayEnabled')
    @PortDelayEnabled.setter
    def PortDelayEnabled(self, value):
        self._set_attribute('portDelayEnabled', value)

    @property
    def PortDelayUnit(self):
        """Sets the port delay unit in which it will be measured

        Returns:
            str(bytes|nanoseconds)
        """
        return self._get_attribute('portDelayUnit')
    @PortDelayUnit.setter
    def PortDelayUnit(self, value):
        self._set_attribute('portDelayUnit', value)

    @property
    def PortDelayValue(self):
        """Sets the port delay value

        Returns:
            number
        """
        return self._get_attribute('portDelayValue')
    @PortDelayValue.setter
    def PortDelayValue(self, value):
        self._set_attribute('portDelayValue', value)

    @property
    def ProtocolItem(self):
        """Protocol Items

        Returns:
            list(str[None|/api/v1/sessions/1/ixnetwork/vport|/api/v1/sessions/1/ixnetwork/vport?deepchild=lan])
        """
        return self._get_attribute('protocolItem')
    @ProtocolItem.setter
    def ProtocolItem(self, value):
        self._set_attribute('protocolItem', value)

    @property
    def ReportSequenceError(self):
        """Reports sequence errors in the test result.

        Returns:
            bool
        """
        return self._get_attribute('reportSequenceError')
    @ReportSequenceError.setter
    def ReportSequenceError(self, value):
        self._set_attribute('reportSequenceError', value)

    @property
    def ReportTputRateUnit(self):
        """Report identifying the unit for measuring the throughput rate in frames per second.

        Returns:
            str(gbps|gBps|kbps|kBps|mbps|mBps)
        """
        return self._get_attribute('reportTputRateUnit')
    @ReportTputRateUnit.setter
    def ReportTputRateUnit(self, value):
        self._set_attribute('reportTputRateUnit', value)

    @property
    def RouterAlert(self):
        """The router alert selected from the Hop-by-hop Options.

        Returns:
            bool
        """
        return self._get_attribute('routerAlert')
    @RouterAlert.setter
    def RouterAlert(self, value):
        self._set_attribute('routerAlert', value)

    @property
    def ShowDetailedBinaryResults(self):
        """NOT DEFINED

        Returns:
            bool
        """
        return self._get_attribute('showDetailedBinaryResults')
    @ShowDetailedBinaryResults.setter
    def ShowDetailedBinaryResults(self, value):
        self._set_attribute('showDetailedBinaryResults', value)

    @property
    def StepFrameLossUnit(self):
        """NOT DEFINED

        Returns:
            str(%|frames)
        """
        return self._get_attribute('stepFrameLossUnit')
    @StepFrameLossUnit.setter
    def StepFrameLossUnit(self, value):
        self._set_attribute('stepFrameLossUnit', value)

    @property
    def StepIncrementFrameSize(self):
        """The step to increment the frame size.

        Returns:
            number
        """
        return self._get_attribute('stepIncrementFrameSize')
    @StepIncrementFrameSize.setter
    def StepIncrementFrameSize(self, value):
        self._set_attribute('stepIncrementFrameSize', value)

    @property
    def StepTolerance(self):
        """NOT DEFINED

        Returns:
            number
        """
        return self._get_attribute('stepTolerance')
    @StepTolerance.setter
    def StepTolerance(self, value):
        self._set_attribute('stepTolerance', value)

    @property
    def SupportedTrafficTypes(self):
        """The traffic types supported.

        Returns:
            str
        """
        return self._get_attribute('supportedTrafficTypes')
    @SupportedTrafficTypes.setter
    def SupportedTrafficTypes(self, value):
        self._set_attribute('supportedTrafficTypes', value)

    @property
    def TestTrafficType(self):
        """It signifies the test traffic type value.

        Returns:
            str
        """
        return self._get_attribute('testTrafficType')
    @TestTrafficType.setter
    def TestTrafficType(self, value):
        self._set_attribute('testTrafficType', value)

    @property
    def TxDelay(self):
        """The delay recorded in the transmit port.

        Returns:
            number
        """
        return self._get_attribute('txDelay')
    @TxDelay.setter
    def TxDelay(self, value):
        self._set_attribute('txDelay', value)

    def update(self, ApplyMode=None, AssignGroupType=None, BidirectionalOptionEnabled=None, BinaryBackoff=None, BinaryFrameLossUnit=None, BinaryResolution=None, BinaryTolerance=None, CalculateJitter=None, CalculateLatency=None, CountRandomFrameSize=None, DelayAfterTransmit=None, DummyTrafficId=None, Duration=None, EnableDataIntegrity=None, EnableLayer1Rate=None, EnableLeaveGroup=None, EnableMinFrameSize=None, EnableMulticastQuerier=None, EnableOldStatsForReef=None, FloodedFramesEnabled=None, FloodedFramesProcessing=None, FloodedFramesTemp=None, ForceRegenerate=None, FrameSizeMode=None, FramesizeList=None, Gap=None, GroupDistributionType=None, IgmpV1Timeout=None, IgmpVersion=None, Igmpv3MessageType=None, Igmpv3SourceAddrList=None, IncrAddresses=None, IncrementLoadUnit=None, InitialBinaryLoadIntegerValues=None, InitialLoadRate=None, Ipv4Address=None, Ipv6Address=None, IsIPv6=None, IsMulticastAutomaticFrameData=None, JoinLeaveMultiplier=None, JoinLeaveRate=None, JoinLeaveWaitTime=None, LatencyBins=None, LatencyBinsEnabled=None, LatencyType=None, LoadInitialRate=None, LoadType=None, MapType=None, MaxBinaryLoadIntegerValue=None, MaxIncrementFrameSize=None, MaxNumGroups=None, MaxRandomFrameSize=None, MinBinaryLoadIntegerValues=None, MinIncrementFrameSize=None, MinRandomFrameSize=None, MldVersion=None, NumAddresses=None, NumIterations=None, Numtrials=None, PortDelayEnabled=None, PortDelayUnit=None, PortDelayValue=None, ProtocolItem=None, ReportSequenceError=None, ReportTputRateUnit=None, RouterAlert=None, ShowDetailedBinaryResults=None, StepFrameLossUnit=None, StepIncrementFrameSize=None, StepTolerance=None, SupportedTrafficTypes=None, TestTrafficType=None, TxDelay=None):
        """Updates a child instance of testConfig on the server.

        Args:
            ApplyMode (str): NOT DEFINED
            AssignGroupType (str(accumulated|distributed)): Assigns the group type.
            BidirectionalOptionEnabled (bool): If true, enables the bidirectional option.
            BinaryBackoff (number): NOT DEFINED
            BinaryFrameLossUnit (str(%|frames)): NOT DEFINED
            BinaryResolution (number): NOT DEFINED
            BinaryTolerance (number): NOT DEFINED
            CalculateJitter (bool): If true, calculates jitter.
            CalculateLatency (bool): If true, calculates the latency.
            CountRandomFrameSize (number): If true, frame sizes are counted at random.
            DelayAfterTransmit (number): The amount of delay after every transmit.
            DummyTrafficId (str): The id of the monitor traffic item
            Duration (number): The duration of the test in hours, which is used to calculate the number of framesto transmit. (read only)
            EnableDataIntegrity (bool): If true, enables data integrity test.
            EnableLayer1Rate (bool): NOT DEFINED
            EnableLeaveGroup (bool): If true, the leave group is enabled.
            EnableMinFrameSize (bool): If true, enables minimum frame size.
            EnableMulticastQuerier (bool): Enable Multicast Querier Settings
            EnableOldStatsForReef (bool): Enables old statistics for reef.
            FloodedFramesEnabled (bool): Enables the flooded frames statistic
            FloodedFramesProcessing (bool): NOT DEFINED
            FloodedFramesTemp (str): NOT DEFINED
            ForceRegenerate (bool): If true, forces regeneration.
            FrameSizeMode (str(custom|increment|random)): This attribute is the frame size mode for the Quad Gaussian. The Quad Gaussianis the superposition of four Gaussian distributions.
            FramesizeList (list(str)): The list of frame sizes.
            Gap (number): The gap in transmission of frames.
            GroupDistributionType (str(acrossHosts|acrossPorts)): Indicates the group distribution type.
            IgmpV1Timeout (number): The IGMPv1 timeout value.
            IgmpVersion (number): The igmp version.
            Igmpv3MessageType (str(exclude|include)): It gives details about the igmpv3 message type in the test configuration
            Igmpv3SourceAddrList (str): It gives details about the igmpv3 source address list in the test configuration
            IncrAddresses (number): If true, the MAC address is incremented.
            IncrementLoadUnit (str(bpsRate|fpsRate|gbpsRate|gBpsRate|kbpsRate|kBpsRate|mbpsRate|mBpsRate|percentMaxRate)): Signifies the incremented load unit.
            InitialBinaryLoadIntegerValues (number): NOT DEFINED
            InitialLoadRate (str): The initial load rate.
            Ipv4Address (str): The allocated IPv4 address for this interface.
            Ipv6Address (str): The allocated IPv6address for this interface .
            IsIPv6 (str): It signifies the ipv6 traffic type.
            IsMulticastAutomaticFrameData (str): It signifies the automatic frame data for multicast.
            JoinLeaveMultiplier (number): NOT DEFINED
            JoinLeaveRate (number): The leave rate.
            JoinLeaveWaitTime (number): The wait time for thr leave.
            LatencyBins (str): Sets the latency bins statistics
            LatencyBinsEnabled (bool): Enables the latency bins statistics
            LatencyType (str(cutThrough|storeForward)): The type of latency.
            LoadInitialRate (number): The initial rate of the load.
            LoadType (str(binary|step)): The type of the payload setting.
            MapType (str): The POS traffic map type.
            MaxBinaryLoadIntegerValue (number): NOT DEFINED
            MaxIncrementFrameSize (number): The integer that states the maximum amount to which the frame size can be incremented.
            MaxNumGroups (str): NOT DEFINED
            MaxRandomFrameSize (number): The integer that states the maximum random amount to which the frame size can be incremented.
            MinBinaryLoadIntegerValues (number): NOT DEFINED
            MinIncrementFrameSize (number): The integer that states the minimum amount to which the frame size can be incremented.
            MinRandomFrameSize (number): The integer that states the minimum random amount to which the frame size can be incremented.
            MldVersion (number): The version of the MLD messages.
            NumAddresses (number): The integer value for the number of addresses.
            NumIterations (number): The number of iterations.
            Numtrials (number): Defines how many times each frame size will be tested.
            PortDelayEnabled (bool): Enables the Port Delay
            PortDelayUnit (str(bytes|nanoseconds)): Sets the port delay unit in which it will be measured
            PortDelayValue (number): Sets the port delay value
            ProtocolItem (list(str[None|/api/v1/sessions/1/ixnetwork/vport|/api/v1/sessions/1/ixnetwork/vport?deepchild=lan])): Protocol Items
            ReportSequenceError (bool): Reports sequence errors in the test result.
            ReportTputRateUnit (str(gbps|gBps|kbps|kBps|mbps|mBps)): Report identifying the unit for measuring the throughput rate in frames per second.
            RouterAlert (bool): The router alert selected from the Hop-by-hop Options.
            ShowDetailedBinaryResults (bool): NOT DEFINED
            StepFrameLossUnit (str(%|frames)): NOT DEFINED
            StepIncrementFrameSize (number): The step to increment the frame size.
            StepTolerance (number): NOT DEFINED
            SupportedTrafficTypes (str): The traffic types supported.
            TestTrafficType (str): It signifies the test traffic type value.
            TxDelay (number): The delay recorded in the transmit port.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def Apply(self):
        """Executes the apply operation on the server.

        Applies the specified Quick Test.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('apply', payload=payload, response_object=None)

    def ApplyAsync(self):
        """Executes the applyAsync operation on the server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('applyAsync', payload=payload, response_object=None)

    def ApplyAsyncResult(self):
        """Executes the applyAsyncResult operation on the server.

            Returns:
                bool: 

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('applyAsyncResult', payload=payload, response_object=None)

    def ApplyITWizardConfiguration(self):
        """Executes the applyITWizardConfiguration operation on the server.

        Applies the specified Quick Test.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('applyITWizardConfiguration', payload=payload, response_object=None)

    def GenerateReport(self):
        """Executes the generateReport operation on the server.

        Generate a PDF report for the last succesfull test run.

            Returns:
                str: This method is asynchronous and has no return value.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('generateReport', payload=payload, response_object=None)

    def Run(self, *args, **kwargs):
        """Executes the run operation on the server.

        Starts the specified Quick Test and waits for its execution to finish.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        run()list

            Returns:
                list(str): This method is synchronous and returns the result of the test.

        run(InputParameters:string)list
            Args:
                args[0] is InputParameters (str): The input arguments of the test.

            Returns:
                list(str): This method is synchronous and returns the result of the test.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('run', payload=payload, response_object=None)

    def Start(self, *args, **kwargs):
        """Executes the start operation on the server.

        Starts the specified Quick Test.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        start()

        start(InputParameters:string)
            Args:
                args[0] is InputParameters (str): The input arguments of the test.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('start', payload=payload, response_object=None)

    def Stop(self):
        """Executes the stop operation on the server.

        Stops the currently running Quick Test.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('stop', payload=payload, response_object=None)

    def WaitForTest(self):
        """Executes the waitForTest operation on the server.

        Waits for the execution of the specified Quick Test to be completed.

            Returns:
                list(str): This method is synchronous and returns the result of the test.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('waitForTest', payload=payload, response_object=None)
