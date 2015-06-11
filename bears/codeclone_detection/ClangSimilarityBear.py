from itertools import combinations

from coalib.misc.StringConverter import StringConverter
from coalib.results.HiddenResult import HiddenResult
from coalib.settings.Setting import typed_dict
from coalib.bears.GlobalBear import GlobalBear
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
    :return:     A tuple containing both function ids and their difference.
    """
    function_1, function_2, count_matrices = args
    return (function_1,
            function_2,
            compare_functions(count_matrices[function_1],
                              count_matrices[function_2]))


class ClangSimilarityBear(GlobalBear):
    def run(self,
            condition_list: counting_condition_dict=
                counting_condition_dict(StringConverter(
                    "returned, "
                    "is_condition, "
                    "in_condition, "
                    "in_second_level_condition, "
                    "in_third_level_condition, "
                    "is_assignee, "
                    "is_assigner, "
                    "loop_content, "
                    "second_level_loop_content, "
                    "third_level_loop_content, "
                    "is_param, "
                    "in_sum, "
                    "in_product, "
                    "in_binary_operation,"
                    "member_accessed"))):
        '''
        Retrieves similarities for code clone detection. Those can be reused in
        another bear to produce results.

        :param condition_list:       A comma seperated list of counting
                                     conditions. Possible values are: used,
                                     returned, is_condition, in_condition,
                                     in_second_level_condition,
                                     in_third_level_condition, is_assignee,
                                     is_assigner, loop_content,
                                     second_level_loop_content,
                                     third_level_loop_content, is_param,
                                     in_sum, in_product, in_binary_operation,
                                     member_accessed.
                                     Weightings can be assigned to each
                                     condition due to providing a dict
                                     value, i.e. having used weighted in
                                     half as much as other conditions would
                                     simply be: "used: 0.5, is_assignee".
                                     Weightings default to 1 if unset.
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
                                    list(condition_list.values()),
                                    self.section["files"].origin),
            list(self.file_dict.keys()),
            lambda prog: self.debug("{:2.4f}%...".format(prog)))

        self.debug("Calculating differences...")
        differences = []
        function_count = len(count_matrices)
        # Thats n over 2, hardcoded to simplify calculation
        combination_length = function_count * (function_count-1) / 2
        function_combinations = [(f1, f2, count_matrices)
                                 for f1, f2 in combinations(count_matrices, 2)]

        for i, elem in enumerate(map(get_difference, function_combinations)):
            if i % 1000 == 0:
                self.debug("{:2.4f}%...".format(100*i/combination_length))
            differences.append(elem)

        return [HiddenResult(self.__class__.__name__, differences)]
