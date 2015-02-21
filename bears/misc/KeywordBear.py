from coalib.results.Result import Result
from coalib.bears.LocalBear import LocalBear
from coalib.misc.i18n import _


class KeywordBear(LocalBear):
    def run(self,
            filename,
            file,
            cs_keywords: list,
            ci_keywords: list):
        """
        Checks the code files for given keywords.

        :param cs_keywords: A list of keywords to search for case sensitively. Usual examples are TODO and FIXME.
        :param ci_keywords: A list of keywords to search for case insensitively.
        """
        results = []

        for i in range(len(ci_keywords)):
            ci_keywords[i] = ci_keywords[i].lower()

        for line_number, line in enumerate(file):
            found_kws = []
            for kw in cs_keywords:
                if kw in line:
                    found_kws.append(kw)

            for kw in ci_keywords:
                if kw in line.lower():
                    found_kws.append(kw)

            if found_kws != []:
                results.append(Result(origin=self,
                                      message=_("Line contains the following keywords:") + "\n" + ", ".join(found_kws),
                                      file=filename,
                                      line_nr=line_number + 1))

        return results
