import unittest

from coalib.results.HiddenResult import HiddenResult


class HiddenResultTest(unittest.TestCase):

    def test_hidden_result(self):
        uut = HiddenResult('any', 'anything')
        self.assertEqual(uut.contents, 'anything')
