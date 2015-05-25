import os
import dbus.service

from coalib.output.dbus.DbusApp import DbusApp


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
