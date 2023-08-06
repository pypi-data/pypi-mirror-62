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
    """Test configuration
    The TestConfig class encapsulates a required testConfig resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'testConfig'

    def __init__(self, parent):
        super(TestConfig, self).__init__(parent)

    @property
    def CorrectionFactorMode(self):
        """Correction Factor mode

        Returns:
            str
        """
        return self._get_attribute('correctionFactorMode')
    @CorrectionFactorMode.setter
    def CorrectionFactorMode(self, value):
        self._set_attribute('correctionFactorMode', value)

    @property
    def CorrectionFactorScale(self):
        """Correction Factor Scale

        Returns:
            str
        """
        return self._get_attribute('correctionFactorScale')
    @CorrectionFactorScale.setter
    def CorrectionFactorScale(self, value):
        self._set_attribute('correctionFactorScale', value)

    @property
    def Duration(self):
        """The wait time in hours, minutes, and seconds, that is required for the PTP protocol to negotiate

        Returns:
            number
        """
        return self._get_attribute('duration')
    @Duration.setter
    def Duration(self, value):
        self._set_attribute('duration', value)

    @property
    def EnableCorrectionFactorPassFail(self):
        """If selected, a Pass/Fail criteria is applied to the Correction Factor Error test

        Returns:
            str
        """
        return self._get_attribute('enableCorrectionFactorPassFail')
    @EnableCorrectionFactorPassFail.setter
    def EnableCorrectionFactorPassFail(self, value):
        self._set_attribute('enableCorrectionFactorPassFail', value)

    @property
    def MaxOutstanding(self):
        """Maximum number of connection requests or tear down requests that can be pending at any one time

        Returns:
            number
        """
        return self._get_attribute('maxOutstanding')
    @MaxOutstanding.setter
    def MaxOutstanding(self, value):
        self._set_attribute('maxOutstanding', value)

    @property
    def MeasuredResidenceTime(self):
        """The measured time taken by a packet to move from the ingress port to the egress port

        Returns:
            str
        """
        return self._get_attribute('measuredResidenceTime')
    @MeasuredResidenceTime.setter
    def MeasuredResidenceTime(self, value):
        self._set_attribute('measuredResidenceTime', value)

    @property
    def NumberCorrectionFactorPassFail(self):
        """Number of criteria used for Pass/Fail

        Returns:
            number
        """
        return self._get_attribute('numberCorrectionFactorPassFail')
    @NumberCorrectionFactorPassFail.setter
    def NumberCorrectionFactorPassFail(self, value):
        self._set_attribute('numberCorrectionFactorPassFail', value)

    @property
    def Numtrials(self):
        """The number of trials that can be run

        Returns:
            number
        """
        return self._get_attribute('numtrials')
    @Numtrials.setter
    def Numtrials(self, value):
        self._set_attribute('numtrials', value)

    @property
    def OffsetGraph(self):
        """Offset graphing

        Returns:
            str
        """
        return self._get_attribute('offsetGraph')
    @OffsetGraph.setter
    def OffsetGraph(self, value):
        self._set_attribute('offsetGraph', value)

    @property
    def PathDelayGraphing(self):
        """Graphing of path delay

        Returns:
            str
        """
        return self._get_attribute('pathDelayGraphing')
    @PathDelayGraphing.setter
    def PathDelayGraphing(self, value):
        self._set_attribute('pathDelayGraphing', value)

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
    def ResidenceTime(self):
        """The time taken by a packet to move from the ingress port to the egress port

        Returns:
            number
        """
        return self._get_attribute('residenceTime')
    @ResidenceTime.setter
    def ResidenceTime(self, value):
        self._set_attribute('residenceTime', value)

    @property
    def Runmode(self):
        """Running mode used

        Returns:
            str(duration|noframes)
        """
        return self._get_attribute('runmode')
    @Runmode.setter
    def Runmode(self, value):
        self._set_attribute('runmode', value)

    @property
    def SetupRate(self):
        """The number of PTP connections to be initiated per second

        Returns:
            number
        """
        return self._get_attribute('setupRate')
    @SetupRate.setter
    def SetupRate(self, value):
        self._set_attribute('setupRate', value)

    @property
    def StartTraffic(self):
        """All traffic configured in IxNetwork is initiated on running this test

        Returns:
            str
        """
        return self._get_attribute('startTraffic')
    @StartTraffic.setter
    def StartTraffic(self, value):
        self._set_attribute('startTraffic', value)

    @property
    def TeardownRate(self):
        """The number of PTP connections to tear down per second

        Returns:
            number
        """
        return self._get_attribute('teardownRate')
    @TeardownRate.setter
    def TeardownRate(self, value):
        self._set_attribute('teardownRate', value)

    @property
    def TestConfiguration(self):
        """Test configuration

        Returns:
            str
        """
        return self._get_attribute('testConfiguration')
    @TestConfiguration.setter
    def TestConfiguration(self, value):
        self._set_attribute('testConfiguration', value)

    @property
    def UseExistingSetupRate(self):
        """The current setup rate value is used

        Returns:
            bool
        """
        return self._get_attribute('useExistingSetupRate')
    @UseExistingSetupRate.setter
    def UseExistingSetupRate(self, value):
        self._set_attribute('useExistingSetupRate', value)

    def update(self, CorrectionFactorMode=None, CorrectionFactorScale=None, Duration=None, EnableCorrectionFactorPassFail=None, MaxOutstanding=None, MeasuredResidenceTime=None, NumberCorrectionFactorPassFail=None, Numtrials=None, OffsetGraph=None, PathDelayGraphing=None, ProtocolItem=None, ResidenceTime=None, Runmode=None, SetupRate=None, StartTraffic=None, TeardownRate=None, TestConfiguration=None, UseExistingSetupRate=None):
        """Updates a child instance of testConfig on the server.

        Args:
            CorrectionFactorMode (str): Correction Factor mode
            CorrectionFactorScale (str): Correction Factor Scale
            Duration (number): The wait time in hours, minutes, and seconds, that is required for the PTP protocol to negotiate
            EnableCorrectionFactorPassFail (str): If selected, a Pass/Fail criteria is applied to the Correction Factor Error test
            MaxOutstanding (number): Maximum number of connection requests or tear down requests that can be pending at any one time
            MeasuredResidenceTime (str): The measured time taken by a packet to move from the ingress port to the egress port
            NumberCorrectionFactorPassFail (number): Number of criteria used for Pass/Fail
            Numtrials (number): The number of trials that can be run
            OffsetGraph (str): Offset graphing
            PathDelayGraphing (str): Graphing of path delay
            ProtocolItem (list(str[None|/api/v1/sessions/1/ixnetwork/vport|/api/v1/sessions/1/ixnetwork/vport?deepchild=lan])): Protocol Items
            ResidenceTime (number): The time taken by a packet to move from the ingress port to the egress port
            Runmode (str(duration|noframes)): Running mode used
            SetupRate (number): The number of PTP connections to be initiated per second
            StartTraffic (str): All traffic configured in IxNetwork is initiated on running this test
            TeardownRate (number): The number of PTP connections to tear down per second
            TestConfiguration (str): Test configuration
            UseExistingSetupRate (bool): The current setup rate value is used

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
