import json
import os.path

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange
from dependency_management.requirements.GemRequirement import GemRequirement
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.GlobalBearTestHelper import GlobalBearTestHelper


@linter(executable='brakeman',
        global_bear=True)
class RubySecurityBear:
    """
    Checks the Security issues of Ruby Applications.

    It uses ``brakeman``.
    """

    LANGUAGES = {'Ruby'}
    REQUIREMENTS = {GemRequirement('brakeman', '4.1.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Security'}
    SEE_MORE = 'https://brakemanscanner.org/'

    severity_map = {'High': RESULT_SEVERITY.MAJOR,
                    'Medium': RESULT_SEVERITY.NORMAL,
                    'Weak': RESULT_SEVERITY.INFO}

    def create_arguments(self, config_file):
        files = tuple(self.file_dict.keys())
        app = os.path.dirname(os.path.commonprefix(files))
        return '-f', 'json', app

    def process_output(self, output, file, filename):
        outputs = json.loads(output)
        for message_type, values in outputs.items():
            if message_type != 'warnings':
                continue

            for value in values:
                sourceranges = [SourceRange.from_values(
                    file=value['file'],
                    start_line=value['line'],
                    end_line=value['line'])]

                if value['code'] is None:
                    message = "'{}': {}".format(
                        value['check_name'], value['message'])

                else:
                    message = "'{}' (in '{}'): {}.".format(
                        value['check_name'], value['code'],
                        value['message'])

                yield Result(
                    origin='{} ({})'.format(self.__class__.__name__,
                                            value['warning_type']),
                    message=message,
                    affected_code=sourceranges,
                    severity=self.severity_map[value['confidence']],
                    additional_info='More information is available at {}'
                                    '.'.format(value['link']))


def _get_test_path():
    return os.path.join(os.path.dirname(__file__),
                        'brakeman_test_files')


@generate_skip_decorator(RubySecurityBear)
class RubySecurityBearTest(GlobalBearTestHelper):

    def test_result(self):
        self.check_results(RubySecurityBear,
                           [Result.from_values(
                                origin='RubySecurityBear (Dangerous Eval)',
                                message="'Evaluation' (in 'eval(params)'): "
                                        'User input in eval.',
                                severity=RESULT_SEVERITY.MAJOR,
                                file='app/models/user.rb',
                                line=3,
                                additional_info='More information is available'
                                                ' at https://brakemanscanner.o'
                                                'rg/docs/warning_types/danger'
                                                'ous_eval/.'),
                            Result.from_values(
                                origin='RubySecurityBear (Format Validation)',
                                message="'ValidationRegex': Insufficient "
                                        "validation for 'name' using /^[a-zA-Z]"
                                        '+$/. Use \\A and \\z as anchors',
                                severity=RESULT_SEVERITY.MAJOR,
                                file='app/models/account.rb',
                                line=2,
                                additional_info='More information is available'
                                                ' at https://brakemanscanner.'
                                                'org/docs/warning_types/format'
                                                '_validation/.')],
                           ['**'],
                           _get_test_path())
