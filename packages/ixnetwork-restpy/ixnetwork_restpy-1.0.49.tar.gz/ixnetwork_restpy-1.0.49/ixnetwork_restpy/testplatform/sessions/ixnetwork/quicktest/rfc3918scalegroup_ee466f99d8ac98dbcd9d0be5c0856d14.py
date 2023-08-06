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


class Rfc3918scaleGroup(Base):
    """The scale group of rfc3918.
    The Rfc3918scaleGroup class encapsulates a list of rfc3918scaleGroup resources that is be managed by the user.
    A list of resources can be retrieved from the server using the Rfc3918scaleGroup.find() method.
    The list can be managed by the user by using the Rfc3918scaleGroup.add() and Rfc3918scaleGroup.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'rfc3918scaleGroup'

    def __init__(self, parent):
        super(Rfc3918scaleGroup, self).__init__(parent)

    @property
    def LearnFrames(self):
        """An instance of the LearnFrames class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest.learnframes_9273ee0fe7fa7747c811af69d24b7834.LearnFrames)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest.learnframes_9273ee0fe7fa7747c811af69d24b7834 import LearnFrames
        return LearnFrames(self)._select()

    @property
    def PassCriteria(self):
        """An instance of the PassCriteria class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest.passcriteria_3647e223e09fc67be2d2c0816afb8602.PassCriteria)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest.passcriteria_3647e223e09fc67be2d2c0816afb8602 import PassCriteria
        return PassCriteria(self)._select()

    @property
    def Results(self):
        """An instance of the Results class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest.results_036285ce091796d1114de8c9083a61b0.Results)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest.results_036285ce091796d1114de8c9083a61b0 import Results
        return Results(self)._select()

    @property
    def TestConfig(self):
        """An instance of the TestConfig class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest.testconfig_16c0255f3da028f054fef24b7b3c2021.TestConfig)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest.testconfig_16c0255f3da028f054fef24b7b3c2021 import TestConfig
        return TestConfig(self)._select()

    @property
    def ForceApplyQTConfig(self):
        """Apply QT config

        Returns:
            bool
        """
        return self._get_attribute('forceApplyQTConfig')
    @ForceApplyQTConfig.setter
    def ForceApplyQTConfig(self, value):
        self._set_attribute('forceApplyQTConfig', value)

    @property
    def InputParameters(self):
        """Input Parameters

        Returns:
            str
        """
        return self._get_attribute('inputParameters')
    @InputParameters.setter
    def InputParameters(self, value):
        self._set_attribute('inputParameters', value)

    @property
    def Mode(self):
        """Test mode

        Returns:
            str(existingMode|newMode)
        """
        return self._get_attribute('mode')
    @Mode.setter
    def Mode(self, value):
        self._set_attribute('mode', value)

    @property
    def Name(self):
        """Test name

        Returns:
            str
        """
        return self._get_attribute('name')
    @Name.setter
    def Name(self, value):
        self._set_attribute('name', value)

    def update(self, ForceApplyQTConfig=None, InputParameters=None, Mode=None, Name=None):
        """Updates a child instance of rfc3918scaleGroup on the server.

        Args:
            ForceApplyQTConfig (bool): Apply QT config
            InputParameters (str): Input Parameters
            Mode (str(existingMode|newMode)): Test mode
            Name (str): Test name

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def add(self, ForceApplyQTConfig=None, InputParameters=None, Mode=None, Name=None):
        """Adds a new rfc3918scaleGroup node on the server and retrieves it in this instance.

        Args:
            ForceApplyQTConfig (bool): Apply QT config
            InputParameters (str): Input Parameters
            Mode (str(existingMode|newMode)): Test mode
            Name (str): Test name

        Returns:
            self: This instance with all currently retrieved rfc3918scaleGroup data using find and the newly added rfc3918scaleGroup data available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(locals())

    def remove(self):
        """Deletes all the rfc3918scaleGroup data in this instance from server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, ForceApplyQTConfig=None, InputParameters=None, Mode=None, Name=None):
        """Finds and retrieves rfc3918scaleGroup data from the server.

        All named parameters support regex and can be used to selectively retrieve rfc3918scaleGroup data from the server.
        By default the find method takes no parameters and will retrieve all rfc3918scaleGroup data from the server.

        Args:
            ForceApplyQTConfig (bool): Apply QT config
            InputParameters (str): Input Parameters
            Mode (str(existingMode|newMode)): Test mode
            Name (str): Test name

        Returns:
            self: This instance with matching rfc3918scaleGroup data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of rfc3918scaleGroup data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the rfc3918scaleGroup data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

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
