import shutil
import unittest
from unittest.case import SkipTest

from bears.natural_language.LanguageToolBear import LanguageToolBear
from bears.tests.BearTestHelper import generate_skip_decorator
from bears.tests.LocalBearTestHelper import verify_local_bear

try:
    import language_check
    import guess_language
except ImportError as err:
    raise SkipTest(str(err))


LanguageToolBear1Test = verify_local_bear(
    LanguageToolBear,
    valid_files=(["A correct English sentence sounds nice in everyone."],
                 ["Eine korrekte englische Satz klingt nett zu jedermann."]),
    invalid_files=(["  "],
                   ["asdgaasdfgahsadf"],
                   ['"quoted"']))


LanguageToolBear2Test = verify_local_bear(
    LanguageToolBear,
    valid_files=(["A correct English sentence sounds nice in everyone."],),
    invalid_files=(["Eine korrekte englische Satz klingt nett zu jedermann."],),
    settings={'locale': 'en-US'})


@generate_skip_decorator(LanguageToolBear)
class LanguageToolBearTest(unittest.TestCase):

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertEqual(LanguageToolBear.check_prerequisites(),
                             "java is not installed.")

            shutil.which = lambda *args, **kwargs: "path/to/java"
            self.assertTrue(LanguageToolBear.check_prerequisites())
        finally:
            shutil.which = _shutil_which
