from shutil import which
from unittest.case import SkipTest

from bears.tests.LocalBearTestHelper import verify_local_bear
from bears.c_languages.CPPLintBear import CPPLintBear

if which('cpplint') is None:
    raise SkipTest('cpplint is not installed')

test_file = '''
int main() {
    return 0;
}
'''.split('\n')

CPPLintBearTest = verify_local_bear(CPPLintBear,
                                    invalid_files=(test_file, ),
                                    filename={'suffix': '.cpp'})

CPPLintBearTestLegal = verify_local_bear(CPPLintBear,
                                         valid_files=(test_file, ),
                                         filename={'suffix': '.cpp'},
                                         settings={'cpplint_ignore': 'legal'})

CPPLintBearTestLength = verify_local_bear(CPPLintBear,
                                          invalid_files=(test_file, ),
                                          filename={'suffix': '.cpp'},
                                          settings={'cpplint_ignore': 'legal',
                                                    'max_line_length': '5'})
