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


class RouteImportOptions(Base):
    """This object holds the available options for the imported routes.
    The RouteImportOptions class encapsulates a list of routeImportOptions resources that is be managed by the user.
    A list of resources can be retrieved from the server using the RouteImportOptions.find() method.
    The list can be managed by the user by using the RouteImportOptions.add() and RouteImportOptions.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'routeImportOptions'

    def __init__(self, parent):
        super(RouteImportOptions, self).__init__(parent)

    @property
    def AdverstiseBestRoutes(self):
        """If checked, only the best routes are imbibed and advertised. The sub-optimal routes are ignored.

        Returns:
            bool
        """
        return self._get_attribute('adverstiseBestRoutes')
    @AdverstiseBestRoutes.setter
    def AdverstiseBestRoutes(self, value):
        self._set_attribute('adverstiseBestRoutes', value)

    @property
    def NextHopAsIs(self):
        """If true, it takes the next Hop AsIs.

        Returns:
            bool
        """
        return self._get_attribute('nextHopAsIs')
    @NextHopAsIs.setter
    def NextHopAsIs(self, value):
        self._set_attribute('nextHopAsIs', value)

    @property
    def NumberOfRoutesPerBlock(self):
        """Represents the maximum number of routes that can be forwared in a block.

        Returns:
            number
        """
        return self._get_attribute('numberOfRoutesPerBlock')
    @NumberOfRoutesPerBlock.setter
    def NumberOfRoutesPerBlock(self, value):
        self._set_attribute('numberOfRoutesPerBlock', value)

    @property
    def RouteFileType(self):
        """The route file type.

        Returns:
            str
        """
        return self._get_attribute('routeFileType')
    @RouteFileType.setter
    def RouteFileType(self, value):
        self._set_attribute('routeFileType', value)

    @property
    def SendMultiExitDiscValue(self):
        """If enabled, the BGP router sends the MED value of the attribute.

        Returns:
            bool
        """
        return self._get_attribute('sendMultiExitDiscValue')
    @SendMultiExitDiscValue.setter
    def SendMultiExitDiscValue(self, value):
        self._set_attribute('sendMultiExitDiscValue', value)

    def update(self, AdverstiseBestRoutes=None, NextHopAsIs=None, NumberOfRoutesPerBlock=None, RouteFileType=None, SendMultiExitDiscValue=None):
        """Updates a child instance of routeImportOptions on the server.

        Args:
            AdverstiseBestRoutes (bool): If checked, only the best routes are imbibed and advertised. The sub-optimal routes are ignored.
            NextHopAsIs (bool): If true, it takes the next Hop AsIs.
            NumberOfRoutesPerBlock (number): Represents the maximum number of routes that can be forwared in a block.
            RouteFileType (str): The route file type.
            SendMultiExitDiscValue (bool): If enabled, the BGP router sends the MED value of the attribute.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def add(self, AdverstiseBestRoutes=None, NextHopAsIs=None, NumberOfRoutesPerBlock=None, RouteFileType=None, SendMultiExitDiscValue=None):
        """Adds a new routeImportOptions node on the server and retrieves it in this instance.

        Args:
            AdverstiseBestRoutes (bool): If checked, only the best routes are imbibed and advertised. The sub-optimal routes are ignored.
            NextHopAsIs (bool): If true, it takes the next Hop AsIs.
            NumberOfRoutesPerBlock (number): Represents the maximum number of routes that can be forwared in a block.
            RouteFileType (str): The route file type.
            SendMultiExitDiscValue (bool): If enabled, the BGP router sends the MED value of the attribute.

        Returns:
            self: This instance with all currently retrieved routeImportOptions data using find and the newly added routeImportOptions data available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(locals())

    def remove(self):
        """Deletes all the routeImportOptions data in this instance from server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, AdverstiseBestRoutes=None, NextHopAsIs=None, NumberOfRoutesPerBlock=None, RouteFileType=None, SendMultiExitDiscValue=None):
        """Finds and retrieves routeImportOptions data from the server.

        All named parameters support regex and can be used to selectively retrieve routeImportOptions data from the server.
        By default the find method takes no parameters and will retrieve all routeImportOptions data from the server.

        Args:
            AdverstiseBestRoutes (bool): If checked, only the best routes are imbibed and advertised. The sub-optimal routes are ignored.
            NextHopAsIs (bool): If true, it takes the next Hop AsIs.
            NumberOfRoutesPerBlock (number): Represents the maximum number of routes that can be forwared in a block.
            RouteFileType (str): The route file type.
            SendMultiExitDiscValue (bool): If enabled, the BGP router sends the MED value of the attribute.

        Returns:
            self: This instance with matching routeImportOptions data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of routeImportOptions data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the routeImportOptions data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def GetSupportedBGPRouteFileTypes(self):
        """Executes the getSupportedBGPRouteFileTypes operation on the server.

        This function allows to Get supported BGP router.

            Returns:
                str: NOT DEFINED

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('getSupportedBGPRouteFileTypes', payload=payload, response_object=None)

    def ImportOpaqueRouteRangeFromFile(self, *args, **kwargs):
        """Executes the importOpaqueRouteRangeFromFile operation on the server.

        This function allows to import opaque route range from file.

        importOpaqueRouteRangeFromFile(Arg2:href)
            Args:
                args[0] is Arg2 (obj(ixnetwork_restpy.files.Files)): NOT DEFINED

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('importOpaqueRouteRangeFromFile', payload=payload, response_object=None)
