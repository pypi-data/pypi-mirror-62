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


class Device(Base):
    """Indicates that the device is used to configure the protocol.
    The Device class encapsulates a list of device resources that is be managed by the user.
    A list of resources can be retrieved from the server using the Device.find() method.
    The list can be managed by the user by using the Device.add() and Device.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'device'

    def __init__(self, parent):
        super(Device, self).__init__(parent)

    @property
    def Interface(self):
        """An instance of the Interface class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.interface_caab5eb40c486f45184116f2447c0e1b.Interface)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.interface_caab5eb40c486f45184116f2447c0e1b import Interface
        return Interface(self)

    @property
    def CaCertificateFile(self):
        """Indicates the Trusted Root certificate file for the device.

        Returns:
            str
        """
        return self._get_attribute('caCertificateFile')

    @property
    def CertificateFile(self):
        """Indicates the certificate file for the device.

        Returns:
            str
        """
        return self._get_attribute('certificateFile')

    @property
    def Description(self):
        """A description of the device used to configure this protocol.

        Returns:
            str
        """
        return self._get_attribute('description')
    @Description.setter
    def Description(self, value):
        self._set_attribute('description', value)

    @property
    def DeviceRole(self):
        """Indicates the device role of the OpenFlow device.

        Returns:
            str(controller|switch)
        """
        return self._get_attribute('deviceRole')
    @DeviceRole.setter
    def DeviceRole(self, value):
        self._set_attribute('deviceRole', value)

    @property
    def EnableVersion100(self):
        """Enables protocol version 1.0

        Returns:
            bool
        """
        return self._get_attribute('enableVersion100')
    @EnableVersion100.setter
    def EnableVersion100(self, value):
        self._set_attribute('enableVersion100', value)

    @property
    def EnableVersion131(self):
        """Enables protocol version 1.3

        Returns:
            bool
        """
        return self._get_attribute('enableVersion131')
    @EnableVersion131.setter
    def EnableVersion131(self, value):
        self._set_attribute('enableVersion131', value)

    @property
    def Enabled(self):
        """If set enables the open-flow device.

        Returns:
            bool
        """
        return self._get_attribute('enabled')
    @Enabled.setter
    def Enabled(self, value):
        self._set_attribute('enabled', value)

    @property
    def PrivateFile(self):
        """Indicates the private key file for the device.

        Returns:
            str
        """
        return self._get_attribute('privateFile')

    @property
    def Version(self):
        """DEPRECATED Indicates the current version of the Openflow protocol implemented.

        Returns:
            str(1.0.0)
        """
        return self._get_attribute('version')
    @Version.setter
    def Version(self, value):
        self._set_attribute('version', value)

    def update(self, Description=None, DeviceRole=None, EnableVersion100=None, EnableVersion131=None, Enabled=None, Version=None):
        """Updates a child instance of device on the server.

        Args:
            Description (str): A description of the device used to configure this protocol.
            DeviceRole (str(controller|switch)): Indicates the device role of the OpenFlow device.
            EnableVersion100 (bool): Enables protocol version 1.0
            EnableVersion131 (bool): Enables protocol version 1.3
            Enabled (bool): If set enables the open-flow device.
            Version (str(1.0.0)): Indicates the current version of the Openflow protocol implemented.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def add(self, Description=None, DeviceRole=None, EnableVersion100=None, EnableVersion131=None, Enabled=None, Version=None):
        """Adds a new device node on the server and retrieves it in this instance.

        Args:
            Description (str): A description of the device used to configure this protocol.
            DeviceRole (str(controller|switch)): Indicates the device role of the OpenFlow device.
            EnableVersion100 (bool): Enables protocol version 1.0
            EnableVersion131 (bool): Enables protocol version 1.3
            Enabled (bool): If set enables the open-flow device.
            Version (str(1.0.0)): Indicates the current version of the Openflow protocol implemented.

        Returns:
            self: This instance with all currently retrieved device data using find and the newly added device data available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(locals())

    def remove(self):
        """Deletes all the device data in this instance from server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, CaCertificateFile=None, CertificateFile=None, Description=None, DeviceRole=None, EnableVersion100=None, EnableVersion131=None, Enabled=None, PrivateFile=None, Version=None):
        """Finds and retrieves device data from the server.

        All named parameters support regex and can be used to selectively retrieve device data from the server.
        By default the find method takes no parameters and will retrieve all device data from the server.

        Args:
            CaCertificateFile (str): Indicates the Trusted Root certificate file for the device.
            CertificateFile (str): Indicates the certificate file for the device.
            Description (str): A description of the device used to configure this protocol.
            DeviceRole (str(controller|switch)): Indicates the device role of the OpenFlow device.
            EnableVersion100 (bool): Enables protocol version 1.0
            EnableVersion131 (bool): Enables protocol version 1.3
            Enabled (bool): If set enables the open-flow device.
            PrivateFile (str): Indicates the private key file for the device.
            Version (str(1.0.0)): Indicates the current version of the Openflow protocol implemented.

        Returns:
            self: This instance with matching device data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of device data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the device data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def AddTlsCertificates(self, *args, **kwargs):
        """Executes the addTlsCertificates operation on the server.

        Exec to add TLS certificates.

        addTlsCertificates(Arg2:href, Arg3:href, Arg4:href)number
            Args:
                args[0] is Arg2 (obj(ixnetwork_restpy.files.Files)): NOT DEFINED
                args[1] is Arg3 (obj(ixnetwork_restpy.files.Files)): NOT DEFINED
                args[2] is Arg4 (obj(ixnetwork_restpy.files.Files)): NOT DEFINED

            Returns:
                number: NOT DEFINED

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('addTlsCertificates', payload=payload, response_object=None)
