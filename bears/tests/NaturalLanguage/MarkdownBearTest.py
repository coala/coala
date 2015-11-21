import sys
import unittest
import subprocess

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import generate_local_bear_test
from bears.NaturalLanguage.MarkdownBear import MarkdownBear


LanguageToolBearTest = generate_local_bear_test(
    MarkdownBear,
    # Last \n because of https://github.com/wooorm/mdast/issues/91
    valid_files=(["```\n", "some code\n", "```\n", "\n"],),
    invalid_files=(['    some code'],))


def skip_test():
    try:
        subprocess.Popen([MarkdownBear.BINARY, '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return False
    except OSError:
        return "mdast is not installed."

if __name__ == '__main__':
    unittest.main(verbosity=2)
