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


class AtmLabelRange(Base):
    """A single ATM label range of VPIs and VCIs used for ATM sessions.
    The AtmLabelRange class encapsulates a list of atmLabelRange resources that is be managed by the user.
    A list of resources can be retrieved from the server using the AtmLabelRange.find() method.
    The list can be managed by the user by using the AtmLabelRange.add() and AtmLabelRange.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'atmLabelRange'

    def __init__(self, parent):
        super(AtmLabelRange, self).__init__(parent)

    @property
    def MaxVci(self):
        """The maximum virtual circuit identifier (VCI) value that will be included in the ATM label range. The valid maximum VCI value = 65,535 [0xFFFF (hex)].

        Returns:
            number
        """
        return self._get_attribute('maxVci')
    @MaxVci.setter
    def MaxVci(self, value):
        self._set_attribute('maxVci', value)

    @property
    def MaxVpi(self):
        """The maximum virtual path identifier (VPI) value that will be included in the ATM label range.

        Returns:
            number
        """
        return self._get_attribute('maxVpi')
    @MaxVpi.setter
    def MaxVpi(self, value):
        self._set_attribute('maxVpi', value)

    @property
    def MinVci(self):
        """The minimum virtual circuit identifier (VCI) value that will be included in the ATM label range.The valid minimum VCI value = 33.

        Returns:
            number
        """
        return self._get_attribute('minVci')
    @MinVci.setter
    def MinVci(self, value):
        self._set_attribute('minVci', value)

    @property
    def MinVpi(self):
        """The minimum virtual path identifier (VPI) value that will be included in the ATM label range.

        Returns:
            number
        """
        return self._get_attribute('minVpi')
    @MinVpi.setter
    def MinVpi(self, value):
        self._set_attribute('minVpi', value)

    def update(self, MaxVci=None, MaxVpi=None, MinVci=None, MinVpi=None):
        """Updates a child instance of atmLabelRange on the server.

        Args:
            MaxVci (number): The maximum virtual circuit identifier (VCI) value that will be included in the ATM label range. The valid maximum VCI value = 65,535 [0xFFFF (hex)].
            MaxVpi (number): The maximum virtual path identifier (VPI) value that will be included in the ATM label range.
            MinVci (number): The minimum virtual circuit identifier (VCI) value that will be included in the ATM label range.The valid minimum VCI value = 33.
            MinVpi (number): The minimum virtual path identifier (VPI) value that will be included in the ATM label range.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def add(self, MaxVci=None, MaxVpi=None, MinVci=None, MinVpi=None):
        """Adds a new atmLabelRange node on the server and retrieves it in this instance.

        Args:
            MaxVci (number): The maximum virtual circuit identifier (VCI) value that will be included in the ATM label range. The valid maximum VCI value = 65,535 [0xFFFF (hex)].
            MaxVpi (number): The maximum virtual path identifier (VPI) value that will be included in the ATM label range.
            MinVci (number): The minimum virtual circuit identifier (VCI) value that will be included in the ATM label range.The valid minimum VCI value = 33.
            MinVpi (number): The minimum virtual path identifier (VPI) value that will be included in the ATM label range.

        Returns:
            self: This instance with all currently retrieved atmLabelRange data using find and the newly added atmLabelRange data available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(locals())

    def remove(self):
        """Deletes all the atmLabelRange data in this instance from server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, MaxVci=None, MaxVpi=None, MinVci=None, MinVpi=None):
        """Finds and retrieves atmLabelRange data from the server.

        All named parameters support regex and can be used to selectively retrieve atmLabelRange data from the server.
        By default the find method takes no parameters and will retrieve all atmLabelRange data from the server.

        Args:
            MaxVci (number): The maximum virtual circuit identifier (VCI) value that will be included in the ATM label range. The valid maximum VCI value = 65,535 [0xFFFF (hex)].
            MaxVpi (number): The maximum virtual path identifier (VPI) value that will be included in the ATM label range.
            MinVci (number): The minimum virtual circuit identifier (VCI) value that will be included in the ATM label range.The valid minimum VCI value = 33.
            MinVpi (number): The minimum virtual path identifier (VPI) value that will be included in the ATM label range.

        Returns:
            self: This instance with matching atmLabelRange data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of atmLabelRange data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the atmLabelRange data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)
