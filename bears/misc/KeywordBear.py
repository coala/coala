from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.bears.LocalBear import LocalBear


class KeywordBear(LocalBear):
    def run(self,
            filename,
            file,
            cs_keywords: list,
            ci_keywords: list):
        '''
        Checks the code files for given keywords.

        :param cs_keywords: A list of keywords to search for (case sensitive).
                            Usual examples are TODO and FIXME.
        :param ci_keywords: A list of keywords to search for (case
                            insensitive).
        '''
        results = list()

        for i in range(len(ci_keywords)):
            ci_keywords[i] = ci_keywords[i].lower()

        for line_number, line in enumerate(file):
            for keyword in cs_keywords:
                results += self.check_line_for_keyword(line,
                                                       filename,
                                                       line_number,
                                                       keyword)

            for keyword in ci_keywords:
                results += self.check_line_for_keyword(line.lower(),
                                                       filename,
                                                       line_number,
                                                       keyword)

        return results

    def check_line_for_keyword(self, line, filename, line_number, keyword):
        pos = line.find(keyword)
        if pos != -1:
            return [Result.from_values(
                origin=self,
                message="The line contains the keyword `{}`."
                        .format(keyword),
                file=filename,
                line=line_number+1,
                column=pos+1,
                end_line=line_number+1,
                end_column=pos+len(keyword)+1,
                severity=RESULT_SEVERITY.INFO)]

        return []
