import shutil

from guess_language import guess_language
from language_check import LanguageTool, correct

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange


def get_language_tool_results(filename, file_contents, locale):
    joined_text = "".join(file_contents)
    locale = guess_language(joined_text) if locale == 'auto' else locale
    locale = 'en-US' if not locale else locale

    tool = LanguageTool(locale)
    matches = tool.check(joined_text)
    for match in matches:
        if not match.replacements:
            diffs = None
        else:
            replaced = correct(joined_text, [match]).splitlines(True)
            diffs = {filename:
                     Diff.from_string_arrays(file_contents, replaced)}

        rule_id = match.ruleId
        if match.subId is not None:
            rule_id += '[{}]'.format(match.subId)

        message = match.msg + ' (' + rule_id + ')'
        yield message, diffs, SourceRange.from_values(filename,
                                                      match.fromy+1,
                                                      match.fromx+1,
                                                      match.toy+1,
                                                      match.tox+1)


class LanguageToolBear(LocalBear):

    @classmethod
    def check_prerequisites(cls):
        if shutil.which("java") is None:
            return "java is not installed."
        else:
            return True

    def run(self,
            filename,
            file,
            locale: str='auto'):
        '''
        Checks the code with LanguageTool.

        :param locale: A locale representing the language you want to
                       have checked. If set to 'auto' the language is
                       guessed. If the language cannot be guessed, 'en-US'
                       is used.
        '''
        for message, diffs, range in get_language_tool_results(
                filename, file, locale):
            yield Result(self, message, diffs=diffs, affected_code=(range,))
