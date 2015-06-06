import os
import dbus.service

from coalib.output.dbus.DbusApp import DbusApp


class DbusServer(dbus.service.Object):
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
        super(DbusServer, self).__init__(bus, path)

        self.apps = {}
        self.next_app_id = 0
        self.callback = on_disconnected

        bus.add_signal_receiver(self._on_name_lost,
                                signal_name='NameOwnerChanged',
                                dbus_interface='org.freedesktop.DBus',
                                path='/org/freedesktop/DBus')

    def _on_name_lost(self, name, oldowner, newowner):
        if newowner != '':
            return

        self.dispose_app(oldowner)

    def _next_app_id(self):
        self.next_app_id += 1
        return self.next_app_id-1

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
        except KeyError:
            pass

        if len(self.apps) == 0 and self.callback:
            self.callback()
