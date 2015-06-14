from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.bears.GlobalBear import GlobalBear
from coalib.misc.i18n import _
from bears.codeclone_detection.ClangSimilarityBear import ClangSimilarityBear


class ClangCloneDetectionBear(GlobalBear):
    def run(self,
            dependency_results: dict,
            max_clone_difference: float=0.33):
        '''
        Checks the given code for similar functions that are probably
        redundant.

        :param max_clone_difference: The maximum difference a clone should
                                     have.
        '''
        differences = dependency_results["ClangSimilarityBear"][0].contents

        self.debug("Creating results...")
        results = []
        for function_1, function_2, difference in differences:
            if difference < max_clone_difference:
                results.append(Result(
                    self.__class__.__name__,
                    _("Code clone found. The other occurrence is at file "
                      "{file}, line {line}, function {function}. The "
                      "similarity is {similarity}.").format(
                        file=function_2[0],
                        line=function_2[1],
                        function=function_2[2],
                        similarity=1-difference),
                    file=function_1[0],
                    severity=RESULT_SEVERITY.MAJOR,
                    line_nr=function_1[1]))

        return results

    @staticmethod
    def get_dependencies():
        return [ClangSimilarityBear]
