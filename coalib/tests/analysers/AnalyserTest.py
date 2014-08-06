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
from coalib.analysers import ANALYSER_KIND
from coalib.processes.communication.LogMessage import LogMessage
from coalib.misc.StringConstants import StringConstants
from coalib.misc.i18n import _
from coalib.analysers.Analyser import Analyser
from coalib.output.LOG_LEVEL import LOG_LEVEL
import unittest


class TestAnalyser(Analyser):
    def __init__(self, settings, queue):
        Analyser.__init__(self, settings, queue)

    def set_up(self):
        self.debug_msg("set", "up", delimiter="=")

    def tear_down(self):
        self.fail_msg("teardown")
        self.fail_msg()

    def run_analyser(self):
        self.warn_msg(self._("A string to test translations."))


class BadTestAnalyzer(Analyser):
    def __init__(self, settings, queue):
        Analyser.__init__(self, settings, queue)

    def tear_down(self):
        raise NotImplementedError

    def run_analyser(self):
        pass


class AnalyserTestCase(unittest.TestCase):
    def setUp(self):
        self.queue = multiprocessing.Queue()
        self.uut = TestAnalyser(None, self.queue)

    def test_kind(self):
        self.assertEqual(self.uut.kind(), ANALYSER_KIND.ANALYSER_KIND.UNKNOWN)

    def test_methods_available(self):
        # these should be available and not throw anything
        base = Analyser(None, None)
        base.set_up()
        base.tear_down()

        self.assertRaises(NotImplementedError, base.run_analyser)

        self.assertEqual(base.get_needed_settings(), {})

    def test_message_queue(self):
        self.uut.run()
        self.check_message(LOG_LEVEL.DEBUG, _("Setting up analyser..."))
        self.check_message(LOG_LEVEL.DEBUG, "set=up")
        self.check_message(LOG_LEVEL.DEBUG, _("Running analyser..."))
        self.check_message(LOG_LEVEL.WARNING, _("A string to test translations."))
        self.check_message(LOG_LEVEL.DEBUG, _("Tearing down analyser..."))
        self.check_message(LOG_LEVEL.ERROR, "teardown")

    def test_bad_analyzer(self):
        self.uut = BadTestAnalyzer(None, self.queue)
        self.uut.run()
        self.check_message(LOG_LEVEL.DEBUG, _("Setting up analyser..."))
        self.check_message(LOG_LEVEL.DEBUG, _("Running analyser..."))
        self.check_message(LOG_LEVEL.DEBUG, _("Tearing down analyser..."))
        self.queue.get()  # debug message contains custom content, dont test this here
        self.check_message(LOG_LEVEL.WARNING, _("An unknown failure occurred and an analyzer run is aborted.") + " " +
                           StringConstants.THIS_IS_A_BUG)

    def check_message(self, log_level, message):
        msg = self.queue.get()
        self.assertIsInstance(msg, LogMessage)
        self.assertEqual(msg.message, message)
        self.assertEqual(msg.log_level, log_level)


if __name__ == '__main__':
    unittest.main(verbosity=2)
