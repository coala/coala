"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import sys
sys.path.insert(0, ".")
import multiprocessing
from coalib.filters import FILTER_KIND
from coalib.processes.communication.LOG_LEVEL import LOG_LEVEL
from coalib.processes.communication.LogMessage import LogMessage
from coalib.misc.i18n import _
from coalib.filters.Filter import Filter
import unittest


class TestFilter(Filter):
    def __init__(self, settings, queue):
        Filter.__init__(self, settings, queue)

    def set_up(self):
        self.debug_msg("set", "up", delimiter="=")

    def tear_down(self):
        self.fail_msg("teardown")

    def run_filter(self):
        self.warn_msg(self._("A string to test translations."))


class FilterTestCase(unittest.TestCase):
    def setUp(self):
        self.queue = multiprocessing.Queue()
        self.uut = TestFilter(None, self.queue)

    def test_kind(self):
        self.assertEqual(self.uut.kind(), FILTER_KIND.FILTER_KIND.UNKNOWN)

    def test_methods_available(self):
        # these should be available and not throw anything
        base = Filter(None, None)
        base.set_up()
        base.tear_down()

        self.assertRaises(NotImplementedError, base.run_filter)

        self.assertEqual(base.get_needed_settings(), {})

    def test_message_queue(self):
        self.uut.run()
        self.check_message(LOG_LEVEL.DEBUG, _("Setting up filter..."))
        self.check_message(LOG_LEVEL.DEBUG, "set=up")
        self.check_message(LOG_LEVEL.DEBUG, _("Running filter..."))
        self.check_message(LOG_LEVEL.WARNING, _("A string to test translations."))
        self.check_message(LOG_LEVEL.DEBUG, _("Tearing down filter..."))
        self.check_message(LOG_LEVEL.ERROR, "teardown")

    def check_message(self, log_level, message):
        msg = self.queue.get()
        self.assertIsInstance(msg, LogMessage)
        self.assertEqual(msg.message, message)
        self.assertEqual(msg.log_level, log_level)


if __name__ == '__main__':
    unittest.main(verbosity=2)
