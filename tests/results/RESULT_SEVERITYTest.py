import unittest

from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class RESULT_SEVERITYTest(unittest.TestCase):

    def test_str_conversion(self):
        self.assertEqual('INFO',
                         RESULT_SEVERITY.__str__(RESULT_SEVERITY.INFO))
        self.assertEqual('NORMAL',
                         RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL))
        self.assertEqual('MAJOR',
                         RESULT_SEVERITY.__str__(RESULT_SEVERITY.MAJOR))
