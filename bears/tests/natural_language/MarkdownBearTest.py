import sys
import unittest
import subprocess

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import generate_local_bear_test
from bears.natural_language.MarkdownBear import MarkdownBear


MarkdownBearTest = generate_local_bear_test(
    MarkdownBear,
    (["```\n", "some code\n", "```\n"],),
    (['    some code'],))


def skip_test():
    try:
        subprocess.Popen([MarkdownBear.BINARY, '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return False
    except OSError:
        return "remark is not installed."


if __name__ == '__main__':
    unittest.main(verbosity=2)
