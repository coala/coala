import os

from coalib.output.dbus.DbusDocument import DbusDocument


class DbusApp:
    """
    Stores data about each client that connects to the DbusServer
    """

    def __init__(self, app_id, name=""):
        self.app_id = app_id
        self.name = name

        self.docs = {}
        self.__next_doc_id = 0

    def _next_doc_id(self):
        self.__next_doc_id += 1
        return self.__next_doc_id

    def create_document(self, path):
        """
        Create a new dbus document.

        :param path:        The path to the document to be created.
        :param object_path: The dbus object path to use as the base for the
                            document object path.
        :param object_path: The connection to which the new ddocument object
                            path should be added.
        :return:            a DbusDocument object.
        """
        path = os.path.abspath(os.path.expanduser(path))
        doc = DbusDocument(doc_id=self._next_doc_id(), path=path)
        self.docs[path] = doc

        return doc

    def dispose_document(self, path):
        """
        Dispose of the document with the given path. It fails silently if the
        document does not exist. If there are no more documents in the app,
        the app is disposed.

        :param path: The path to the document.
        """
        path = os.path.abspath(os.path.expanduser(path))
        try:
            return self.docs.pop(path)
        except KeyError:
            return None
