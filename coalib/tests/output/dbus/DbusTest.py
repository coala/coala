import sys
import os
import unittest
from unittest.case import skipIf
import subprocess
import time

from coalib.misc import Constants

try:
    import dbus
    # Needed to determine if test needs skipping
    from gi.repository import GLib

    skip, message = False, ''
except ImportError as err:
    skip, message = True, str(err)


def make_test_server():
    # Make a dbus service in a new process. It cannot be in this process
    # as that gives SegmentationFaults because the same bus is being used.

    # For some reason this also fails on some systems if moved to another file
    return subprocess.Popen([
        sys.executable,
        '-c',
        """
import sys
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
from coalib.output.dbus.DbusServer import DbusServer
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
session_bus = dbus.SessionBus()
dbus_name = dbus.service.BusName("org.coala_analyzer.v1.test", session_bus)
dbus_server = DbusServer(session_bus, "/org/coala_analyzer/v1/test",
                         on_disconnected=lambda: GLib.idle_add(sys.exit))
mainloop = GLib.MainLoop()
mainloop.run()
"""])


@skipIf(skip, message)
class DbusTest(unittest.TestCase):

    def setUp(self):
        self.config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         "dbus_test_files",
                         ".coafile"))
        self.testcode_c_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         "dbus_test_files",
                         "testcode.c"))

        self.subprocess = make_test_server()
        trials_left = 10

        while trials_left > 0:
            time.sleep(0.1)
            trials_left = trials_left - 1
            try:
                self.connect_to_test_server()
                continue
            except dbus.exceptions.DBusException as exception:
                if trials_left == 0:
                    raise exception

    def connect_to_test_server(self):
        self.bus = dbus.SessionBus()
        self.remote_object = self.bus.get_object("org.coala_analyzer.v1.test",
                                                 "/org/coala_analyzer/v1/test")

    def test_dbus(self):
        self.document_object_path = self.remote_object.CreateDocument(
            self.testcode_c_path,
            dbus_interface="org.coala_analyzer.v1")

        self.assertRegex(str(self.document_object_path),
                         r"^/org/coala_analyzer/v1/test/\d+/documents/\d+$")

        self.document_object = self.bus.get_object(
            "org.coala_analyzer.v1.test",
            self.document_object_path)

        config_file = self.document_object.SetConfigFile(
            "dummy_config",
            dbus_interface="org.coala_analyzer.v1")
        self.assertEqual(config_file, "dummy_config")

        config_file = self.document_object.GetConfigFile(
            dbus_interface="org.coala_analyzer.v1")
        self.assertEqual(config_file, "dummy_config")

        config_file = self.document_object.FindConfigFile(
            dbus_interface="org.coala_analyzer.v1")
        self.assertEqual(config_file, self.config_path)

        analysis = self.document_object.Analyze(
            dbus_interface="org.coala_analyzer.v1")
        self.maxDiff = None
        self.assertEqual(analysis,
                         (1,
                          [],
                          [('default',
                            True,
                            [{'debug_msg': '',
                              'file': '',
                              'id': analysis[2][0][2][0]['id'],
                              'line_nr': "",
                              'message': 'test msg',
                              'origin': 'LocalTestBear',
                              'severity': 'NORMAL'},
                             {'debug_msg': '',
                              'file': self.testcode_c_path,
                              'id': analysis[2][0][2][1]['id'],
                              'line_nr': "",
                              'message': 'test msg',
                              'origin': 'GlobalTestBear',
                              'severity': 'NORMAL'}])]))

        config_file = self.document_object.SetConfigFile(
            self.config_path + "2",
            dbus_interface="org.coala_analyzer.v1")
        analysis = self.document_object.Analyze(
            dbus_interface="org.coala_analyzer.v1")
        self.assertEqual(analysis[0], 255)
        self.assertEqual(analysis[1][1]["log_level"], "ERROR")
        self.assertEqual(analysis[1][1]["message"], Constants.CRASH_MESSAGE)

        # Skip file if file pattern doesn't match
        # Also test if 2 documents can be opened simultaneously
        self.document_object_path = self.remote_object.CreateDocument(
            "test.unknown_ext",
            dbus_interface="org.coala_analyzer.v1")
        self.document_object = self.bus.get_object(
            "org.coala_analyzer.v1.test",
            self.document_object_path)
        config_file = self.document_object.SetConfigFile(
            self.config_path,
            dbus_interface="org.coala_analyzer.v1")
        analysis = self.document_object.Analyze(
            dbus_interface="org.coala_analyzer.v1")
        self.assertEqual(analysis, (0, [], []))

        self.remote_object.DisposeDocument(
            self.testcode_c_path,
            dbus_interface="org.coala_analyzer.v1")

        self.remote_object.DisposeDocument(
            "test.unknown_ext",
            dbus_interface="org.coala_analyzer.v1")

    def tearDown(self):
        if self.subprocess:
            self.subprocess.kill()


if __name__ == "__main__" and not skip:
    unittest.main(verbosity=2)
