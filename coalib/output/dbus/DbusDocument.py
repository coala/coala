import os
import dbus.service


class DbusDocument(dbus.service.Object):
    def __init__(self, path=""):
        """
        Creates a new dbus object-path for every document that a
        DbusApplication wants coala to analyze. It stores the information
        (path) of the document and the config_file to use when analyzing the
        given document.

        :param path: The path to the document.
        """
        dbus.service.Object.__init__(self)

        self.config_file = ""
        self.path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        if new_path:
            new_path = os.path.abspath(os.path.expanduser(new_path))
        self._path = new_path
