from language_check import LanguageTool, correct

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.Diff import Diff


def get_language_tool_results(file_contents, locale):
    tool = LanguageTool(locale)
    joined_text = "".join(file_contents)
    matches = tool.check(joined_text)
    for match in matches:
        if not match.replacements:
            diff = None
        else:
            replaced = correct(joined_text, [match]).splitlines(True)
            diff = Diff.from_string_arrays(file_contents, replaced)

        rule_id = match.ruleId
        if match.subId is not None:
            rule_id += '[{}]'.format(match.subId)

        message = (match.msg + ' (' + rule_id + ', ' +
                   'Found at column {col}.').format(col=match.fromx+1) + ')'
        yield message, diff, match.fromy+1


class LanguageToolBear(LocalBear):
    def run(self,
            filename,
            file,
            locale: str='en-US'):
        '''
        Checks the code with LanguageTool.

        locale: A locale representing the language you want to have checked.
        '''
        for message, diff, line in get_language_tool_results(file, locale):
            if diff:
                yield Result.from_values(self,
                                         message,
                                         diffs={filename: diff},
                                         file=filename,
                                         line=line)
            else:
                yield Result.from_values(self,
                                         message,
                                         file=filename,
                                         line=line)
