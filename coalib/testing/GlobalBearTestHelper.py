import os.path
import unittest

from queue import Queue

from coalib.bears.GlobalBear import GlobalBear
from coalib.settings.Section import Section
from coalib.testing.BaseTestHelper import BaseTestHelper


def _get_test_path(test_dir,
                   file):
    return os.path.join(test_dir,
                        file)


class GlobalBearTestHelper(BaseTestHelper, unittest.TestCase):
    """
    """

    def get_results(self,
                    global_bear,
                    test_files,
                    test_dir):
        files = [_get_test_path(test_dir=test_dir,
                                file=file)
                 for file in test_files
                 ]
        file_dict = {}
        for filename in files:
            file_dict[filename] = tuple(filename)

        uut = global_bear(file_dict, Section('name'), Queue())
        assert isinstance(
            uut, GlobalBear), 'The given bear is not a global bear.'

        return list(uut.run())

    def check_results(self,
                      global_bear,
                      results=[],
                      test_files=[],
                      test_dir: str = ''):

        assert isinstance(self, BaseTestHelper)

        bear_output = self.get_results(global_bear,
                                       test_files=test_files,
                                       test_dir=test_dir)
        self.assert_result_equal(sorted(bear_output), sorted(results))

        return bear_output
