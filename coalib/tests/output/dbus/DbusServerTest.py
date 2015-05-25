import sys
import os
import unittest
import subprocess
import dbus
import dbus.mainloop

sys.path.insert(0, ".")
from coalib.output.dbus.DbusServer import DbusServer


class DbusDocument(dbus.service.Object):
    def __init__(self, id=-1, path=""):
        super(DbusDocument, self).__init__()
        self.path = path
        self.id = id


class TestException(Exception):
    pass


class DbusServerTest(unittest.TestCase):
    def setUp(self):
        self.session_bus = dbus.SessionBus(
                                mainloop=dbus.mainloop.NULL_MAIN_LOOP)
        self.dbus_name = dbus.service.BusName("org.coala.v1.test",
                                                self.session_bus)

    def test_apps(self):
        uut = DbusServer(self.session_bus, "/org/coala/v1/test_apps")

        uut.ensure_app("app1")
        self.assertEqual(len(uut.apps), 1)
        self.assertIn("app1", uut.apps)

        uut.ensure_app("app1")
        self.assertIn("app1", uut.apps)

        uut.dispose_app(uut.apps["app1"])
        self.assertNotIn("app1", uut.apps)

    @staticmethod
    def callback1():
        raise TestException()

    def test_callback(self):
        test_output = 0
        uut = DbusServer(self.session_bus, "/org/coala/v1/test_callback",
            callback=DbusServerTest.callback1)
        uut.make_app("app1")
        self.assertRaises(TestException, uut.dispose_app, uut.apps["app1"])


def skip_test():
    try:
        with open(os.devnull, "w") as devnull:
            subprocess.Popen(["dbus-daemon", "--version"],
                             stdout=devnull)
        return False
    except OSError:
        return "dbus is not installed."


if __name__ == "__main__":
    unittest.main(verbosity=2)
