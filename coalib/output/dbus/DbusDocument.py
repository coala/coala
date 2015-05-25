import os
import dbus.service


class DbusDocument(dbus.service.Object):
    """
    This is a dbus object-path for every document that a DbusApplication wants
    coala to analyze. It stores the information (path) of the document and the
    config_file to use when analyzing the given document.
    """
    interface = "org.coala.v1"

    def __init__(self, path=""):
        super(DbusDocument, self).__init__()
        self.config_file = ""
        if path:
            self._path = os.path.abspath(os.path.expanduser(path))
        else:
            self._path = ""

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        new_abs_path = os.path.abspath(os.path.expanduser(new_path))
        self._path = new_abs_path
