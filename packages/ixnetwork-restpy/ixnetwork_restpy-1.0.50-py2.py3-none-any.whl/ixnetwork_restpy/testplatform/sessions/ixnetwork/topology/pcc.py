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


class Pcc(Base):
    """Pcep Session (Device) level Configuration
    The Pcc class encapsulates a list of pcc resources that is be managed by the user.
    A list of resources can be retrieved from the server using the Pcc.find() method.
    The list can be managed by the user by using the Pcc.add() and Pcc.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'pcc'

    def __init__(self, parent):
        super(Pcc, self).__init__(parent)

    @property
    def ExpectedInitiatedLspList(self):
        """An instance of the ExpectedInitiatedLspList class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.expectedinitiatedlsplist.ExpectedInitiatedLspList)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.expectedinitiatedlsplist import ExpectedInitiatedLspList
        return ExpectedInitiatedLspList(self)._select()

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
    def PccLearnedLspDb(self):
        """An instance of the PccLearnedLspDb class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcclearnedlspdb.PccLearnedLspDb)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcclearnedlspdb import PccLearnedLspDb
        return PccLearnedLspDb(self)._select()

    @property
    def PcepBackupPCEs(self):
        """An instance of the PcepBackupPCEs class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepbackuppces.PcepBackupPCEs)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepbackuppces import PcepBackupPCEs
        return PcepBackupPCEs(self)._select()

    @property
    def PreEstablishedSrLsps(self):
        """An instance of the PreEstablishedSrLsps class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.preestablishedsrlsps.PreEstablishedSrLsps)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.preestablishedsrlsps import PreEstablishedSrLsps
        return PreEstablishedSrLsps(self)._select()

    @property
    def RequestedLsps(self):
        """An instance of the RequestedLsps class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.requestedlsps.RequestedLsps)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.requestedlsps import RequestedLsps
        return RequestedLsps(self)._select()

    @property
    def Active(self):
        """Activate/Deactivate Configuration

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('active')

    @property
    def Active_pre_established_lsps(self):
        """

        Returns:
            number
        """
        return self._get_attribute('active_pre_established_lsps')
    @Active_pre_established_lsps.setter
    def Active_pre_established_lsps(self, value):
        self._set_attribute('active_pre_established_lsps', value)

    @property
    def Authentication(self):
        """The type of cryptographic authentication to be used on this link interface

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('authentication')

    @property
    def BurstInterval(self):
        """Interval in milisecond in which desired rate of messages needs to be maintained.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('burstInterval')

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
        """This is the time interval, after the expiration of which, a PCEP peer declares the session down if no PCEP message has been received.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('deadInterval')

    @property
    def DescriptiveName(self):
        """Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context

        Returns:
            str
        """
        return self._get_attribute('descriptiveName')

    @property
    def ErrorValue(self):
        """To configure the type of error. Editable only if Return Instantiation Error is enabled.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('errorValue')

    @property
    def Errors(self):
        """A list of errors that have occurred

        Returns:
            list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
        """
        return self._get_attribute('errors')

    @property
    def ExpectedInitiatedLspsForTraffic(self):
        """Based on the value in this control the number of Expected Initiated LSPs for Traffic can be configured. This is used for traffic only.

        Returns:
            number
        """
        return self._get_attribute('expectedInitiatedLspsForTraffic')
    @ExpectedInitiatedLspsForTraffic.setter
    def ExpectedInitiatedLspsForTraffic(self, value):
        self._set_attribute('expectedInitiatedLspsForTraffic', value)

    @property
    def KeepaliveInterval(self):
        """Frequency/Time Interval of sending PCEP messages to keep the session active.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('keepaliveInterval')

    @property
    def LspInstantiationCapability(self):
        """If Stateful PCE Capability is enabled then this control should be activated to set the LSP Instantiation capability in the Stateful PCE Capability TLV.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('lspInstantiationCapability')

    @property
    def LspUpdateCapability(self):
        """If Stateful PCE Capability is enabled then this control should be activated to set the update capability in the Stateful PCE Capability TLV.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('lspUpdateCapability')

    @property
    def MD5Key(self):
        """A value to be used as the secret MD5 Key.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('mD5Key')

    @property
    def MaxLspPerPcReq(self):
        """Max LSPs Per PCReq

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('maxLspPerPcReq')

    @property
    def MaxLspsPerPcRpt(self):
        """Controls the maximum LSP information that can be present in a Path report message when the session is stateful session.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('maxLspsPerPcRpt')

    @property
    def MaxReconnectInterval(self):
        """This is the maximum time interval, by which recoonect timer will be increased upto.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('maxReconnectInterval')

    @property
    def MaxRequestedLspPerInterval(self):
        """Maximum number of LSP computation request messages can be sent per interval.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('maxRequestedLspPerInterval')

    @property
    def MaxSyncLspPerInterval(self):
        """Maximum number of LSP sync can be sent per interval.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('maxSyncLspPerInterval')

    @property
    def MaximumSidDepth(self):
        """Maximum SID Depth field (MSD) specifies the maximum number of SIDs that a PCC is capable of imposing on a packet. Editable only if SR PCE Capability is enabled.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('maximumSidDepth')

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
    def NumberOfBackupPCEs(self):
        """Number of Backup PCEs

        Returns:
            number
        """
        return self._get_attribute('numberOfBackupPCEs')
    @NumberOfBackupPCEs.setter
    def NumberOfBackupPCEs(self, value):
        self._set_attribute('numberOfBackupPCEs', value)

    @property
    def PccPpagTLVType(self):
        """PPAG TLV Type specifies PCC's capability of interpreting this type of PPAG TLV

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('pccPpagTLVType')

    @property
    def PceIpv4Address(self):
        """IPv4 address of the PCE. This column is greyed out in case of PCCv6.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('pceIpv4Address')

    @property
    def PreEstablishedSrLspsPerPcc(self):
        """Pre-Established SR LSPs per PCC

        Returns:
            number
        """
        return self._get_attribute('preEstablishedSrLspsPerPcc')
    @PreEstablishedSrLspsPerPcc.setter
    def PreEstablishedSrLspsPerPcc(self, value):
        self._set_attribute('preEstablishedSrLspsPerPcc', value)

    @property
    def RateControl(self):
        """The rate control is an optional feature associated with PCE initiated LSP.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('rateControl')

    @property
    def ReconnectInterval(self):
        """This is the time interval, after the expiration of which, retry to establish the broken session by PCC happen.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('reconnectInterval')

    @property
    def RequestedLspsPerPcc(self):
        """Requested LSPs per PCC

        Returns:
            number
        """
        return self._get_attribute('requestedLspsPerPcc')
    @RequestedLspsPerPcc.setter
    def RequestedLspsPerPcc(self, value):
        self._set_attribute('requestedLspsPerPcc', value)

    @property
    def ReturnInstantiationError(self):
        """If enabled, then PCC will reply PCErr upon receiving PCInitiate message.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('returnInstantiationError')

    @property
    def SessionStatus(self):
        """Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

        Returns:
            list(str[down|notStarted|up])
        """
        return self._get_attribute('sessionStatus')

    @property
    def SrPceCapability(self):
        """The SR PCE Capability TLV is an optional TLV associated with the OPEN Object to exchange SR capability of PCEP speakers.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('srPceCapability')

    @property
    def Srv6MaxSL(self):
        """This field specifies the maximum value of the Segments Left (SL) in the SRH.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('srv6MaxSL')

    @property
    def Srv6PceCapability(self):
        """The SRv6 PCE Capability TLV is a sub-TLV that comes under PATH-SETUP-TYPE-CAPABILITY TLV if PST List contains SRv6 PST type. This TLV is associated with the OPEN Object to exchange SRv6 capability of PCEP speakers.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('srv6PceCapability')

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
    def StateTimeoutInterval(self):
        """This is the time interval, after the expiration of which, LSP is cleaned up by PCC.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('stateTimeoutInterval')

    @property
    def Status(self):
        """Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

        Returns:
            str(configured|error|mixed|notStarted|started|starting|stopping)
        """
        return self._get_attribute('status')

    @property
    def TcpPort(self):
        """PCEP operates over TCP using a registered TCP port (default - 4189). This allows the requirements of reliable messaging and flow control to bemet without further protocol work. This control can be configured when user does not want to use the default one.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('tcpPort')

    def update(self, Active_pre_established_lsps=None, ConnectedVia=None, ExpectedInitiatedLspsForTraffic=None, Multiplier=None, Name=None, NumberOfBackupPCEs=None, PreEstablishedSrLspsPerPcc=None, RequestedLspsPerPcc=None, StackedLayers=None):
        """Updates a child instance of pcc on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args:
            Active_pre_established_lsps (number): 
            ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
            ExpectedInitiatedLspsForTraffic (number): Based on the value in this control the number of Expected Initiated LSPs for Traffic can be configured. This is used for traffic only.
            Multiplier (number): Number of layer instances per parent instance (multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario
            NumberOfBackupPCEs (number): Number of Backup PCEs
            PreEstablishedSrLspsPerPcc (number): Pre-Established SR LSPs per PCC
            RequestedLspsPerPcc (number): Requested LSPs per PCC
            StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def add(self, Active_pre_established_lsps=None, ConnectedVia=None, ExpectedInitiatedLspsForTraffic=None, Multiplier=None, Name=None, NumberOfBackupPCEs=None, PreEstablishedSrLspsPerPcc=None, RequestedLspsPerPcc=None, StackedLayers=None):
        """Adds a new pcc node on the server and retrieves it in this instance.

        Args:
            Active_pre_established_lsps (number): 
            ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
            ExpectedInitiatedLspsForTraffic (number): Based on the value in this control the number of Expected Initiated LSPs for Traffic can be configured. This is used for traffic only.
            Multiplier (number): Number of layer instances per parent instance (multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario
            NumberOfBackupPCEs (number): Number of Backup PCEs
            PreEstablishedSrLspsPerPcc (number): Pre-Established SR LSPs per PCC
            RequestedLspsPerPcc (number): Requested LSPs per PCC
            StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

        Returns:
            self: This instance with all currently retrieved pcc data using find and the newly added pcc data available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(locals())

    def remove(self):
        """Deletes all the pcc data in this instance from server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, Active_pre_established_lsps=None, ConnectedVia=None, Count=None, DescriptiveName=None, Errors=None, ExpectedInitiatedLspsForTraffic=None, Multiplier=None, Name=None, NumberOfBackupPCEs=None, PreEstablishedSrLspsPerPcc=None, RequestedLspsPerPcc=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None):
        """Finds and retrieves pcc data from the server.

        All named parameters support regex and can be used to selectively retrieve pcc data from the server.
        By default the find method takes no parameters and will retrieve all pcc data from the server.

        Args:
            Active_pre_established_lsps (number): 
            ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
            Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
            DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
            Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
            ExpectedInitiatedLspsForTraffic (number): Based on the value in this control the number of Expected Initiated LSPs for Traffic can be configured. This is used for traffic only.
            Multiplier (number): Number of layer instances per parent instance (multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario
            NumberOfBackupPCEs (number): Number of Backup PCEs
            PreEstablishedSrLspsPerPcc (number): Pre-Established SR LSPs per PCC
            RequestedLspsPerPcc (number): Requested LSPs per PCC
            SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
            StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
            StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
            Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

        Returns:
            self: This instance with matching pcc data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of pcc data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the pcc data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def get_device_ids(self, PortNames=None, Active=None, Authentication=None, BurstInterval=None, DeadInterval=None, ErrorValue=None, KeepaliveInterval=None, LspInstantiationCapability=None, LspUpdateCapability=None, MD5Key=None, MaxLspPerPcReq=None, MaxLspsPerPcRpt=None, MaxReconnectInterval=None, MaxRequestedLspPerInterval=None, MaxSyncLspPerInterval=None, MaximumSidDepth=None, PccPpagTLVType=None, PceIpv4Address=None, RateControl=None, ReconnectInterval=None, ReturnInstantiationError=None, SrPceCapability=None, Srv6MaxSL=None, Srv6PceCapability=None, StateTimeoutInterval=None, TcpPort=None):
        """Base class infrastructure that gets a list of pcc device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args:
            PortNames (str): optional regex of port names
            Active (str): optional regex of active
            Authentication (str): optional regex of authentication
            BurstInterval (str): optional regex of burstInterval
            DeadInterval (str): optional regex of deadInterval
            ErrorValue (str): optional regex of errorValue
            KeepaliveInterval (str): optional regex of keepaliveInterval
            LspInstantiationCapability (str): optional regex of lspInstantiationCapability
            LspUpdateCapability (str): optional regex of lspUpdateCapability
            MD5Key (str): optional regex of mD5Key
            MaxLspPerPcReq (str): optional regex of maxLspPerPcReq
            MaxLspsPerPcRpt (str): optional regex of maxLspsPerPcRpt
            MaxReconnectInterval (str): optional regex of maxReconnectInterval
            MaxRequestedLspPerInterval (str): optional regex of maxRequestedLspPerInterval
            MaxSyncLspPerInterval (str): optional regex of maxSyncLspPerInterval
            MaximumSidDepth (str): optional regex of maximumSidDepth
            PccPpagTLVType (str): optional regex of pccPpagTLVType
            PceIpv4Address (str): optional regex of pceIpv4Address
            RateControl (str): optional regex of rateControl
            ReconnectInterval (str): optional regex of reconnectInterval
            ReturnInstantiationError (str): optional regex of returnInstantiationError
            SrPceCapability (str): optional regex of srPceCapability
            Srv6MaxSL (str): optional regex of srv6MaxSL
            Srv6PceCapability (str): optional regex of srv6PceCapability
            StateTimeoutInterval (str): optional regex of stateTimeoutInterval
            TcpPort (str): optional regex of tcpPort

        Returns:
            list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())

    def ClearPccLearnedInfoInClient(self, *args, **kwargs):
        """Executes the clearPccLearnedInfoInClient operation on the server.

        Clears ALL Learned LSP Information of PCC Device.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        clearPccLearnedInfoInClient()

        clearPccLearnedInfoInClient(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        clearPccLearnedInfoInClient(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        clearPccLearnedInfoInClient(Arg2:list)list
            Args:
                args[0] is Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

            Returns:
                list(str): ID to associate each async action invocation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('clearPccLearnedInfoInClient', payload=payload, response_object=None)

    def GetPccBasicAllSrLspLearnedInfo(self, *args, **kwargs):
        """Executes the getPccBasicAllSrLspLearnedInfo operation on the server.

        Gets Basic Information about All SR LSPs learnt by this PCC.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getPccBasicAllSrLspLearnedInfo()

        getPccBasicAllSrLspLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getPccBasicAllSrLspLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getPccBasicAllSrLspLearnedInfo(Arg2:list)list
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
        return self._execute('getPccBasicAllSrLspLearnedInfo', payload=payload, response_object=None)

    def GetPccBasicAllSrv6LspLearnedInfo(self, *args, **kwargs):
        """Executes the getPccBasicAllSrv6LspLearnedInfo operation on the server.

        Gets Basic Information about All SRv6 LSPs learnt by this PCC.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getPccBasicAllSrv6LspLearnedInfo()

        getPccBasicAllSrv6LspLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getPccBasicAllSrv6LspLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getPccBasicAllSrv6LspLearnedInfo(Arg2:list)list
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
        return self._execute('getPccBasicAllSrv6LspLearnedInfo', payload=payload, response_object=None)

    def GetPccBasicSrPccRequestedLspLearnedInfo(self, *args, **kwargs):
        """Executes the getPccBasicSrPccRequestedLspLearnedInfo operation on the server.

        Gets Basic Information about SR-TE PCC Requested LSPs learnt by this PCC.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getPccBasicSrPccRequestedLspLearnedInfo()

        getPccBasicSrPccRequestedLspLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getPccBasicSrPccRequestedLspLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getPccBasicSrPccRequestedLspLearnedInfo(Arg2:list)list
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
        return self._execute('getPccBasicSrPccRequestedLspLearnedInfo', payload=payload, response_object=None)

    def GetPccBasicSrPccSyncOrReportLspLearnedInfo(self, *args, **kwargs):
        """Executes the getPccBasicSrPccSyncOrReportLspLearnedInfo operation on the server.

        Gets Basic Information about SR-TE PCC Sync/Report LSPs learnt by this PCC.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getPccBasicSrPccSyncOrReportLspLearnedInfo()

        getPccBasicSrPccSyncOrReportLspLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getPccBasicSrPccSyncOrReportLspLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getPccBasicSrPccSyncOrReportLspLearnedInfo(Arg2:list)list
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
        return self._execute('getPccBasicSrPccSyncOrReportLspLearnedInfo', payload=payload, response_object=None)

    def GetPccBasicSrPceInitiatedLspLearnedInfo(self, *args, **kwargs):
        """Executes the getPccBasicSrPceInitiatedLspLearnedInfo operation on the server.

        Gets Basic Information about SR-TE PCE Initiated LSPs learnt by this PCC.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getPccBasicSrPceInitiatedLspLearnedInfo()

        getPccBasicSrPceInitiatedLspLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getPccBasicSrPceInitiatedLspLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getPccBasicSrPceInitiatedLspLearnedInfo(Arg2:list)list
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
        return self._execute('getPccBasicSrPceInitiatedLspLearnedInfo', payload=payload, response_object=None)

    def GetPccBasicSrv6PccRequestedLspLearnedInfo(self, *args, **kwargs):
        """Executes the getPccBasicSrv6PccRequestedLspLearnedInfo operation on the server.

        Gets Basic Information about SRv6 PCC Requested LSPs learnt by this PCC.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getPccBasicSrv6PccRequestedLspLearnedInfo()

        getPccBasicSrv6PccRequestedLspLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getPccBasicSrv6PccRequestedLspLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getPccBasicSrv6PccRequestedLspLearnedInfo(Arg2:list)list
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
        return self._execute('getPccBasicSrv6PccRequestedLspLearnedInfo', payload=payload, response_object=None)

    def GetPccBasicSrv6PccSyncOrReportLspLearnedInfo(self, *args, **kwargs):
        """Executes the getPccBasicSrv6PccSyncOrReportLspLearnedInfo operation on the server.

        Gets Basic Information about SRv6 PCC Sync/Report LSPs learnt by this PCC.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getPccBasicSrv6PccSyncOrReportLspLearnedInfo()

        getPccBasicSrv6PccSyncOrReportLspLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getPccBasicSrv6PccSyncOrReportLspLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getPccBasicSrv6PccSyncOrReportLspLearnedInfo(Arg2:list)list
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
        return self._execute('getPccBasicSrv6PccSyncOrReportLspLearnedInfo', payload=payload, response_object=None)

    def GetPccBasicSrv6PceInitiatedLspLearnedInfo(self, *args, **kwargs):
        """Executes the getPccBasicSrv6PceInitiatedLspLearnedInfo operation on the server.

        Gets Basic Information about SRv6 PCE Initiated LSPs learnt by this PCC.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getPccBasicSrv6PceInitiatedLspLearnedInfo()

        getPccBasicSrv6PceInitiatedLspLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getPccBasicSrv6PceInitiatedLspLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getPccBasicSrv6PceInitiatedLspLearnedInfo(Arg2:list)list
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
        return self._execute('getPccBasicSrv6PceInitiatedLspLearnedInfo', payload=payload, response_object=None)

    def GetPccLearnedInfo(self, *args, **kwargs):
        """Executes the getPccLearnedInfo operation on the server.

        Gets Detailed Information about All SR LSPs learnt by this PCC.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getPccLearnedInfo()

        getPccLearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getPccLearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getPccLearnedInfo(Arg2:list)list
            Args:
                args[0] is Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

            Returns:
                list(str): ID to associate each async action invocation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('getPccLearnedInfo', payload=payload, response_object=None)

    def GetPccSrv6LearnedInfo(self, *args, **kwargs):
        """Executes the getPccSrv6LearnedInfo operation on the server.

        Gets Detailed Information about All SRv6 LSPs learnt by this PCC.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        getPccSrv6LearnedInfo()

        getPccSrv6LearnedInfo(SessionIndices:list)
            Args:
                args[0] is SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        getPccSrv6LearnedInfo(SessionIndices:string)
            Args:
                args[0] is SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        getPccSrv6LearnedInfo(Arg2:list)list
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
        return self._execute('getPccSrv6LearnedInfo', payload=payload, response_object=None)

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

    def Start(self, *args, **kwargs):
        """Executes the start operation on the server.

        Start selected protocols.

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

        Stop selected protocols.

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
