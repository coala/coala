__author__ = 'lasse'

import unittest
from codeclib.fillib.util.setting import Setting


class SettingTest(unittest.TestCase):
    def setUp(self):
        self.test_instance = Setting('TestKey',
                                     ['TestValue', ''],
                                     trailing_comment="testcomment",
                                     comments_before=["beforecomment", ""])

    def tearDown(self):
        pass

    def test_line_generation(self):
        lines = self.test_instance.generate_lines()
        self.assertEqual(lines, [
            '# beforecomment',
            '',
            'TestKey = TestValue,  # testcomment'
        ], "Line generation does not work!")
