from coalib.results.Result import Result
from coalib.bears.LocalBear import LocalBear
from coalib.misc.i18n import _


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
        for i in range(len(ci_keywords)):
            ci_keywords[i] = ci_keywords[i].lower()

        for line_number, line in enumerate(file):
            found_kws = []
            for keyword in cs_keywords:
                if keyword in line:
                    found_kws.append(keyword)

            for keyword in ci_keywords:
                if keyword in line.lower():
                    found_kws.append(keyword)

            if found_kws != []:
                yield Result(
                    origin=self,
                    message=_("Line contains the following keywords:") +
                            "\n" + ", ".join(found_kws),
                    file=filename,
                    line_nr=line_number + 1)
