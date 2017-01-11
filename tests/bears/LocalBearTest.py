import unittest

from coalib.bears.LocalBear import LocalBear
from coalib.settings.Section import Section


class LocalBearTest(unittest.TestCase):

    def test_api(self):
        test_object = LocalBear(Section('name'), None)
        self.assertRaises(NotImplementedError,
                          test_object.run,
                          'filename',
                          ['file\n'])
