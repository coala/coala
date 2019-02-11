import unittest

from coala_utils.ContextManagers import retrieve_stderr
from coalib.testing.LineLengthTestHelper import verify_line_length
from tests.test_bears.LineLengthTestBear import LineLengthTestBear
from coalib.bearlib.aspects import (
    AspectList,
    get as get_aspect,
)


verify_line_length_test = verify_line_length(
                              LineLengthTestBear,
                              source_file='test\ntesta\ntestaaa',)

verify_line_length_setting_test = verify_line_length(
                                      LineLengthTestBear,
                                      source_file='test\ntesta\ntestaaa',
                                      settings={'max_line_length': '79'})

verify_line_length_aspect_test = verify_line_length(
                                     LineLengthTestBear,
                                     source_file='test\ntesta\ntestaaa',
                                     aspects=AspectList([
                                         get_aspect('LineLength')(
                                             'Unknown',
                                             max_line_length=20),
                                     ]),)


class VerifyLineLengthTest(unittest.TestCase):
    def test_timeout_deprecation_warning(self):
        with retrieve_stderr() as stderr:
            verify_line_length(LineLengthTestBear, source_file=(), timeout=50)
            self.assertIn('timeout is ignored as the timeout set in the repo '
                          'configuration will be sufficient', stderr.getvalue())
