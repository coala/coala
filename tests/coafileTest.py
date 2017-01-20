import unittest
import re
from coalib.misc.Shell import run_shell_command
from coalib.output.printers.LogPrinter import LogPrinter
from pyprint.ConsolePrinter import ConsolePrinter
from coalib.settings.ConfigurationGathering import load_config_file
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL


class coafileTest(unittest.TestCase):

    def setUp(self):
        self.logprinter = LogPrinter(ConsolePrinter(), LOG_LEVEL.ERROR)
        self.sections = load_config_file('.coafile', self.logprinter, True)

    def test_commit_regex(self):
        shortlog_regex=self.sections['commit']['shortlog_regex'].value
        for i in range(0, 100):
            git_command = 'git log -1 --skip {0} --pretty=%B'.format(i)
            commit_message, stderr = run_shell_command(git_command)
            self.assertEqual(stderr,'',msg=stderr)
            pos = commit_message.find('\n')
            if(pos != -1):
                commit_message = commit_message[:pos]
            self.assertIsNotNone(re.fullmatch(shortlog_regex, commit_message),
                                 msg='\"{0}\" does not match the give regex'.format(commit_message))
