from coalib.parsing.StringProcessing import convert_to_raw
from tests.parsing.StringProcessing.StringProcessingTestBase import (
    StringProcessingTestBase)


class ConvertToRawTest(StringProcessingTestBase):

    def test_convert_to_raw(self):
        # In (input, output) format
        test_data = [
            (r"test", r"test"),
            (r"test_path", r"test_path"),
            (r"test, path", r"test, path"),
            (r"test\ path", r"test\ path"),
            (r"test\path", r"test\\path"),
            (r"test\\path", r"test\\path"),
            (r"test\=path", r"test\=path"),
            (r"test=path", r"test=path"),
            (r"value\=as\something", r"value\=as\\something")]
        for test in test_data:
            self.assertEqual(convert_to_raw(test[0], ",.=# "), test[1])
