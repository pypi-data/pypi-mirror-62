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


class LearnedInfo(Base):
    """The main learned information node that contains tables of learned information.
    The LearnedInfo class encapsulates a list of learnedInfo resources that is managed by the system.
    A list of resources can be retrieved from the server using the LearnedInfo.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'learnedInfo'

    def __init__(self, parent):
        super(LearnedInfo, self).__init__(parent)

    @property
    def Col(self):
        """An instance of the DEPRECATED Col class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.col.Col)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.col import Col
        return Col(self)

    @property
    def Table(self):
        """An instance of the Table class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.table.Table)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.table import Table
        return Table(self)

    @property
    def __id__(self):
        """A unique id for the learned information table

        Returns:
            list(str)
        """
        return self._get_attribute('__id__')

    @property
    def Columns(self):
        """DEPRECATED The list of columns in the learned information table

        Returns:
            list(str)
        """
        return self._get_attribute('columns')

    @property
    def State(self):
        """The state of the learned information query

        Returns:
            str
        """
        return self._get_attribute('state')

    @property
    def Type(self):
        """DEPRECATED The type of learned information

        Returns:
            str
        """
        return self._get_attribute('type')

    @property
    def Values(self):
        """DEPRECATED A list of rows of learned information values

        Returns:
            list(list[str])
        """
        return self._get_attribute('values')

    def find(self, __id__=None, Columns=None, State=None, Type=None, Values=None):
        """Finds and retrieves learnedInfo data from the server.

        All named parameters support regex and can be used to selectively retrieve learnedInfo data from the server.
        By default the find method takes no parameters and will retrieve all learnedInfo data from the server.

        Args:
            __id__ (list(str)): A unique id for the learned information table
            Columns (list(str)): The list of columns in the learned information table
            State (str): The state of the learned information query
            Type (str): The type of learned information
            Values (list(list[str])): A list of rows of learned information values

        Returns:
            self: This instance with matching learnedInfo data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of learnedInfo data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the learnedInfo data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)
