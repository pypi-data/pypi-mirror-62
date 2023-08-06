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


class SpbmNodeBaseVidRange(Base):
    """The SPBM Node Base VLAN ID Range.
    The SpbmNodeBaseVidRange class encapsulates a list of spbmNodeBaseVidRange resources that is be managed by the user.
    A list of resources can be retrieved from the server using the SpbmNodeBaseVidRange.find() method.
    The list can be managed by the user by using the SpbmNodeBaseVidRange.add() and SpbmNodeBaseVidRange.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'spbmNodeBaseVidRange'

    def __init__(self, parent):
        super(SpbmNodeBaseVidRange, self).__init__(parent)

    @property
    def SpbmNodeIsIdRange(self):
        """An instance of the SpbmNodeIsIdRange class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.spbmnodeisidrange_66a4e09ee9e28a4afee3fbd813597d20.SpbmNodeIsIdRange)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.spbmnodeisidrange_66a4e09ee9e28a4afee3fbd813597d20 import SpbmNodeIsIdRange
        return SpbmNodeIsIdRange(self)

    @property
    def BVlanPriority(self):
        """The user priority of the Base VLAN.

        Returns:
            number
        """
        return self._get_attribute('bVlanPriority')
    @BVlanPriority.setter
    def BVlanPriority(self, value):
        self._set_attribute('bVlanPriority', value)

    @property
    def BVlanTpId(self):
        """The tag priority identifier for base VLAN.

        Returns:
            number
        """
        return self._get_attribute('bVlanTpId')
    @BVlanTpId.setter
    def BVlanTpId(self, value):
        self._set_attribute('bVlanTpId', value)

    @property
    def BaseVid(self):
        """The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.

        Returns:
            number
        """
        return self._get_attribute('baseVid')
    @BaseVid.setter
    def BaseVid(self, value):
        self._set_attribute('baseVid', value)

    @property
    def EctAlgorithm(self):
        """The SPB Equal Cost Tree (ECT) algorithm. The default algorithm is 01-80-C2-01.

        Returns:
            number
        """
        return self._get_attribute('ectAlgorithm')
    @EctAlgorithm.setter
    def EctAlgorithm(self, value):
        self._set_attribute('ectAlgorithm', value)

    @property
    def UseFlag(self):
        """Set to true to activate the user flag.

        Returns:
            bool
        """
        return self._get_attribute('useFlag')
    @UseFlag.setter
    def UseFlag(self, value):
        self._set_attribute('useFlag', value)

    def update(self, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithm=None, UseFlag=None):
        """Updates a child instance of spbmNodeBaseVidRange on the server.

        Args:
            BVlanPriority (number): The user priority of the Base VLAN.
            BVlanTpId (number): The tag priority identifier for base VLAN.
            BaseVid (number): The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.
            EctAlgorithm (number): The SPB Equal Cost Tree (ECT) algorithm. The default algorithm is 01-80-C2-01.
            UseFlag (bool): Set to true to activate the user flag.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def add(self, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithm=None, UseFlag=None):
        """Adds a new spbmNodeBaseVidRange node on the server and retrieves it in this instance.

        Args:
            BVlanPriority (number): The user priority of the Base VLAN.
            BVlanTpId (number): The tag priority identifier for base VLAN.
            BaseVid (number): The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.
            EctAlgorithm (number): The SPB Equal Cost Tree (ECT) algorithm. The default algorithm is 01-80-C2-01.
            UseFlag (bool): Set to true to activate the user flag.

        Returns:
            self: This instance with all currently retrieved spbmNodeBaseVidRange data using find and the newly added spbmNodeBaseVidRange data available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(locals())

    def remove(self):
        """Deletes all the spbmNodeBaseVidRange data in this instance from server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithm=None, UseFlag=None):
        """Finds and retrieves spbmNodeBaseVidRange data from the server.

        All named parameters support regex and can be used to selectively retrieve spbmNodeBaseVidRange data from the server.
        By default the find method takes no parameters and will retrieve all spbmNodeBaseVidRange data from the server.

        Args:
            BVlanPriority (number): The user priority of the Base VLAN.
            BVlanTpId (number): The tag priority identifier for base VLAN.
            BaseVid (number): The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.
            EctAlgorithm (number): The SPB Equal Cost Tree (ECT) algorithm. The default algorithm is 01-80-C2-01.
            UseFlag (bool): Set to true to activate the user flag.

        Returns:
            self: This instance with matching spbmNodeBaseVidRange data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of spbmNodeBaseVidRange data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the spbmNodeBaseVidRange data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)
