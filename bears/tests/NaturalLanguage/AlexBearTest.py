import sys
import unittest
import subprocess

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import generate_local_bear_test
from bears.NaturalLanguage.AlexBear import AlexBear


LanguageToolBearTest = generate_local_bear_test(
    AlexBear,
    valid_files=(["Their network looks good."],),
    invalid_files=(['His network looks good.'],))


def skip_test():
    try:
        subprocess.Popen([AlexBear.BINARY, '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return False
    except OSError:
        return "alex is not installed."

if __name__ == '__main__':
    unittest.main(verbosity=2)
