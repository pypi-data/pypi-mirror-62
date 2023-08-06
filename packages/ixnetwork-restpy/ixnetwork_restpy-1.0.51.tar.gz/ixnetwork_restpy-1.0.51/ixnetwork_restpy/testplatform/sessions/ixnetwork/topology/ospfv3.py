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


class Ospfv3(Base):
    """Ospfv3 Interface level Configuration
    The Ospfv3 class encapsulates a list of ospfv3 resources that is be managed by the user.
    A list of resources can be retrieved from the server using the Ospfv3.find() method.
    The list can be managed by the user by using the Ospfv3.add() and Ospfv3.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'ospfv3'

    def __init__(self, parent):
        super(Ospfv3, self).__init__(parent)

    @property
    def Connector(self):
        """An instance of the Connector class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector.Connector)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector import Connector
        return Connector(self)

    @property
    def LearnedInfo(self):
        """An instance of the LearnedInfo class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo.LearnedInfo)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo import LearnedInfo
        return LearnedInfo(self)

    @property
    def Active(self):
        """Activate/Deactivate Configuration

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('active')

    @property
    def AreaId(self):
        """OSPFv3 Area ID for a non-connected interface, displayed in Interger format

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('areaId')

    @property
    def AreaIdIp(self):
        """OSPFv3 Area ID for a non-connected interface, displayed in IP Address format

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('areaIdIp')

    @property
    def AuthAlgo(self):
        """Authentication Algorithms

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('authAlgo')

    @property
    def ConnectedVia(self):
        """DEPRECATED List of layers this layer used to connect to the wire

        Returns:
            list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
        """
        return self._get_attribute('connectedVia')
    @ConnectedVia.setter
    def ConnectedVia(self, value):
        self._set_attribute('connectedVia', value)

    @property
    def Count(self):
        """Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.

        Returns:
            number
        """
        return self._get_attribute('count')

    @property
    def DeadInterval(self):
        """Dead Interval

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('deadInterval')

    @property
    def DemandCircuit(self):
        """Option bit 5

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('demandCircuit')

    @property
    def DescriptiveName(self):
        """Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context

        Returns:
            str
        """
        return self._get_attribute('descriptiveName')

    @property
    def EnableAuthentication(self):
        """Enable Authentication

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('enableAuthentication')

    @property
    def EnableBfdRegistration(self):
        """Enable BFD Registration

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('enableBfdRegistration')

    @property
    def EnableFastHello(self):
        """Enable Fast Hello

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('enableFastHello')

    @property
    def EnableIgnoreDbDescMtu(self):
        """Ignore DB-Desc MTU

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('enableIgnoreDbDescMtu')

    @property
    def Errors(self):
        """A list of errors that have occurred

        Returns:
            list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
        """
        return self._get_attribute('errors')

    @property
    def ExternalCapability(self):
        """Option bit 1

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('externalCapability')

    @property
    def HelloInterval(self):
        """Hello Interval

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('helloInterval')

    @property
    def HelloMultiplier(self):
        """Hello Multiplier

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('helloMultiplier')

    @property
    def InstanceId(self):
        """Instance ID

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('instanceId')

    @property
    def Key(self):
        """Key

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('key')

    @property
    def LinkMetric(self):
        """Link Metric

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('linkMetric')

    @property
    def LocalRouterID(self):
        """Router ID

        Returns:
            list(str)
        """
        return self._get_attribute('localRouterID')

    @property
    def Multiplier(self):
        """Number of layer instances per parent instance (multiplier)

        Returns:
            number
        """
        return self._get_attribute('multiplier')
    @Multiplier.setter
    def Multiplier(self, value):
        self._set_attribute('multiplier', value)

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
    def NetworkType(self):
        """Network Type

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('networkType')

    @property
    def NssaCapability(self):
        """Option bit 3

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('nssaCapability')

    @property
    def Ospfv3IfaceState(self):
        """Logs additional information about the Interface State

        Returns:
            list(str[backup|down|dr|drOther|pointToPoint|unrecognized|waiting])
        """
        return self._get_attribute('ospfv3IfaceState')

    @property
    def Ospfv3NeighborState(self):
        """Logs additional information about the Neighbor State

        Returns:
            list(str[attempt|down|exchange|exStart|full|init|loading|multiNeighbor|none|twoWay])
        """
        return self._get_attribute('ospfv3NeighborState')

    @property
    def Priority(self):
        """Priority (when DR/BDR)

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('priority')

    @property
    def Router(self):
        """Option bit 4

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('router')

    @property
    def SaId(self):
        """Security Association ID

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('saId')

    @property
    def SessionInfo(self):
        """Logs additional information about the session state

        Returns:
            list(str[ifaceSessInfoAllNbrIn2Way|ifaceSessInfoAllNbrInattempt|ifaceSessInfoAllNbrInDown|ifaceSessInfoAllNbrInExchange|ifaceSessInfoAllNbrInExStart|ifaceSessInfoAllNbrInInit|ifaceSessInfoAllNbrInLoading|ifaceSessInfoFsmNotStarted|ifaceSessInfoSameNbrId|iPAddressNotRcvd|none])
        """
        return self._get_attribute('sessionInfo')

    @property
    def SessionStatus(self):
        """Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

        Returns:
            list(str[down|notStarted|up])
        """
        return self._get_attribute('sessionStatus')

    @property
    def StackedLayers(self):
        """List of secondary (many to one) child layer protocols

        Returns:
            list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
        """
        return self._get_attribute('stackedLayers')
    @StackedLayers.setter
    def StackedLayers(self, value):
        self._set_attribute('stackedLayers', value)

    @property
    def StateCounts(self):
        """A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up

        Returns:
            dict(total:number,notStarted:number,down:number,up:number)
        """
        return self._get_attribute('stateCounts')

    @property
    def Status(self):
        """Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

        Returns:
            str(configured|error|mixed|notStarted|started|starting|stopping)
        """
        return self._get_attribute('status')

    @property
    def TypeAreaId(self):
        """Area ID Type

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('typeAreaId')

    @property
    def V6(self):
        """Option bit 0

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('v6')

    def update(self, ConnectedVia=None, Multiplier=None, Name=None, StackedLayers=None):
        """Updates a child instance of ospfv3 on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args:
            ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
            Multiplier (number): Number of layer instances per parent instance (multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario
            StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def add(self, ConnectedVia=None, Multiplier=None, Name=None, StackedLayers=None):
        """Adds a new ospfv3 node on the server and retrieves it in this instance.

        Args:
            ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
            Multiplier (number): Number of layer instances per parent instance (multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario
            StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

        Returns:
            self: This instance with all currently retrieved ospfv3 data using find and the newly added ospfv3 data available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(locals())

    def remove(self):
        """Deletes all the ospfv3 data in this instance from server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, ConnectedVia=None, Count=None, DescriptiveName=None, Errors=None, LocalRouterID=None, Multiplier=None, Name=None, Ospfv3IfaceState=None, Ospfv3NeighborState=None, SessionInfo=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None):
        """Finds and retrieves ospfv3 data from the server.

        All named parameters support regex and can be used to selectively retrieve ospfv3 data from the server.
        By default the find method takes no parameters and will retrieve all ospfv3 data from the server.

        Args:
            ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
            Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
            DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
            Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
            LocalRouterID (list(str)): Router ID
            Multiplier (number): Number of layer instances per parent instance (multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario
            Ospfv3IfaceState (list(str[backup|down|dr|drOther|pointToPoint|unrecognized|waiting])): Logs additional information about the Interface State
            Ospfv3NeighborState (list(str[attempt|down|exchange|exStart|full|init|loading|multiNeighbor|none|twoWay])): Logs additional information about the Neighbor State
            SessionInfo (list(str[ifaceSessInfoAllNbrIn2Way|ifaceSessInfoAllNbrInattempt|ifaceSessInfoAllNbrInDown|ifaceSessInfoAllNbrInExchange|ifaceSessInfoAllNbrInExStart|ifaceSessInfoAllNbrInInit|ifaceSessInfoAllNbrInLoading|ifaceSessInfoFsmNotStarted|ifaceSessInfoSameNbrId|iPAddressNotRcvd|none])): Logs additional information about the session state
            SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
            StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
            StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
            Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

        Returns:
            self: This instance with matching ospfv3 data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of ospfv3 data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the ospfv3 data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def get_device_ids(self, PortNames=None, Active=None, AreaId=None, AreaIdIp=None, AuthAlgo=None, DeadInterval=None, DemandCircuit=None, EnableAuthentication=None, EnableBfdRegistration=None, EnableFastHello=None, EnableIgnoreDbDescMtu=None, ExternalCapability=None, HelloInterval=None, HelloMultiplier=None, InstanceId=None, Key=None, LinkMetric=None, NetworkType=None, NssaCapability=None, Priority=None, Router=None, SaId=None, TypeAreaId=None, V6=None):
        """Base class infrastructure that gets a list of ospfv3 device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args:
            PortNames (str): optional regex of port names
            Active (str): optional regex of active
            AreaId (str): optional regex of areaId
            AreaIdIp (str): optional regex of areaIdIp
            AuthAlgo (str): optional regex of authAlgo
            DeadInterval (str): optional regex of deadInterval
            DemandCircuit (str): optional regex of demandCircuit
            EnableAuthentication (str): optional regex of enableAuthentication
            EnableBfdRegistration (str): optional regex of enableBfdRegistration
            EnableFastHello (str): optional regex of enableFastHello
            EnableIgnoreDbDescMtu (str): optional regex of enableIgnoreDbDescMtu
            ExternalCapability (str): optional regex of externalCapability
            HelloInterval (str): optional regex of helloInterval
            HelloMultiplier (str): optional regex of helloMultiplier
            InstanceId (str): optional regex of instanceId
            Key (str): optional regex of key
            LinkMetric (str): optional regex of linkMetric
            NetworkType (str): optional regex of networkType
            NssaCapability (str): optional regex of nssaCapability
            Priority (str): optional regex of priority
            Router (str): optional regex of router
            SaId (str): optional regex of saId
            TypeAreaId (str): optional regex of typeAreaId
            V6 (str): optional regex of v6

        Returns:
            list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())

    def ClearAllLearnedInfo(self, *args, **kwargs):
        """Executes the clearAllLearnedInfo operation on the server.

        Clear All Learned Info

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        clearAllLearnedInfo()

        clearAllLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        clearAllLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('clearAllLearnedInfo', payload=payload, response_object=None)

    def ClearAllLearnedInfoInClient(self, *args, **kwargs):
        """Executes the clearAllLearnedInfoInClient operation on the server.

        Clears ALL routes from GUI grid for the selected OSPFv3 router.

        clearAllLearnedInfoInClient(Arg2:list)list
            Args:
                args[0] is Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

            Returns:
                list(str): ID to associate each async action invocation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('clearAllLearnedInfoInClient', payload=payload, response_object=None)

    def GetBasicLearnedInfo(self, *args, **kwargs):
        """Executes the getBasicLearnedInfo operation on the server.

        Get Basic Learned Info

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getBasicLearnedInfo()

        getBasicLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getBasicLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getBasicLearnedInfo(Arg2:list)list
            Args:
                args[0] is Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

            Returns:
                list(str): ID to associate each async action invocation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getBasicLearnedInfo', payload=payload, response_object=None)

    def GetDetailedLearnedInfo(self, *args, **kwargs):
        """Executes the getDetailedLearnedInfo operation on the server.

        Get Detailed Learned Info

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getDetailedLearnedInfo()

        getDetailedLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getDetailedLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getDetailedLearnedInfo(Arg2:list)list
            Args:
                args[0] is Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

            Returns:
                list(str): ID to associate each async action invocation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getDetailedLearnedInfo', payload=payload, response_object=None)

    def RestartDown(self, *args, **kwargs):
        """Executes the restartDown operation on the server.

        Stop and start interfaces and sessions that are in Down state.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        restartDown()

        restartDown(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        restartDown(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('restartDown', payload=payload, response_object=None)

    def ResumeHello(self, *args, **kwargs):
        """Executes the resumeHello operation on the server.

        Resume sending OSPFv3 Hellos

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        resumeHello()

        resumeHello(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        resumeHello(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('resumeHello', payload=payload, response_object=None)

    def Resumehello(self, *args, **kwargs):
        """Executes the resumehello operation on the server.

        Starts the protocol state machine for the given protocol session instances.

        resumehello(Arg2:list)list
            Args:
                args[0] is Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

            Returns:
                list(str): ID to associate each async action invocation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('resumehello', payload=payload, response_object=None)

    def Start(self, *args, **kwargs):
        """Executes the start operation on the server.

        Start OSPFv3 Interface

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        start()

        start(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        start(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('start', payload=payload, response_object=None)

    def Stop(self, *args, **kwargs):
        """Executes the stop operation on the server.

        Stop OSPF Interface

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        stop()

        stop(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        stop(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('stop', payload=payload, response_object=None)

    def StopHello(self, *args, **kwargs):
        """Executes the stopHello operation on the server.

        Stop sending OSPFv3 Hellos

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        stopHello()

        stopHello(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        stopHello(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('stopHello', payload=payload, response_object=None)

    def Stophello(self, *args, **kwargs):
        """Executes the stophello operation on the server.

        Stops the protocol state machine for the given protocol session instances.

        stophello(Arg2:list)list
            Args:
                args[0] is Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

            Returns:
                list(str): ID to associate each async action invocation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('stophello', payload=payload, response_object=None)
