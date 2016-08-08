import multiprocessing
import unittest
from os.path import abspath

from coalib.bears.Bear import Bear
from coalib.results.Result import Result
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.processes.communication.LogMessage import LogMessage
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class BadTestBear(Bear):

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    def run(self):
        raise NotImplementedError


class TestBear(Bear):

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    def run(self):
        self.print("set", "up", delimiter="=")
        self.err("teardown")
        self.err()

    @staticmethod
    def get_dependencies():
        return [BadTestBear]


class TypedTestBear(Bear):

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)
        self.was_executed = False

    def run(self, something: int):
        self.was_executed = True
        return []


class BearWithPrerequisites(Bear):
    prerequisites_fulfilled = True

    def __init__(self, section, queue, prerequisites_fulfilled):
        BearWithPrerequisites.prerequisites_fulfilled = prerequisites_fulfilled
        Bear.__init__(self, section, queue)
        self.was_executed = False

    def run(self):
        self.was_executed = True
        return []

    @classmethod
    def check_prerequisites(cls):
        return cls.prerequisites_fulfilled


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
                           "Running bear TestBear...")
        self.check_message(LOG_LEVEL.DEBUG, "set=up")
        self.check_message(LOG_LEVEL.ERROR, "teardown")

    def test_bad_bear(self):
        self.uut = BadTestBear(self.settings, self.queue)
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.WARNING,
                           "Bear BadTestBear failed to run. Take a look at "
                           "debug messages (`-L DEBUG`) for further "
                           "information.")
        # debug message contains custom content, dont test this here
        self.queue.get()

    def test_inconvertible(self):
        self.uut = TypedTestBear(self.settings, self.queue)
        self.settings.append(Setting("something", "5"))
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.assertTrue(self.uut.was_executed)

        self.settings.append(Setting("something", "nonsense"))
        self.uut.was_executed = False
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.WARNING)
        self.assertTrue(self.queue.empty())
        self.assertFalse(self.uut.was_executed)

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

    def test_check_prerequisites(self):
        uut = BearWithPrerequisites(self.settings, self.queue, True)
        uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.assertTrue(self.queue.empty())
        self.assertTrue(uut.was_executed)

        self.assertRaisesRegex(RuntimeError,
                               "The bear BearWithPrerequisites does not "
                               "fulfill all requirements\\.",
                               BearWithPrerequisites,
                               self.settings,
                               self.queue,
                               False)

        self.check_message(LOG_LEVEL.WARNING,
                           "The bear BearWithPrerequisites does not fulfill "
                           "all requirements.")
        self.assertTrue(self.queue.empty())

        self.assertRaisesRegex(RuntimeError,
                               "The bear BearWithPrerequisites does not "
                               "fulfill all requirements\\. Just because "
                               "I want to\\.",
                               BearWithPrerequisites,
                               self.settings,
                               self.queue,
                               "Just because I want to.")

        self.check_message(LOG_LEVEL.WARNING,
                           "The bear BearWithPrerequisites does not fulfill "
                           "all requirements. Just because I want to.")
        self.assertTrue(self.queue.empty())

    def test_get_config_dir(self):
        section = Section("default")
        section.append(Setting("files", "**", "/path/to/dir/config"))
        uut = TestBear(section, None)
        self.assertEqual(uut.get_config_dir(), abspath("/path/to/dir"))

    def test_new_result(self):
        bear = Bear(self.settings, None)
        result = bear.new_result('test message', '/tmp/testy')
        expected = Result.from_values(bear, 'test message', '/tmp/testy')
        self.assertEqual(result, expected)
