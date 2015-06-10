import os
import dbus.service

from coalib.settings.ConfigurationGathering import find_user_config


class DbusDocument(dbus.service.Object):
    interface = "org.coala.v1"

    def __init__(self, id, path=""):
        """
        Creates a new dbus object-path for every document that a
        DbusApplication wants coala to analyze. It stores the information
        (path) of the document and the config file to use when analyzing the
        given document.

        :param id:   An id for the document.
        :param path: The path to the document.
        """
        dbus.service.Object.__init__(self)

        self.config_file = ""
        self.path = path
        self.id = id

    @dbus.service.method(interface,
                         in_signature="",
                         out_signature="s")
    def FindConfigFile(self):
        """
        This method uses the path of the document to identify a user config
        file for it

        :return: The config file path
        """
        self.config_file = find_user_config(self.path)
        return self.config_file

    @dbus.service.method(interface,
                         in_signature="s",
                         out_signature="s")
    def SetConfigFile(self, config_file):
        """
        This method sets the config file to use. It has to be an absolute path,
        as otherwise it is difficult to find it.

        :param config_file: The path fo the config file to use. This has to be
                            an absolute path
        :return:            The config path which has been used
        """
        self.config_file = config_file
        return self.config_file

    @dbus.service.method(interface,
                         in_signature="",
                         out_signature="s")
    def GetConfigFile(self):
        """
        This method gets the config file which is being used

        :return: The config path which is being used
        """
        return self.config_file

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        if new_path:
            new_path = os.path.abspath(os.path.expanduser(new_path))
        self._path = new_path
