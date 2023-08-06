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


class Card(Base):
    """This command allows the user to view version and type information for the card.
    The Card class encapsulates a list of card resources that is managed by the system.
    A list of resources can be retrieved from the server using the Card.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'card'

    def __init__(self, parent):
        super(Card, self).__init__(parent)

    @property
    def Aggregation(self):
        """An instance of the Aggregation class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.aggregation.aggregation.Aggregation)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.aggregation.aggregation import Aggregation
        return Aggregation(self)

    @property
    def Port(self):
        """An instance of the Port class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.port.port.Port)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.port.port import Port
        return Port(self)

    @property
    def AggregationMode(self):
        """Gets or sets the aggregation mode.

        Returns:
            str(notSupported|mixed|normal|tenGigAggregation|fortyGigAggregation|singleMode|dualMode|hundredGigNonFanOut|fortyGigFanOut|threeByTenGigFanOut|eightByTenGigFanOut|fourByTwentyFiveGigNonFanOut|twoByTwentyFiveGigNonFanOut|oneByFiftyGigNonFanOut|fortyGigNonFanOut|oneByTenGigFanOut|fourByTenGigFanOut|incompatibleMode|hundredGigCapturePlayback|fortyGigCapturePlayback|novusHundredGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusTwoByFiftyGigNonFanOut|novusOneByFortyGigNonFanOut|novusFourByTenGigNonFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|krakenFourByFiftyGigFanOut|aresOneOneByFourHundredGigNonFanOut|aresOneTwoByTwoHundredGigFanOut|aresOneFourByOneHundredGigFanOut|aresOneEightByFiftyGigFanOut)
        """
        return self._get_attribute('aggregationMode')
    @AggregationMode.setter
    def AggregationMode(self, value):
        self._set_attribute('aggregationMode', value)

    @property
    def AggregationSupported(self):
        """(read only) If true, indicates that the card is operating in resource group mode and not in normal mode

        Returns:
            bool
        """
        return self._get_attribute('aggregationSupported')

    @property
    def AvailableModes(self):
        """Gets the supported port resource group modes on the card.

        Returns:
            list(str[notSupported|mixed|normal|tenGigAggregation|fortyGigAggregation|singleMode|dualMode|hundredGigNonFanOut|fortyGigFanOut|threeByTenGigFanOut|eightByTenGigFanOut|fourByTwentyFiveGigNonFanOut|twoByTwentyFiveGigNonFanOut|oneByFiftyGigNonFanOut|fortyGigNonFanOut|oneByTenGigFanOut|fourByTenGigFanOut|incompatibleMode|hundredGigCapturePlayback|fortyGigCapturePlayback|novusHundredGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusTwoByFiftyGigNonFanOut|novusOneByFortyGigNonFanOut|novusFourByTenGigNonFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|krakenFourByFiftyGigFanOut|aresOneOneByFourHundredGigNonFanOut|aresOneTwoByTwoHundredGigFanOut|aresOneFourByOneHundredGigFanOut|aresOneEightByFiftyGigFanOut])
        """
        return self._get_attribute('availableModes')

    @property
    def CardId(self):
        """Identifier for the card on the chassis.

        Returns:
            number
        """
        return self._get_attribute('cardId')

    @property
    def Description(self):
        """Description of the card.

        Returns:
            str
        """
        return self._get_attribute('description')

    def update(self, AggregationMode=None):
        """Updates a child instance of card on the server.

        Args:
            AggregationMode (str(notSupported|mixed|normal|tenGigAggregation|fortyGigAggregation|singleMode|dualMode|hundredGigNonFanOut|fortyGigFanOut|threeByTenGigFanOut|eightByTenGigFanOut|fourByTwentyFiveGigNonFanOut|twoByTwentyFiveGigNonFanOut|oneByFiftyGigNonFanOut|fortyGigNonFanOut|oneByTenGigFanOut|fourByTenGigFanOut|incompatibleMode|hundredGigCapturePlayback|fortyGigCapturePlayback|novusHundredGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusTwoByFiftyGigNonFanOut|novusOneByFortyGigNonFanOut|novusFourByTenGigNonFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|krakenFourByFiftyGigFanOut|aresOneOneByFourHundredGigNonFanOut|aresOneTwoByTwoHundredGigFanOut|aresOneFourByOneHundredGigFanOut|aresOneEightByFiftyGigFanOut)): Gets or sets the aggregation mode.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def find(self, AggregationMode=None, AggregationSupported=None, AvailableModes=None, CardId=None, Description=None):
        """Finds and retrieves card data from the server.

        All named parameters support regex and can be used to selectively retrieve card data from the server.
        By default the find method takes no parameters and will retrieve all card data from the server.

        Args:
            AggregationMode (str(notSupported|mixed|normal|tenGigAggregation|fortyGigAggregation|singleMode|dualMode|hundredGigNonFanOut|fortyGigFanOut|threeByTenGigFanOut|eightByTenGigFanOut|fourByTwentyFiveGigNonFanOut|twoByTwentyFiveGigNonFanOut|oneByFiftyGigNonFanOut|fortyGigNonFanOut|oneByTenGigFanOut|fourByTenGigFanOut|incompatibleMode|hundredGigCapturePlayback|fortyGigCapturePlayback|novusHundredGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusTwoByFiftyGigNonFanOut|novusOneByFortyGigNonFanOut|novusFourByTenGigNonFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|krakenFourByFiftyGigFanOut|aresOneOneByFourHundredGigNonFanOut|aresOneTwoByTwoHundredGigFanOut|aresOneFourByOneHundredGigFanOut|aresOneEightByFiftyGigFanOut)): Gets or sets the aggregation mode.
            AggregationSupported (bool): (read only) If true, indicates that the card is operating in resource group mode and not in normal mode
            AvailableModes (list(str[notSupported|mixed|normal|tenGigAggregation|fortyGigAggregation|singleMode|dualMode|hundredGigNonFanOut|fortyGigFanOut|threeByTenGigFanOut|eightByTenGigFanOut|fourByTwentyFiveGigNonFanOut|twoByTwentyFiveGigNonFanOut|oneByFiftyGigNonFanOut|fortyGigNonFanOut|oneByTenGigFanOut|fourByTenGigFanOut|incompatibleMode|hundredGigCapturePlayback|fortyGigCapturePlayback|novusHundredGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusTwoByFiftyGigNonFanOut|novusOneByFortyGigNonFanOut|novusFourByTenGigNonFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|krakenFourByFiftyGigFanOut|aresOneOneByFourHundredGigNonFanOut|aresOneTwoByTwoHundredGigFanOut|aresOneFourByOneHundredGigFanOut|aresOneEightByFiftyGigFanOut])): Gets the supported port resource group modes on the card.
            CardId (number): Identifier for the card on the chassis.
            Description (str): Description of the card.

        Returns:
            self: This instance with matching card data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of card data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the card data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def RefreshInfo(self):
        """Executes the refreshInfo operation on the server.

        Refresh the hardware information.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        return self._execute('refreshInfo', payload=payload, response_object=None)
