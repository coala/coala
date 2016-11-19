from queue import Queue
import unittest

from tests.test_bears.TestBear import TestBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.testing.LocalBearTestHelper import verify_local_bear, execute_bear


files = ('Everything is invalid/valid/raises error',)
invalidTest = verify_local_bear(TestBear,
                                valid_files=(),
                                invalid_files=files,
                                settings={'result': True})
validTest = verify_local_bear(TestBear,
                              valid_files=files,
                              invalid_files=())


class LocalBearTestHelper(unittest.TestCase):

    def setUp(self):
        section = Section('')
        section.append(Setting('exception', True))
        self.uut = TestBear(section, Queue())

    def test_exception(self):

        with self.assertRaises(AssertionError), execute_bear(
                self.uut,  'Luke', files[0]) as result:
            pass
