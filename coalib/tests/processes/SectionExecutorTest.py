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
import inspect
import os
import sys
sys.path.insert(0, ".")

import unittest
from coalib.settings.SectionManager import SectionManager
from coalib.processes.SectionExecutor import SectionExecutor
from coalib.settings.Section import Section


class SectionExecutorInitTestCase(unittest.TestCase):
    def test_init(self):
        self.assertRaises(TypeError, SectionExecutor, 5,               [], [])
        self.assertRaises(TypeError, SectionExecutor, Section("test"), 5 , [])
        self.assertRaises(TypeError, SectionExecutor, Section("test"), [], 5 )
        self.assertRaises(TypeError, SectionExecutor, Section("test"), [], [], outputter=5)
        self.assertRaises(TypeError, SectionExecutor, Section("test"), [], [], log_printer=5)
        self.assertRaises(IndexError, SectionExecutor(Section("test"), [], []).run)


class SectionExecutorTestCase(unittest.TestCase):
    def setUp(self):
        config_path = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(SectionExecutorTestCase)),
                                                   "section_executor_test_files",
                                                   ".coafile"))

        self.sections, self.local_bears, self.global_bears = SectionManager().run(["--config", config_path])
        self.uut = SectionExecutor(self.sections["default"], self.local_bears["default"], self.global_bears["default"])

    def test_run(self):
        self.uut.run()


if __name__ == '__main__':
    unittest.main(verbosity=2)
