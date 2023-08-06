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


class Instructions(Base):
    """Instruction
    The Instructions class encapsulates a required instructions resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'instructions'

    def __init__(self, parent):
        super(Instructions, self).__init__(parent)

    @property
    def Instruction(self):
        """An instance of the Instruction class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.instruction.Instruction)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.instruction import Instruction
        return Instruction(self)

    @property
    def Count(self):
        """Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.

        Returns:
            number
        """
        return self._get_attribute('count')

    @property
    def Description(self):
        """Description of the field.

        Returns:
            str
        """
        return self._get_attribute('description')
    @Description.setter
    def Description(self, value):
        self._set_attribute('description', value)

    @property
    def DisplayName(self):
        """Display name used by GUI.

        Returns:
            str
        """
        return self._get_attribute('displayName')

    @property
    def IsEditable(self):
        """Information on the requirement of the field.

        Returns:
            bool
        """
        return self._get_attribute('isEditable')
    @IsEditable.setter
    def IsEditable(self, value):
        self._set_attribute('isEditable', value)

    @property
    def IsEnabled(self):
        """Enables disables the field.

        Returns:
            bool
        """
        return self._get_attribute('isEnabled')
    @IsEnabled.setter
    def IsEnabled(self, value):
        self._set_attribute('isEnabled', value)

    @property
    def IsRequired(self):
        """Information on the requirement of the field.

        Returns:
            bool
        """
        return self._get_attribute('isRequired')
    @IsRequired.setter
    def IsRequired(self, value):
        self._set_attribute('isRequired', value)

    @property
    def Name(self):
        """Name of packet field

        Returns:
            str
        """
        return self._get_attribute('name')
    @Name.setter
    def Name(self, value):
        self._set_attribute('name', value)

    def update(self, Description=None, IsEditable=None, IsEnabled=None, IsRequired=None, Name=None):
        """Updates a child instance of instructions on the server.

        Args:
            Description (str): Description of the field.
            IsEditable (bool): Information on the requirement of the field.
            IsEnabled (bool): Enables disables the field.
            IsRequired (bool): Information on the requirement of the field.
            Name (str): Name of packet field

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def AddInstruction(self, *args, **kwargs):
        """Executes the addInstruction operation on the server.

        Adds Instruction item in profile.

        addInstruction(Arg2:string)
            Args:
                args[0] is Arg2 (str): 

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('addInstruction', payload=payload, response_object=None)
