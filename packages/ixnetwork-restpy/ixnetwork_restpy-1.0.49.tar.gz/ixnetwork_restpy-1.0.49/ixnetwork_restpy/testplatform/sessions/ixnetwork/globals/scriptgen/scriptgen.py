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


class Scriptgen(Base):
    """Container for scriptgen options
    The Scriptgen class encapsulates a required scriptgen resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'scriptgen'

    def __init__(self, parent):
        super(Scriptgen, self).__init__(parent)

    @property
    def Base64CodeOptions(self):
        """An instance of the Base64CodeOptions class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.base64codeoptions.base64codeoptions.Base64CodeOptions)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.base64codeoptions.base64codeoptions import Base64CodeOptions
        return Base64CodeOptions(self)._select()

    @property
    def IxNetCodeOptions(self):
        """An instance of the IxNetCodeOptions class.

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.ixnetcodeoptions.ixnetcodeoptions.IxNetCodeOptions)

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.ixnetcodeoptions.ixnetcodeoptions import IxNetCodeOptions
        return IxNetCodeOptions(self)._select()

    @property
    def ConnectHostname(self):
        """The hostname to be used in the connect command

        Returns:
            str
        """
        return self._get_attribute('connectHostname')
    @ConnectHostname.setter
    def ConnectHostname(self, value):
        self._set_attribute('connectHostname', value)

    @property
    def ConnectPort(self):
        """The port number to be used in the connect command

        Returns:
            number
        """
        return self._get_attribute('connectPort')
    @ConnectPort.setter
    def ConnectPort(self, value):
        self._set_attribute('connectPort', value)

    @property
    def ConnectVersion(self):
        """The version number to be used in the connect command

        Returns:
            str
        """
        return self._get_attribute('connectVersion')
    @ConnectVersion.setter
    def ConnectVersion(self, value):
        self._set_attribute('connectVersion', value)

    @property
    def IncludeConnect(self):
        """Flag to include the connect command

        Returns:
            bool
        """
        return self._get_attribute('includeConnect')
    @IncludeConnect.setter
    def IncludeConnect(self, value):
        self._set_attribute('includeConnect', value)

    @property
    def IncludeTestComposer(self):
        """Flag to include test composer code

        Returns:
            bool
        """
        return self._get_attribute('includeTestComposer')
    @IncludeTestComposer.setter
    def IncludeTestComposer(self, value):
        self._set_attribute('includeTestComposer', value)

    @property
    def Language(self):
        """Select the target scriptgen language

        Returns:
            str(perl|python|ruby|tcl)
        """
        return self._get_attribute('language')
    @Language.setter
    def Language(self, value):
        self._set_attribute('language', value)

    @property
    def LinePerAttribute(self):
        """If true the scriptgen output will show each attribute on a separate line

        Returns:
            bool
        """
        return self._get_attribute('linePerAttribute')
    @LinePerAttribute.setter
    def LinePerAttribute(self, value):
        self._set_attribute('linePerAttribute', value)

    @property
    def OverwriteScriptFilename(self):
        """If true the file indicated by the script filename will be overwritten

        Returns:
            bool
        """
        return self._get_attribute('overwriteScriptFilename')
    @OverwriteScriptFilename.setter
    def OverwriteScriptFilename(self, value):
        self._set_attribute('overwriteScriptFilename', value)

    @property
    def ScriptFilename(self):
        """The name of the target scriptgen file

        Returns:
            str
        """
        return self._get_attribute('scriptFilename')
    @ScriptFilename.setter
    def ScriptFilename(self, value):
        self._set_attribute('scriptFilename', value)

    @property
    def SerializationType(self):
        """The scriptgen serialization type

        Returns:
            str(base64|ixNet)
        """
        return self._get_attribute('serializationType')
    @SerializationType.setter
    def SerializationType(self, value):
        self._set_attribute('serializationType', value)

    def update(self, ConnectHostname=None, ConnectPort=None, ConnectVersion=None, IncludeConnect=None, IncludeTestComposer=None, Language=None, LinePerAttribute=None, OverwriteScriptFilename=None, ScriptFilename=None, SerializationType=None):
        """Updates a child instance of scriptgen on the server.

        Args:
            ConnectHostname (str): The hostname to be used in the connect command
            ConnectPort (number): The port number to be used in the connect command
            ConnectVersion (str): The version number to be used in the connect command
            IncludeConnect (bool): Flag to include the connect command
            IncludeTestComposer (bool): Flag to include test composer code
            Language (str(perl|python|ruby|tcl)): Select the target scriptgen language
            LinePerAttribute (bool): If true the scriptgen output will show each attribute on a separate line
            OverwriteScriptFilename (bool): If true the file indicated by the script filename will be overwritten
            ScriptFilename (str): The name of the target scriptgen file
            SerializationType (str(base64|ixNet)): The scriptgen serialization type

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        self._update(locals())

    def Generate(self, *args, **kwargs):
        """Executes the generate operation on the server.

        Generate a script of the currently loaded configuration using the options in the /globals/scriptgen hierarchy.

        The IxNetwork modeling infrastructure allows for multiple method Signatures with the same name while python does not.
        The following correlates the modeling Signatures to the python *args variable length list:

        generate()

        generate(Arg2:href)
            Args:
                args[0] is Arg2 (obj(ixnetwork_restpy.files.Files)): A valid writeTo file handle the script will be written to.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self.href }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('generate', payload=payload, response_object=None)
