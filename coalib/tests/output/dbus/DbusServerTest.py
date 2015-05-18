#!/usr/bin/env python3

import sys
import os
import inspect
import unittest
import subprocess
import time
from gi.repository import GLib
try:
    import dbus
    import dbus.mainloop.glib
except ImportError:
    pass

sys.path.insert(0, ".")
from coalib.output.dbus.DbusServer import DbusServer


def create_mainloop():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    # The BusName needs to be saved to a variable, if it is not saved - the
    # Bus will be closed.
    dbus_name = dbus.service.BusName("org.coala.v1.test", session_bus)
    dbus_server = DbusServer(session_bus, '/org/coala/v1/test')

    mainloop = GLib.MainLoop()
    mainloop.run()


class DbusServerTest(unittest.TestCase):
    def setUp(self):
        self.test_file_path = '/path/to/file'

        try:
            self.connect_to_test_server()
        except dbus.exceptions.DBusException as exception:
            if exception.get_dbus_name() == \
                "org.freedesktop.DBus.Error.ServiceUnknown":
                self.make_test_server()
                # Wait for the server to become available
                time.sleep(2)
                self.connect_to_test_server()
            else:
                raise(exception)
        return

    def make_test_server(self):
        # Make a dbus service in a new process. It cannot be in this process
        # as that gives SegmentationFaults because the same bus is being used.
        env = os.environ.copy()
        self.subprocess = subprocess.Popen(
            ['python3', __file__, 'server'], env=env)

    def connect_to_test_server(self):
        self.bus = dbus.SessionBus()
        self.remote_object = self.bus.get_object("org.coala.v1.test",
                                                 "/org/coala/v1/test")

    def test_dbus(self):
        self.document_object_path = self.remote_object.CreateDocument(
            self.test_file_path,
            dbus_interface="org.coala.v1")

        self.assertRegex(str(self.document_object_path),
            "^/org/coala/v1/test/\d+/documents/\d+$")

        self.remote_object.DisposeDocument(
            self.test_file_path,
            dbus_interface="org.coala.v1")

    def tearDown(self):
        self.subprocess.kill()


def skip_test():
    try:
        subprocess.Popen(['dbus-daemon --version'])
        return False
    except OSError:
        return "dbus is not installed."


if __name__ == '__main__':
    arg = ""
    if len(sys.argv) > 1:
        arg = sys.argv[1]

    if arg == "server":
        create_mainloop()
    else:
        unittest.main(verbosity=2)
