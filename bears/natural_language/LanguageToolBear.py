from language_check import LanguageTool, correct

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.results.SourceRange import SourceRange


def get_language_tool_results(filename, file_contents, locale):
    tool = LanguageTool(locale)
    joined_text = "".join(file_contents)
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
    def run(self,
            filename,
            file,
            locale: str='en-US'):
        '''
        Checks the code with LanguageTool.

        locale: A locale representing the language you want to have checked.
        '''
        for message, diffs, range in get_language_tool_results(
                filename, file, locale):
            yield Result(self, message, diffs=diffs, affected_code=(range,))
