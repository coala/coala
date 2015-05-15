import os
import dbus.service


class DbusDocument(dbus.service.Object):
    """
    This is a dbus object-path for every document that a DbusApplication wants
    coala to analyze.
    """
    interface = "org.coala.v1"

    def __init__(self, path=""):
        super(DbusDocument, self).__init__()
        if path:
            abs_path = os.path.abspath(path)
            self._path = abs_path
        else:
            self._path = ""

    @dbus.service.method(interface,
                         in_signature="",
                         out_signature="")
    def Analyze(self):
        """
        This method analyzes the document and sends back the result
        """
        pass

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        new_abs_path = os.path.abspath(new_path)
        self._path = new_abs_path
