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


class TlvProfile(Base):
    """Tlv profile functionality is contained under this node
    The TlvProfile class encapsulates a list of tlvProfile resources that is managed by the system.
    A list of resources can be retrieved from the server using the TlvProfile.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'tlvProfile'

    def __init__(self, parent):
        super(TlvProfile, self).__init__(parent)

    @property
    def DefaultTlv(self):
        """An instance of the DefaultTlv class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.defaulttlv.DefaultTlv)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.defaulttlv import DefaultTlv
        return DefaultTlv(self)

    @property
    def Tlv(self):
        """An instance of the Tlv class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlv.Tlv)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlv import Tlv
        return Tlv(self)

    def find(self):
        """Finds and retrieves tlvProfile data from the server.

        All named parameters support regex and can be used to selectively retrieve tlvProfile data from the server.
        By default the find method takes no parameters and will retrieve all tlvProfile data from the server.

        Returns:
            self: This instance with matching tlvProfile data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of tlvProfile data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the tlvProfile data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def CopyTlv(self, *args, **kwargs):
        """Executes the copyTlv operation on the server.

        Copy a template tlv to a topology tlv profile

        copyTlv(Arg2:href)href
            Args:
                args[0] is Arg2 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=topology)): An object reference to a source template tlv

            Returns:
                str(None): An object reference to the newly created topology tlv as a result of the copy operation

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('copyTlv', payload=payload, response_object=None)
