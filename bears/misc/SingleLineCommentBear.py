from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.bears.LocalBear import LocalBear
from coalib.misc.i18n import _
from coalib.settings.Setting import typed_list
from coalib.parsing.StringProcessing import (unescaped_search_in_between,
                                             unescaped_search_for)


class SingleLineCommentBear(LocalBear):
    def run(self,
            filename,
            file,
            string_delimiters: typed_list(str)=['"', "'"],
            spaces_before_comment: int=2,
            comment_delimiters: typed_list(str)=["#"]):
        '''
        TODO
        '''
        for line_number, line in enumerate(file, start=1):
            comments = []
            for delim in comment_delimiters:
                comments += list(unescaped_search_for(delim, line))

            if not comments:
                continue

            strings = []
            for delim in string_delimiters:
                strings += list(unescaped_search_in_between(delim, delim, line))



    def check_line_for_keyword(self, line, filename, line_number, keyword):
        pos = line.find(keyword)
        if pos != -1:
            return [Result.from_values(
                origin=self,
                message=_("The line contains the keyword `{}`.")
                        .format(keyword),
                file=filename,
                line=line_number+1,
                column=pos+1,
                end_line=line_number+1,
                end_column=pos+len(keyword)+1,
                severity=RESULT_SEVERITY.INFO)]

        return []
