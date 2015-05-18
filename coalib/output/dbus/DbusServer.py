import os
import sys
import dbus.service
from gi.repository import GLib

from coalib.output.dbus.DbusDocument import DbusDocument
from coalib.output.dbus.DbusApp import DbusApp


class DbusServer(dbus.service.Object):
    """
        Handles the dynamic creation and disposal of dbus object-paths for
        documents  and also handles information about the DbusApplication of
        the document.
    """
    interface = "org.coala.v1"

    def __init__(self, bus, path):
        super(DbusServer, self).__init__(bus, path)
        self.apps = {}
        self.next_app_id = 0

        bus.add_signal_receiver(self.on_name_lost,
                                signal_name='NameOwnerChanged',
                                dbus_interface='org.freedesktop.DBus',
                                path='/org/freedesktop/DBus')

    @dbus.service.method(interface,
                         in_signature="s",
                         out_signature="o",
                         sender_keyword="sender")
    def CreateDocument(self, path, sender=None):
        app = self.ensure_app(sender)
        doc = self.ensure_document(app, path)
        return doc._object_path

    @dbus.service.method(interface,
                         in_signature="s",
                         out_signature="",
                         sender_keyword="sender")
    def DisposeDocument(self, path, sender=None):
        path = os.path.normpath(path)

        try:
            app = self.apps[sender]
        except KeyError:
            return

        self.dispose_document(app, path)

    def on_name_lost(self, name, oldowner, newowner):
        if newowner != '':
            return

        try:
            app = self.apps[oldowner]
        except KeyError:
            return

        self.dispose_app(app)

    def make_app(self, appname):
        app = DbusApp(self.next_app_id, appname)
        self.apps[appname] = app
        self.next_app_id += 1
        return app

    def ensure_app(self, appname):
        try:
            return self.apps[appname]
        except KeyError:
            return self.make_app(appname)

    def make_document(self, app, path):
        doc = DbusDocument()

        doc.id = app.next_doc_id
        doc.path = path
        app.next_doc_id += 1
        app.docs[path] = doc
        objpath = self._object_path + "/" + str(app.id) + \
                  "/documents/" + str(doc.id)

        doc.add_to_connection(self._connection, objpath)
        return doc

    def ensure_document(self, app, path):
        npath = (path and os.path.normpath(path))
        try:
            doc = app.docs[npath]
        except KeyError:
            doc = self.make_document(app, npath)
        doc.path = path

        return doc

    def dispose_app(self, app):
        for doc in app.docs:
            self.dispose_document(app, app.docs[doc])
        self.apps.pop(app.name)

        if len(self.apps) == 0:
            GLib.idle_add(lambda: sys.exit(0))

    def dispose_document(self, app, path):
        app.docs[path].remove_from_connection()
        app.docs.pop(path)

    def dispose(self, app, path):
        doc = app.docs[path]

        self.dispose_document(app, doc)

        if len(app.docs) == 0:
            self.dispose_app(app)
