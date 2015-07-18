import os
import dbus.service

from coalib.output.dbus.DbusApp import DbusApp


class DbusServer(dbus.service.Object):
    interface = "org.coala_analyzer.v1"

    def __init__(self, bus, path, on_disconnected=None):
        """
        Creates a new DbusServer class which handles the dynamic creation and
        disposal of dbus object-paths for documents and also handles
        information about DbusApplication.

        :param bus:             The dbus bus to which to connect this object
                                path to.
        :param path:            The path in the dbus bus using which apps can
                                communicate.
        :param on_disconnected: This function will be called when the DbusServer
                                has no more applications connected to it.
        """
        dbus.service.Object.__init__(self, bus, path)

        self.apps = {}
        self.__next_app_id = 0
        self.on_disconnected = on_disconnected

        bus.add_signal_receiver(self._on_name_lost,
                                signal_name='NameOwnerChanged',
                                dbus_interface=None,
                                path=None)

    @dbus.service.method(interface,
                         in_signature="s",
                         out_signature="o",
                         sender_keyword="sender")
    def CreateDocument(self, path, sender=None):
        """
        Creates a DbusDocument if it doesn't exist.

        :param path:   The path to the document.
        :param sender: The client who created the dbus request - this is used
                       as the DbusApp's name.
        :return:       a DbusDocument object.
        """
        app = self.get_or_create_app(sender)
        doc = self.get_or_create_document(app, path)
        return doc._object_path

    @dbus.service.method(interface,
                         in_signature="s",
                         out_signature="",
                         sender_keyword="sender")
    def DisposeDocument(self, path, sender=None):
        """
        Disposes a DbusDocument if it exists. Fails silently if it does not
        exist.

        :param path:   The path to the document.
        :param sender: The client who created the dbus request - this is used
                       as the DbusApp's name to search for the document in.
        """
        path = os.path.normpath(path)

        try:
            app = self.apps[sender]
        except KeyError:
            return

        self.dispose_document(app, path)

    def _on_name_lost(self, name, oldowner, newowner):
        if newowner != '':
            return

        self.dispose_app(oldowner)

    def _next_app_id(self):
        self.__next_app_id += 1
        return self.__next_app_id

    def create_app(self, appname):
        """
        Create a new dbus app with the given appname.

        :param appname: The name of the app to be created.
        :return:        a DbusApp object.
        """
        self.apps[appname] = DbusApp(self._next_app_id(), appname)
        return self.apps[appname]

    def get_or_create_app(self, appname):
        """
        Get the dbus app with the given appname. If there does not exist any
        app with the given name, a new app is created and returned.

        :param appname: The name of the app to be created.
        :return:        A DbusApp object.
        """
        try:
            return self.apps[appname]
        except KeyError:
            return self.create_app(appname)

    def dispose_app(self, appname):
        """
        Dispose of the app with the given name. It fails silently if the app
        does not exist. If there are no more apps connected to the server, it
        calls the on_disconnected callback.

        :param appname: The name of the app to dispose of.
        """
        try:
            self.apps.pop(appname)
            if len(self.apps) == 0 and self.on_disconnected:
                self.on_disconnected()
        except KeyError:
            pass

    def create_document(self, app, path):
        """
        Create a new dbus document.

        :param app:  The DbusApp the document is related to.
        :param path: The path to the document to be created.
        :return:     a DbusDocument object.
        """
        doc = app.create_document(path)
        objpath = (self._object_path + "/" + str(app.app_id) +
                   "/documents/" + str(doc.doc_id))
        doc.add_to_connection(self._connection, objpath)

        return doc

    def get_or_create_document(self, app, path):
        """
        Get the dbus document with the given path. If there does not exist any
        document under the DbusApp with the given path, a new document is
        created and returned.

        :param app:  The DbusApp the document is under.
        :param path: The path to the document to be created.
        :return:     A DbusApp object.
        """
        path = os.path.abspath(os.path.expanduser(path))
        try:
            doc = app.docs[path]
        except KeyError:
            doc = self.create_document(app, path)

        return doc

    def dispose_document(self, app, path):
        """
        Dispose of the document with the given path. It fails silently if the
        document does not exist. If there are no more documents in the app,
        the app is disposed.

        :param app:  The DbusApp the document is under.
        :param path: The path to the document.
        """
        doc = app.dispose_document(path)
        if doc != None:
            doc.remove_from_connection()
            if len(app.docs) == 0:
                self.dispose_app(app.name)
