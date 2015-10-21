import sys
import os
import unittest
import re
import hashlib

if sys.version_info < (3, 4):
    import imp as importlib
else:
    import importlib

sys.path.insert(0, ".")
from coalib.tests.misc.i18nTest import set_lang
from coalib.misc.ContextManagers import retrieve_stdout
from coalib import coala_ci
from coalib.settings import ConfigurationGathering
from coalib.misc.Constants import Constants


def execute_coala_ci(args):
    """
    Executes the coala-ci main function with the given argument string.

    :param args: A list of arguments to pass to coala.
    :return:     A tuple holding the return value first and the stdout output
                 as second element.
    """
    sys.argv = ["coala-ci"] + list(args)
    # Need to reload both as ConfigurationGathering has the old sys.argv loaded
    # and coala_ci has the old ConfigurationGathering values.
    importlib.reload(ConfigurationGathering)
    importlib.reload(coala_ci)
    with retrieve_stdout() as stdout:
        retval = coala_ci.main()
        return retval, stdout.getvalue()


class coalaTest(unittest.TestCase):
    def setUp(self):
        self.old_argv = sys.argv
        set_lang("unknown_language")  # Fall back to untranslated
        self.coafile = re.escape(os.path.abspath("./.coafile"))

    def tearDown(self):
        sys.argv = self.old_argv

    def test_nonexistent(self):
        retval, output = execute_coala_ci(("-c", "nonex", "test"))
        self.assertRegex(
            output,
            ".*\\[WARNING\\].*The requested coafile '.*' does not exist.\n"
            ".*\\[WARNING\\].*The requested section 'test' is not.*\n")

    def test_find_no_issues(self):
        retval, output = execute_coala_ci(("-c", self.coafile))
        self.assertRegex(output,
                         "(.*Unable to collect bears from.*PyLintBear.*)?",
                         "coala-ci output should be empty when running "
                         "over its own code.")
        self.assertEqual(retval,
                         0,
                         "coala-ci must return zero when running over its "
                         "own code.")

    def test_find_issues(self):
        retval, output = execute_coala_ci(("todos", "-c", self.coafile))
        self.assertRegex(output,
                         "(.*Unable to collect bears from.*PyLintBear.*)?",
                         "coala-ci output should be empty when running "
                         "over its own code. (Target section: todos)")
        self.assertNotEqual(retval,
                            0,
                            "coala-ci must return nonzero when running over "
                            "its own code. (Target section: todos)")

    def test_tag(self):
        default_hash = hashlib.sha224(
            (os.getcwd() + "/.coafile test_tag").encode()).hexdigest()
        execute_coala_ci(("-S", "tag=test_tag", "-c", self.coafile))
        self.assertTrue(os.path.exists(Constants.TAGS_DIR+"/"+default_hash))


if __name__ == '__main__':
    unittest.main(verbosity=2)
