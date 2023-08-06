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


class Meters(Base):
    """Openflow Meter Configuration
    The Meters class encapsulates a list of meters resources that is managed by the system.
    A list of resources can be retrieved from the server using the Meters.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'meters'

    def __init__(self, parent):
        super(Meters, self).__init__(parent)

    @property
    def Bands(self):
        """An instance of the Bands class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bands.Bands)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bands import Bands
        return Bands(self)

    @property
    def Active(self):
        """Activate/Deactivate Configuration

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('active')

    @property
    def Advertise(self):
        """When this check box is cleared, no meter is advertised when the OpenFlow channel comes up or when the Enable check box is selected or cleared.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('advertise')

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
    def Flags(self):
        """Select the meter configuration flags from the list.

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('flags')

    @property
    def MeterDesc(self):
        """A description of the meter

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('meterDesc')

    @property
    def MeterId(self):
        """The value by which a meter is uniquely identified .

        Returns:
            obj(ixnetwork_restpy.multivalue.Multivalue)
        """
        return self._get_attribute('meterId')

    @property
    def Multiplier(self):
        """Number of instances per parent instance (multiplier)

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
    def NumberOfBands(self):
        """Specify the number of Bands.

        Returns:
            number
        """
        return self._get_attribute('numberOfBands')
    @NumberOfBands.setter
    def NumberOfBands(self, value):
        self._set_attribute('numberOfBands', value)

    def update(self, Multiplier=None, Name=None, NumberOfBands=None):
        """Updates a child instance of meters on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args:
            Multiplier (number): Number of instances per parent instance (multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario
            NumberOfBands (number): Specify the number of Bands.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def find(self, Count=None, DescriptiveName=None, Multiplier=None, Name=None, NumberOfBands=None):
        """Finds and retrieves meters data from the server.

        All named parameters support regex and can be used to selectively retrieve meters data from the server.
        By default the find method takes no parameters and will retrieve all meters data from the server.

        Args:
            Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
            DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
            Multiplier (number): Number of instances per parent instance (multiplier)
            Name (str): Name of NGPF element, guaranteed to be unique in Scenario
            NumberOfBands (number): Specify the number of Bands.

        Returns:
            self: This instance with matching meters data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of meters data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the meters data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def get_device_ids(self, PortNames=None, Active=None, Advertise=None, Flags=None, MeterDesc=None, MeterId=None):
        """Base class infrastructure that gets a list of meters device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args:
            PortNames (str): optional regex of port names
            Active (str): optional regex of active
            Advertise (str): optional regex of advertise
            Flags (str): optional regex of flags
            MeterDesc (str): optional regex of meterDesc
            MeterId (str): optional regex of meterId

        Returns:
            list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())

    def SendAllMeterAdd(self):
        """Executes the sendAllMeterAdd operation on the server.

        Sends a Meter Add on all meters.

            Returns:
                list(str): ID to associate each async action invocation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('sendAllMeterAdd', payload=payload, response_object=None)

    def SendAllMeterRemove(self):
        """Executes the sendAllMeterRemove operation on the server.

        Sends a Meter Remove on all meters.

            Returns:
                list(str): ID to associate each async action invocation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('sendAllMeterRemove', payload=payload, response_object=None)

    def SendMeterAdd(self, *args, **kwargs):
        """Executes the sendMeterAdd operation on the server.

        Sends a Meter Add on selected Meter.

        sendMeterAdd(Arg2:list)list
            Args:
                args[0] is Arg2 (list(number)): List of indices into the meter range grid

            Returns:
                list(str): ID to associate each async action invocation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('sendMeterAdd', payload=payload, response_object=None)

    def SendMeterRemove(self, *args, **kwargs):
        """Executes the sendMeterRemove operation on the server.

        Sends a Meter Remove on selected Meter.

        sendMeterRemove(Arg2:list)list
            Args:
                args[0] is Arg2 (list(number)): List of indices into the meter range grid

            Returns:
                list(str): ID to associate each async action invocation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('sendMeterRemove', payload=payload, response_object=None)
