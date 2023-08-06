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


class Mpls(Base):
    """MPLS protocol.
    The Mpls class encapsulates a list of mpls resources that is be managed by the user.
    A list of resources can be retrieved from the server using the Mpls.find() method.
    The list can be managed by the user by using the Mpls.add() and Mpls.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'mpls'

    def __init__(self, parent):
        super(Mpls, self).__init__(parent)

    @property
    def BondedGRE(self):
        """An instance of the BondedGRE class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bondedgre.BondedGRE)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bondedgre import BondedGRE
        return BondedGRE(self)

    @property
    def CfmBridge(self):
        """An instance of the CfmBridge class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cfmbridge.CfmBridge)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cfmbridge import CfmBridge
        return CfmBridge(self)

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
    def Dhcpv4client(self):
        """An instance of the Dhcpv4client class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dhcpv4client.Dhcpv4client)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dhcpv4client import Dhcpv4client
        return Dhcpv4client(self)

    @property
    def Dhcpv6client(self):
        """An instance of the Dhcpv6client class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dhcpv6client.Dhcpv6client)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.dhcpv6client import Dhcpv6client
        return Dhcpv6client(self)

    @property
    def ECpriRe(self):
        """An instance of the ECpriRe class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ecprire.ECpriRe)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ecprire import ECpriRe
        return ECpriRe(self)

    @property
    def ECpriRec(self):
        """An instance of the ECpriRec class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ecprirec.ECpriRec)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ecprirec import ECpriRec
        return ECpriRec(self)

    @property
    def Ethernet(self):
        """An instance of the Ethernet class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ethernet.Ethernet)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ethernet import Ethernet
        return Ethernet(self)

    @property
    def Ipv4(self):
        """An instance of the Ipv4 class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4.Ipv4)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4 import Ipv4
        return Ipv4(self)

    @property
    def Ipv6(self):
        """An instance of the Ipv6 class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6.Ipv6)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6 import Ipv6
        return Ipv6(self)

    @property
    def Ipv6Autoconfiguration(self):
        """An instance of the Ipv6Autoconfiguration class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6autoconfiguration.Ipv6Autoconfiguration)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6autoconfiguration import Ipv6Autoconfiguration
        return Ipv6Autoconfiguration(self)

    @property
    def IsisDceSimRouter(self):
        """An instance of the IsisDceSimRouter class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcesimrouter.IsisDceSimRouter)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcesimrouter import IsisDceSimRouter
        return IsisDceSimRouter(self)

    @property
    def IsisFabricPath(self):
        """An instance of the IsisFabricPath class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisfabricpath.IsisFabricPath)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisfabricpath import IsisFabricPath
        return IsisFabricPath(self)

    @property
    def IsisL3(self):
        """An instance of the IsisL3 class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3.IsisL3)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3 import IsisL3
        return IsisL3(self)

    @property
    def IsisSpbBcb(self):
        """An instance of the IsisSpbBcb class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbbcb.IsisSpbBcb)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbbcb import IsisSpbBcb
        return IsisSpbBcb(self)

    @property
    def IsisSpbBeb(self):
        """An instance of the IsisSpbBeb class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbbeb.IsisSpbBeb)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbbeb import IsisSpbBeb
        return IsisSpbBeb(self)

    @property
    def IsisSpbSimRouter(self):
        """An instance of the IsisSpbSimRouter class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbsimrouter.IsisSpbSimRouter)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbsimrouter import IsisSpbSimRouter
        return IsisSpbSimRouter(self)

    @property
    def IsisTrill(self):
        """An instance of the IsisTrill class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrill.IsisTrill)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrill import IsisTrill
        return IsisTrill(self)

    @property
    def IsisTrillSimRouter(self):
        """An instance of the IsisTrillSimRouter class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillsimrouter.IsisTrillSimRouter)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillsimrouter import IsisTrillSimRouter
        return IsisTrillSimRouter(self)

    @property
    def Lacp(self):
        """An instance of the Lacp class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.lacp.Lacp)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.lacp import Lacp
        return Lacp(self)

    @property
    def Lagportlacp(self):
        """An instance of the Lagportlacp class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.lagportlacp.Lagportlacp)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.lagportlacp import Lagportlacp
        return Lagportlacp(self)

    @property
    def Lagportstaticlag(self):
        """An instance of the Lagportstaticlag class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.lagportstaticlag.Lagportstaticlag)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.lagportstaticlag import Lagportstaticlag
        return Lagportstaticlag(self)

    @property
    def Mpls(self):
        """An instance of the Mpls class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mpls.Mpls)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mpls import Mpls
        return Mpls(self)

    @property
    def MsrpListener(self):
        """An instance of the MsrpListener class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.msrplistener.MsrpListener)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.msrplistener import MsrpListener
        return MsrpListener(self)

    @property
    def MsrpTalker(self):
        """An instance of the MsrpTalker class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.msrptalker.MsrpTalker)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.msrptalker import MsrpTalker
        return MsrpTalker(self)

    @property
    def StaticLag(self):
        """An instance of the StaticLag class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.staticlag.StaticLag)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.staticlag import StaticLag
        return StaticLag(self)

    @property
    def Streams(self):
        """An instance of the Streams class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.streams.Streams)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.streams import Streams
        return Streams(self)

    @property
    def Bos(self):
        """bos

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('bos')

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
    def Cos(self):
        """EXP

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('cos')

    @property
    def Count(self):
        """Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.

        Returns:
            number
        """
        return self._get_attribute('count')

    @property
    def DescriptiveName(self):
        """Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context

        Returns:
            str
        """
        return self._get_attribute('descriptiveName')

    @property
    def DestMac(self):
        """Destination Mac.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('destMac')

    @property
    def Enablecw(self):
        """Enable Control Word

        Returns:
            bool
        """
        return self._get_attribute('enablecw')
    @Enablecw.setter
    def Enablecw(self, value):
        self._set_attribute('enablecw', value)

    @property
    def Errors(self):
        """A list of errors that have occurred

        Returns:
            list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
        """
        return self._get_attribute('errors')

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
    def Overridecos(self):
        """Override Cos

        Returns:
            bool
        """
        return self._get_attribute('overridecos')
    @Overridecos.setter
    def Overridecos(self, value):
        self._set_attribute('overridecos', value)

    @property
    def RxLabelValue(self):
        """Rx Label

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('rxLabelValue')

    @property
    def SessionInfo(self):
        """Logs additional information about the session state

        Returns:
            list(str[interfaceCreationFailed|interfaceDeletionFailed|interfaceInternalProblem|none])
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
    def TransportType(self):
        """TransportType

        Returns:
            str(overMac|overTunnel)
        """
        return self._get_attribute('transportType')
    @TransportType.setter
    def TransportType(self, value):
        self._set_attribute('transportType', value)

    @property
    def Ttl(self):
        """TTL

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('ttl')

    @property
    def TxLabelValue(self):
        """Tx Label

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('txLabelValue')

    @property
    def UpperLayer(self):
        """Value to Determine who is upper Layer.

        Returns:
            str(nhEthernet|nhIp)
        """
        return self._get_attribute('upperLayer')
    @UpperLayer.setter
    def UpperLayer(self, value):
        self._set_attribute('upperLayer', value)

    def update(self, ConnectedVia=None, Enablecw=None, Multiplier=None, Name=None, Overridecos=None, StackedLayers=None, TransportType=None, UpperLayer=None):
        """Updates a child instance of mpls on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args:
            ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
            Enablecw (bool): Enable Control Word
            Multiplier (number): Number of layer instances per parent instance (multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario
            Overridecos (bool): Override Cos
            StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
            TransportType (str(overMac|overTunnel)): TransportType
            UpperLayer (str(nhEthernet|nhIp)): Value to Determine who is upper Layer.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def add(self, ConnectedVia=None, Enablecw=None, Multiplier=None, Name=None, Overridecos=None, StackedLayers=None, TransportType=None, UpperLayer=None):
        """Adds a new mpls node on the server and retrieves it in this instance.

        Args:
            ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
            Enablecw (bool): Enable Control Word
            Multiplier (number): Number of layer instances per parent instance (multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario
            Overridecos (bool): Override Cos
            StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
            TransportType (str(overMac|overTunnel)): TransportType
            UpperLayer (str(nhEthernet|nhIp)): Value to Determine who is upper Layer.

        Returns:
            self: This instance with all currently retrieved mpls data using find and the newly added mpls data available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(locals())

    def remove(self):
        """Deletes all the mpls data in this instance from server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, ConnectedVia=None, Count=None, DescriptiveName=None, Enablecw=None, Errors=None, Multiplier=None, Name=None, Overridecos=None, SessionInfo=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None, TransportType=None, UpperLayer=None):
        """Finds and retrieves mpls data from the server.

        All named parameters support regex and can be used to selectively retrieve mpls data from the server.
        By default the find method takes no parameters and will retrieve all mpls data from the server.

        Args:
            ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
            Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
            DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
            Enablecw (bool): Enable Control Word
            Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
            Multiplier (number): Number of layer instances per parent instance (multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario
            Overridecos (bool): Override Cos
            SessionInfo (list(str[interfaceCreationFailed|interfaceDeletionFailed|interfaceInternalProblem|none])): Logs additional information about the session state
            SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
            StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
            StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
            Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.
            TransportType (str(overMac|overTunnel)): TransportType
            UpperLayer (str(nhEthernet|nhIp)): Value to Determine who is upper Layer.

        Returns:
            self: This instance with matching mpls data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of mpls data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the mpls data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def get_device_ids(self, PortNames=None, Bos=None, Cos=None, DestMac=None, RxLabelValue=None, Ttl=None, TxLabelValue=None):
        """Base class infrastructure that gets a list of mpls device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args:
            PortNames (str): optional regex of port names
            Bos (str): optional regex of bos
            Cos (str): optional regex of cos
            DestMac (str): optional regex of destMac
            RxLabelValue (str): optional regex of rxLabelValue
            Ttl (str): optional regex of ttl
            TxLabelValue (str): optional regex of txLabelValue

        Returns:
            list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())

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
