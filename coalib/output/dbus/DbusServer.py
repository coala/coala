import os
import dbus.service

from coalib.output.dbus.DbusApp import DbusApp
from coalib.output.dbus.DbusDocument import DbusDocument


class DbusServer(dbus.service.Object):
    """
        Handles the dynamic creation and disposal of dbus object-paths for
        documents  and also handles information about the DbusApplication of
        the document.
    """
    def __init__(self, bus, path, callback=None):
        """
        :param bus:      The dbus bus to which to connect this object path to
        :param path:     The path in the dbus bus using which apps can
                         communicate
        :param callback: The function which will be called when the DbusServer
                         has no more applications connected to it.
        """
        super(DbusServer, self).__init__(bus, path)

        self.apps = {}
        self.next_app_id = 0
        self.callback = callback

        bus.add_signal_receiver(self._on_name_lost,
                                signal_name='NameOwnerChanged',
                                dbus_interface='org.freedesktop.DBus',
                                path='/org/freedesktop/DBus')

    def _on_name_lost(self, name, oldowner, newowner):
        if newowner != '':
            return

        self.dispose_app(oldowner)

    def create_app(self, appname):
        app = DbusApp(self.next_app_id, appname)
        self.apps[appname] = app
        self.next_app_id += 1
        return app

    def get_or_create_app(self, appname):
        try:
            return self.apps[appname]
        except KeyError:
            return self.create_app(appname)

    def dispose_app(self, appname):
        try:
            self.apps.pop(appname)
        except KeyError:
            pass

        if len(self.apps) == 0 and self.callback:
            self.callback()

    def create_document(self, app, path):
        doc = DbusDocument()

        doc.id = app.next_doc_id
        doc.path = path
        app.next_doc_id += 1
        app.docs[path] = doc
        objpath = self._object_path + "/" + str(app.id) + \
                  "/documents/" + str(doc.id)

        doc.add_to_connection(self._connection, objpath)
        return doc

    def get_or_create_document(self, app, path):
        npath = (path and os.path.normpath(path))
        try:
            doc = app.docs[npath]
        except KeyError:
            doc = self.create_document(app, npath)
        doc.path = path

        return doc

    def dispose_document(self, app, path):
        try:
            app.docs[path].remove_from_connection()
            app.docs.pop(path)
        except KeyError:
            pass

        if len(app.docs) == 0:
            self.dispose_app(app.name)
