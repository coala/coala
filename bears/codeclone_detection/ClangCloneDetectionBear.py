from itertools import combinations
import multiprocessing


from coalib.processes.SectionExecutor import get_cpu_count
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.settings.Setting import typed_dict
from coalib.bears.GlobalBear import GlobalBear
from coalib.misc.i18n import _
from bears.codeclone_detection.ClangCountVectorCreator import \
    ClangCountVectorCreator
from bears.codeclone_detection.ClangCountingConditions import condition_dict
from bears.codeclone_detection.CloneDetectionRoutines import \
    compare_functions, \
    get_count_matrices


"""
counting_condition_dict is a function object generated by typed_dict. This
function takes a setting and creates a dictionary out of it while it
converts all keys to counting condition function objects (via the
condition_dict) and all values to floats while unset values default to 1.
"""
counting_condition_dict = typed_dict(
    lambda setting: condition_dict[str(setting).lower()],
    float,
    1)


# Coverage cannot be measured because this is in another process
def get_difference(args):  # pragma: no cover
    """
    Retrieves the difference between two functions using the munkres algorithm.

    :param args: A tuple holding the first function id, the second and the
                 count matrices dictionary holding the count matrices for
                 each function with the function id as key.
    :return:     A tuple containing both function ids and their similarity.
    """
    function_1, function_2, count_matrices = args
    return (function_1,
            function_2,
            compare_functions(count_matrices[function_1],
                              count_matrices[function_2]))


class ClangCloneDetectionBear(GlobalBear):
    def run(self,
            condition_list: counting_condition_dict,
            max_clone_difference: float=0.15):
        '''
        Checks the given code for similar functions that are probably
        redundant.

        :param condition_list:       A comma seperated list of counting
                                     conditions. Possible values are: used,
                                     returned, is_condition, in_condition,
                                     is_assignee, is_assigner, loop_content.
                                     Weightings can be assigned to each
                                     condition due to providing a dict
                                     value, i.e. having used weighted in
                                     half as much as other conditions would
                                     simply be: "used: 0.5, is_assignee".
                                     Weightings default to 1 if unset.
        :param max_clone_difference: The maximum difference a clone should
                                     have.
        '''
        if not isinstance(condition_list, dict):
            self.err("The condition_list setting is invalid. Code clone "
                     "detection cannot run.")
            return

        self.debug("Using the following counting conditions:")
        for key, val in condition_list.items():
            self.debug(" *", key.__name__, "(weighting: {})".format(val))

        self.debug("Creating count matrices...")
        count_matrices = get_count_matrices(
            ClangCountVectorCreator(list(condition_list.keys()),
                                    list(condition_list.values())),
            list(self.file_dict.keys()))

        self.debug("Calculating differences...")
        # Code clone detection may take ages for a larger code basis. It is
        # highly probable, that no other bears are running in parallel,
        # thus we do parallel execution within this bear.
        pool = multiprocessing.Pool(get_cpu_count())
        differences = pool.map(
            get_difference,
            [(f1, f2, count_matrices)
             for f1, f2 in combinations(count_matrices, 2)])

        function_list = []
        for f_1, f_2, diff in differences:
            if diff < max_clone_difference:
                if f_1 not in function_list:
                    function_list.append(f_1)
                if f_2 not in function_list:
                    function_list.append(f_2)

        self.debug("Found {} cloned functions out of {}.".format(
            len(function_list),
            len(count_matrices)))

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
