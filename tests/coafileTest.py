import unittest
import re
from coalib.settings.ConfigurationGathering import load_config_file


class coafileTest(unittest.TestCase):

    def setUp(self):
        self.filepath = '.coafile'
        self.commits_filepath = 'tests/commits.txt'
        self.sections = load_config_file(self.filepath, None, True)

    def test_commit_regex(self):
        regex_string = self.sections['commit']['shortlog_regex'].value
        shortlog_regex = re.compile(regex_string)
        git_log = open(self.commits_filepath, 'r').read()
        for message in git_log.splitlines():
            self.assertIsNotNone(shortlog_regex.fullmatch(message),
                                 msg='{!r} does not match the '
                                 'given regex {}'.format(message, regex_string))
