import unittest
from unittest.case import SkipTest

try:
    from coalib import coala_dbus
    from gi.repository import GLib
except ImportError:
    raise SkipTest("python-gi or python-dbus not installed")


class GlibMainLoopTest:

    @staticmethod
    def run():
        raise AssertionError


class coalaDbusTest(unittest.TestCase):

    def setUp(self):
        self.glib_main_loop = GLib.MainLoop
        GLib.MainLoop = GlibMainLoopTest

    def tearDown(self):
        GLib.MainLoop = self.glib_main_loop

    def test_main(self):
        # Ensure we are able to setup dbus and create a mainloop
        with self.assertRaises(AssertionError):
            coala_dbus.main()

        with self.assertRaises(SystemExit):
            coala_dbus.sys_clean_exit()

        self.assertGreater(coala_dbus.on_disconnected(), 0)
