import sys

sys.path.insert(0, ".")
import multiprocessing

from coalib.settings.Section import Section
from coalib.processes.communication.LogMessage import LogMessage
from coalib.misc.i18n import _
from coalib.bears.Bear import Bear
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
import unittest


class TestBear(Bear):
    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    def set_up(self):
        self.debug_msg("set", "up", delimiter="=")

    def tear_down(self):
        self.fail_msg("teardown")
        self.fail_msg()

    def run_bear(self):
        self.warn_msg(_("A string to test translations."))


class BadTestBear(Bear):
    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    def tear_down(self):
        raise NotImplementedError

    def run_bear(self):
        pass


class BearTestCase(unittest.TestCase):
    def setUp(self):
        self.queue = multiprocessing.Queue()
        self.settings = Section("test_settings")
        self.uut = TestBear(self.settings, self.queue)

    def test_raises(self):
        self.assertRaises(TypeError, TestBear, self.settings, 2)
        self.assertRaises(TypeError, TestBear, None, self.queue)
        self.assertRaises(NotImplementedError, self.uut.kind)

    def test_methods_available(self):
        # these should be available and not throw anything
        base = Bear(self.settings, None)
        print("XXXXXXXXXXXXXXXXXXXXX:", type(base), isinstance(base, Bear))

        base.set_up()
        base.tear_down()

        self.assertRaises(NotImplementedError, base.run_bear)

        self.assertEqual(base.get_non_optional_settings(), {})

    def test_message_queue(self):
        self.uut.run()
        self.check_message(LOG_LEVEL.DEBUG, _("Setting up bear {}...").format("TestBear"))
        self.check_message(LOG_LEVEL.DEBUG, "set=up")
        self.check_message(LOG_LEVEL.DEBUG, _("Running bear {}...").format("TestBear"))
        self.check_message(LOG_LEVEL.WARNING, _("A string to test translations."))
        self.check_message(LOG_LEVEL.DEBUG, _("Tearing down bear {}...").format("TestBear"))
        self.check_message(LOG_LEVEL.ERROR, "teardown")

    def test_bad_bear(self):
        self.uut = BadTestBear(self.settings, self.queue)
        self.uut.run()
        self.check_message(LOG_LEVEL.DEBUG, _("Setting up bear {}...").format("BadTestBear"))
        self.check_message(LOG_LEVEL.DEBUG, _("Running bear {}...").format("BadTestBear"))
        self.check_message(LOG_LEVEL.DEBUG, _("Tearing down bear {}...").format("BadTestBear"))
        self.check_message(LOG_LEVEL.WARNING, _("Bear {} failed to run").format("BadTestBear"))
        self.queue.get()  # debug message contains custom content, dont test this here

    def check_message(self, log_level, message):
        msg = self.queue.get()
        self.assertIsInstance(msg, LogMessage)
        self.assertEqual(msg.message, message)
        self.assertEqual(msg.log_level, log_level)

    def test_no_queue(self):
        uut = TestBear(self.settings, None)
        uut.run()  # No exceptions


if __name__ == '__main__':
    unittest.main(verbosity=2)
