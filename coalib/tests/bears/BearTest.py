import sys
import multiprocessing

sys.path.insert(0, ".")
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.processes.communication.LogMessage import LogMessage
from coalib.misc.i18n import _
from coalib.bears.Bear import Bear
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
import unittest


class TestBear(Bear):
    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    def run(self):
        self.print("set", "up", delimiter="=")
        self.warn(_("A string to test translations."))
        self.err("teardown")
        self.err()

    @staticmethod
    def get_dependencies():
        return [BadTestBear]


class BadTestBear(Bear):
    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    def run(self):
        raise NotImplementedError


class TypedTestBear(Bear):
    def run(self, something: int):
        return []


class BearTest(unittest.TestCase):
    def setUp(self):
        self.queue = multiprocessing.Queue()
        self.settings = Section("test_settings")
        self.uut = TestBear(self.settings, self.queue)

    def test_simple_api(self):
        self.assertRaises(TypeError, TestBear, self.settings, 2)
        self.assertRaises(TypeError, TestBear, None, self.queue)
        self.assertRaises(NotImplementedError, self.uut.kind)

        base = Bear(self.settings, None)
        self.assertRaises(NotImplementedError, base.run)
        self.assertEqual(base.get_non_optional_settings(), {})

    def test_message_queue(self):
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG,
                           _("Running bear {}...").format("TestBear"))
        self.check_message(LOG_LEVEL.DEBUG, "set=up")
        self.check_message(LOG_LEVEL.WARNING,
                           _("A string to test translations."))
        self.check_message(LOG_LEVEL.ERROR, "teardown")

    def test_bad_bear(self):
        self.uut = BadTestBear(self.settings, self.queue)
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.WARNING,
                           _("Bear {} failed to run. Take a look at debug "
                             "messages for further "
                             "information.").format("BadTestBear"))
        # debug message contains custom content, dont test this here
        self.queue.get()

    def test_inconvertible(self):
        self.uut = TypedTestBear(self.settings, self.queue)
        self.settings.append(Setting("something", "5"))
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)

        self.settings.append(Setting("something", "nonsense"))
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.WARNING)

    def check_message(self, log_level, message=None):
        msg = self.queue.get()
        self.assertIsInstance(msg, LogMessage)
        if message:
            self.assertEqual(msg.message, message)

        self.assertEqual(msg.log_level, log_level, msg)

    def test_no_queue(self):
        uut = TestBear(self.settings, None)
        uut.execute()  # No exceptions

    def test_dependencies(self):
        self.assertEqual(Bear.get_dependencies(), [])
        self.assertEqual(Bear.missing_dependencies([]), [])
        self.assertEqual(Bear.missing_dependencies([BadTestBear]), [])

        self.assertEqual(TestBear.missing_dependencies([]), [BadTestBear])
        self.assertEqual(TestBear.missing_dependencies([BadTestBear]), [])
        self.assertEqual(TestBear.missing_dependencies([TestBear]),
                         [BadTestBear])
        self.assertEqual(TestBear.missing_dependencies([TestBear,
                                                        BadTestBear]),
                         [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
