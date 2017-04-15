import sys
import os
import unittest
import subprocess
import dbus
import dbus.mainloop

sys.path.insert(0, ".")
from coalib.output.dbus.DbusDocument import DbusDocument


class DbusDocumentTest(unittest.TestCase):
    def setUp(self):
        self.session_bus = dbus.SessionBus(
                                mainloop=dbus.mainloop.NULL_MAIN_LOOP)
        self.dbus_name = dbus.service.BusName("org.coala.v1.test",
                                                self.session_bus)

    def test_path(self):
        test_file = "a"
        uut = DbusDocument()
        self.assertEqual(uut.path, "")

        uut = DbusDocument(test_file)
        self.assertEqual(uut.path, os.path.abspath(test_file))

        uut.path = "/"
        self.assertEqual(uut.path, "/")


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
