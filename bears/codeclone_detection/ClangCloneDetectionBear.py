from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.bears.GlobalBear import GlobalBear
from bears.codeclone_detection.ClangFunctionDifferenceBear import (
    ClangFunctionDifferenceBear)


class ClangCloneDetectionBear(GlobalBear):
    def run(self,
            dependency_results: dict,
            max_clone_difference: float=0.185):
        '''
        Checks the given code for similar functions that are probably
        redundant.

        :param max_clone_difference: The maximum difference a clone should
                                     have.
        '''
        differences = dependency_results[
            ClangFunctionDifferenceBear.__name__][0].contents
        count_matrices = dependency_results[
            ClangFunctionDifferenceBear.__name__][1].contents

        self.debug("Creating results...")
        for function_1, function_2, difference in differences:
            if difference < max_clone_difference:
                yield Result.from_values(
                    self,
                    "Code clone found. The other occurrence is at file "
                    "{file}, line {line}, function {function}. The "
                    "difference is {difference}.".format(
                        file=function_2[0],
                        line=function_2[1],
                        function=function_2[2],
                        difference=difference),
                    file=function_1[0],
                    severity=RESULT_SEVERITY.MAJOR,
                    line=function_1[1],
                    debug_msg=[count_matrices[function_1],
                               count_matrices[function_2]])

    @staticmethod
    def get_dependencies():
        return [ClangFunctionDifferenceBear]
