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


class TrackingFilter(Base):
    """Tracking filter specification.
    The TrackingFilter class encapsulates a list of trackingFilter resources that is be managed by the user.
    A list of resources can be retrieved from the server using the TrackingFilter.find() method.
    The list can be managed by the user by using the TrackingFilter.add() and TrackingFilter.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'trackingFilter'

    def __init__(self, parent):
        super(TrackingFilter, self).__init__(parent)

    @property
    def Operator(self):
        """The logical operation to be performed.

        Returns:
            str(isAnyOf|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isInAnyRange|isNoneOf|isSmaller)
        """
        return self._get_attribute('operator')
    @Operator.setter
    def Operator(self, value):
        self._set_attribute('operator', value)

    @property
    def TrackingFilterId(self):
        """Selected tracking filters from the availableTrackingFilter list.

        Returns:
            str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)
        """
        return self._get_attribute('trackingFilterId')
    @TrackingFilterId.setter
    def TrackingFilterId(self, value):
        self._set_attribute('trackingFilterId', value)

    @property
    def Value(self):
        """Value of the object

        Returns:
            list(str)
        """
        return self._get_attribute('value')
    @Value.setter
    def Value(self, value):
        self._set_attribute('value', value)

    def update(self, Operator=None, TrackingFilterId=None, Value=None):
        """Updates a child instance of trackingFilter on the server.

        Args:
            Operator (str(isAnyOf|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isInAnyRange|isNoneOf|isSmaller)): The logical operation to be performed.
            TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): Selected tracking filters from the availableTrackingFilter list.
            Value (list(str)): Value of the object

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def add(self, Operator=None, TrackingFilterId=None, Value=None):
        """Adds a new trackingFilter node on the server and retrieves it in this instance.

        Args:
            Operator (str(isAnyOf|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isInAnyRange|isNoneOf|isSmaller)): The logical operation to be performed.
            TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): Selected tracking filters from the availableTrackingFilter list.
            Value (list(str)): Value of the object

        Returns:
            self: This instance with all currently retrieved trackingFilter data using find and the newly added trackingFilter data available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(locals())

    def remove(self):
        """Deletes all the trackingFilter data in this instance from server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, Operator=None, TrackingFilterId=None, Value=None):
        """Finds and retrieves trackingFilter data from the server.

        All named parameters support regex and can be used to selectively retrieve trackingFilter data from the server.
        By default the find method takes no parameters and will retrieve all trackingFilter data from the server.

        Args:
            Operator (str(isAnyOf|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isInAnyRange|isNoneOf|isSmaller)): The logical operation to be performed.
            TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): Selected tracking filters from the availableTrackingFilter list.
            Value (list(str)): Value of the object

        Returns:
            self: This instance with matching trackingFilter data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of trackingFilter data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the trackingFilter data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)
