import os
import dbus.service

from coalib.output.dbus.DbusApp import DbusApp


class DbusServer(dbus.service.Object):
    """
        Handles the dynamic creation and disposal of dbus object-paths for
        documents  and also handles information about the DbusApplication of
        the document.
    """
    interface = "org.coala.v1"

    def __init__(self, bus, path, callback=None):
        super(DbusServer, self).__init__(bus, path)
        self.apps = {}
        self.next_app_id = 0
        self.callback = callback

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

    def dispose_app(self, app):
        self.apps.pop(app.name)

        if len(self.apps) == 0 and self.callback:
            self.callback()
