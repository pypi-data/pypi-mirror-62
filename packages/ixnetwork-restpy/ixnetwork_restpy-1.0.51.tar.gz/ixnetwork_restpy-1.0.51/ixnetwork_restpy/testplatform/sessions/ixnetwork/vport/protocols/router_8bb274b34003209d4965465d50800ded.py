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


class Router(Base):
    """This object represents a simulated router.
    The Router class encapsulates a list of router resources that is be managed by the user.
    A list of resources can be retrieved from the server using the Router.find() method.
    The list can be managed by the user by using the Router.add() and Router.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'router'

    def __init__(self, parent):
        super(Router, self).__init__(parent)

    @property
    def Interface(self):
        """An instance of the Interface class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.interface_3fd3ad5c7974f63314ea2d7b237f6967.Interface)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.interface_3fd3ad5c7974f63314ea2d7b237f6967 import Interface
        return Interface(self)

    @property
    def LearnedInformation(self):
        """An instance of the LearnedInformation class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.learnedinformation_6f323287cf4e4e63d4d555a86b09ff95.LearnedInformation)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.learnedinformation_6f323287cf4e4e63d4d555a86b09ff95 import LearnedInformation
        return LearnedInformation(self)._select()

    @property
    def Enabled(self):
        """This signifies the enablement of the simulated router.

        Returns:
            bool
        """
        return self._get_attribute('enabled')
    @Enabled.setter
    def Enabled(self, value):
        self._set_attribute('enabled', value)

    @property
    def RouterId(self):
        """This signifies the Id of the simulated router, expressed as an IP address.

        Returns:
            str
        """
        return self._get_attribute('routerId')
    @RouterId.setter
    def RouterId(self, value):
        self._set_attribute('routerId', value)

    def update(self, Enabled=None, RouterId=None):
        """Updates a child instance of router on the server.

        Args:
            Enabled (bool): This signifies the enablement of the simulated router.
            RouterId (str): This signifies the Id of the simulated router, expressed as an IP address.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def add(self, Enabled=None, RouterId=None):
        """Adds a new router node on the server and retrieves it in this instance.

        Args:
            Enabled (bool): This signifies the enablement of the simulated router.
            RouterId (str): This signifies the Id of the simulated router, expressed as an IP address.

        Returns:
            self: This instance with all currently retrieved router data using find and the newly added router data available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(locals())

    def remove(self):
        """Deletes all the router data in this instance from server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, Enabled=None, RouterId=None):
        """Finds and retrieves router data from the server.

        All named parameters support regex and can be used to selectively retrieve router data from the server.
        By default the find method takes no parameters and will retrieve all router data from the server.

        Args:
            Enabled (bool): This signifies the enablement of the simulated router.
            RouterId (str): This signifies the Id of the simulated router, expressed as an IP address.

        Returns:
            self: This instance with matching router data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of router data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the router data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)
