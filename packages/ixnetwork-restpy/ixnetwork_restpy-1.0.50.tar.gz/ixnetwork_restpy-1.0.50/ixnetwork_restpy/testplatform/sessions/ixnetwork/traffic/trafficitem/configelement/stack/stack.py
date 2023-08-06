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


class Stack(Base):
    """This object helps to specify the field properties of a protocol stack.
    The Stack class encapsulates a list of stack resources that is managed by the system.
    A list of resources can be retrieved from the server using the Stack.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'stack'

    def __init__(self, parent):
        super(Stack, self).__init__(parent)

    @property
    def Field(self):
        """An instance of the Field class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stack.field.field.Field)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stack.field.field import Field
        return Field(self)

    @property
    def DisplayName(self):
        """The display name of the stack.

        Returns:
            str
        """
        return self._get_attribute('displayName')

    @property
    def StackTypeId(self):
        """

        Returns:
            str
        """
        return self._get_attribute('stackTypeId')

    @property
    def TemplateName(self):
        """Indiates the protocol template name that is added to a packet in a stack.

        Returns:
            str
        """
        return self._get_attribute('templateName')

    def find(self, DisplayName=None, StackTypeId=None, TemplateName=None):
        """Finds and retrieves stack data from the server.

        All named parameters support regex and can be used to selectively retrieve stack data from the server.
        By default the find method takes no parameters and will retrieve all stack data from the server.

        Args:
            DisplayName (str): The display name of the stack.
            StackTypeId (str): 
            TemplateName (str): Indiates the protocol template name that is added to a packet in a stack.

        Returns:
            self: This instance with matching stack data retrieved from the server available through an iterator or index

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(locals())

    def read(self, href):
        """Retrieves a single instance of stack data from the server.

        Args:
            href (str): An href to the instance to be retrieved

        Returns:
            self: This instance with the stack data from the server available through an iterator or index

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def Append(self, *args, **kwargs):
        """Executes the append operation on the server.

        Append a protocol template after the specified stack object reference.

        DEPRECATED append(Arg2:href)string
            Args:
                args[0] is Arg2 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=protocolTemplate)): A valid /traffic/protocolTemplate object reference.

            Returns:
                str: This exec returns an object reference to the newly appended stack item.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('append', payload=payload, response_object=None)

    def AppendProtocol(self, *args, **kwargs):
        """Executes the appendProtocol operation on the server.

        Append a protocol template after the specified stack object reference.

        appendProtocol(Arg2:href)href
            Args:
                args[0] is Arg2 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=protocolTemplate)): A valid /traffic/protocolTemplate object reference.

            Returns:
                str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stack): This exec returns an object reference to the newly appended stack item.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('appendProtocol', payload=payload, response_object=None)

    def GetValidProtocols(self):
        """Executes the getValidProtocols operation on the server.

        Retrieves the list of recommended protocols that can be added on top of the current protocol.

            Returns:
                list(str): This exec returns an array containing: the name of the protocol, the reference of the protocol and the type of it (successor or ancestor)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('getValidProtocols', payload=payload, response_object=None)

    def Insert(self, *args, **kwargs):
        """Executes the insert operation on the server.

        Insert a protocol template before the specified stack object reference.

        DEPRECATED insert(Arg2:href)string
            Args:
                args[0] is Arg2 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=protocolTemplate)): A valid /traffic/protocolTemplate object reference

            Returns:
                str: This exec returns an object reference to the newly inserted stack item.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('insert', payload=payload, response_object=None)

    def InsertProtocol(self, *args, **kwargs):
        """Executes the insertProtocol operation on the server.

        Insert a protocol template before the specified stack object reference.

        insertProtocol(Arg2:href)href
            Args:
                args[0] is Arg2 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=protocolTemplate)): A valid /traffic/protocolTemplate object reference

            Returns:
                str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stack): This exec returns an object reference to the newly inserted stack item.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('insertProtocol', payload=payload, response_object=None)

    def Remove(self):
        """Executes the remove operation on the server.

        Delete the specified stack object reference.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        return self._execute('remove', payload=payload, response_object=None)
