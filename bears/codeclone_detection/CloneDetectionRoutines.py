import os
import math
import copy
from munkres import Munkres
# Instantiate globally since this class is holding stateless public methods.
munkres = Munkres()

from coalib.collecting.Collectors import collect_dirs


def exclude_function(count_matrix):
    """
    Determines heuristically whether or not it makes sense for clone
    detection to take this function into account.

    Applied heuristics:
     * Functions with only count vectors with a sum of all unweighted elements
       of lower then 10 are very likely only declarations or empty and to be
       ignored. (Constants are not taken into account.)

    :param count_matrix: A dictionary with count vectors representing all
                         variables for a function.
    :return:             True if the function is useless for evaluation.
    """
    var_count = [cv.name.startswith("#")
                 for cv in count_matrix.values()].count(False)
    variable_sum = sum(0 if cv.name.startswith("#") else sum(cv.unweighted)
                       for cv in count_matrix.values())
    return (all((cv.name.startswith("#") or sum(cv.unweighted) < 10)
                for cv in count_matrix.values()) or
            variable_sum < 11 or
            var_count < 2)


def get_count_matrices(count_vector_creator,
                       filenames,
                       progress_callback,
                       base_path,
                       extra_include_paths):
    """
    Retrieves matrices holding count vectors for all variables for all
    functions in the given file.

    :param count_vector_creator: A object with a get_vectors_for_file method
                                 taking a filename as argument.
    :param filenames:            The files to create count vectors for.
    :param progress_callback:    A function with one float argument which is
                                 called after processing each file with the
                                 progress percentage (float) as an argument.
    :param extra_include_paths:  A list containing additional include paths.
    :return:                     A dict holding a tuple of (file, line,
                                 function) as key and as value a dict with
                                 variable names as key and count vector
                                 objects as value.
    """
    result = {}
    maxlen = len(filenames)
    include_paths = collect_dirs([os.path.dirname(base_path) + "/**"])
    include_paths += extra_include_paths

    for i, filename in enumerate(filenames):
        progress_callback(100*(i/maxlen))
        count_dict = count_vector_creator.get_vectors_for_file(filename,
                                                               include_paths)
        for function in count_dict:
            if not exclude_function(count_dict[function]):
                result[(filename,
                        function[0],
                        function[1])] = count_dict[function]

    return result


def pad_count_vectors(cm1, cm2):
    """
    Pads the smaller count matrix with zeroed count vectors.

    :param cm1: First cm. Will not be modified.
    :param cm2: Second cm. Will not be modified.
    :return:    A tuple holding two cms.
    """
    cm1len = len(cm1)
    cm2len = len(cm2)
    if cm1len != cm2len:
        # Copy the smaller matrix as it will be altered
        if cm1len > cm2len:
            cm2 = copy.copy(cm2)
        else:  # make cm1 the larger (or equal) one
            tmp = cm2
            cm2 = copy.copy(cm1)
            cm1 = tmp

        any_count_vector = list(cm1.values())[0]
        # Fill up smaller count matrix with zero vectors. This way no
        # padding is needed later and if count vectors are zero on both
        # side, the difference is zero too which wouldn't be taken into
        # account with simple padding of ones.
        for i in range(len(cm1) - len(cm2)):
            cm2[i] = any_count_vector.create_null_vector(i)

    return cm1, cm2


def relative_difference(difference, maxabs):
    if maxabs == 0:
        return 1
    return difference/maxabs


def average(lst):
    return sum(lst)/len(lst)


def get_difference(matching_iterator,
                   average_calculation,
                   poly_postprocessing,
                   exp_postprocessing):
    """
    Retrieves the difference value for the matched function represented by the
    given matches.

    Postprocessing may be done because small functions are less likely to be
    clones at the same difference value than big functions which may provide a
    better refactoring opportunity for the user.

    :return:                    A difference value between 0 and 1.

    :param matching_iterator:   A list holding tuples of an absolute difference
                                value and a value to normalize the difference
                                into a range of [0, 1].
    :param average_calculation: If set to true this function will take the
                                average of all variable differences as the
                                difference, else it will normalize the
                                function as a whole and thus weighting in
                                variables dependent on their size.
    :param poly_postprocessing: If set to true, the difference value of big
                                function pairs will be reduced using a
                                polynomial approach.
    :param exp_postprocessing:  If set to true, the difference value of big
                                function pairs will be reduced using an
                                exponential approach.
    """
    norm_sum = sum(norm for diff, norm in matching_iterator)

    if average_calculation:
        difference = average([relative_difference(diff, norm)
                              for diff, norm in matching_iterator])
    else:
        difference = relative_difference(
            sum(diff for diff, norm in matching_iterator),
            norm_sum)

    if poly_postprocessing and norm_sum != 0:
        # This function starts at 1 and converges to .75 for norm_sum -> inf
        difference *= (3*norm_sum+1)/(4*norm_sum)
    if exp_postprocessing and norm_sum != 0:
        difference *= math.exp(1-norm_sum)/4 + 0.75

    return difference


def compare_functions(cm1,
                      cm2,
                      average_calculation=False,
                      poly_postprocessing=True,
                      exp_postprocessing=False):
    """
    Compares the functions represented by the given count matrices.

    Postprocessing may be done because small functions are less likely to be
    clones at the same difference value than big functions which may provide a
    better refactoring opportunity for the user.

    :param cm1:                 Count vector dict for the first function.
    :param cm2:                 Count vector dict for the second function.
    :param average_calculation: If set to true the difference calculation
                                function will take the average of all variable
                                differences as the difference, else it will
                                normalize the function as a whole and thus
                                weighting in variables dependent on their size.
    :param poly_postprocessing: If set to true, the difference value of big
                                function pairs will be reduced using a
                                polynomial approach.
    :param exp_postprocessing:  If set to true, the difference value of big
                                function pairs will be reduced using an
                                exponential approach.
    :return:                    The difference between these functions, 0 is
                                identical and 1 is not similar at all.
    """
    assert 0 not in (len(cm1), len(cm2))

    cm1, cm2 = pad_count_vectors(cm1, cm2)

    diff_table = [(cv1,
                   [(cv2, cv1.difference(cv2), cv1.maxabs(cv2))
                    for cv2 in cm2.values()])
                  for cv1 in cm1.values()]

    # The cost matrix holds the difference between the two variables i and
    # j in the i/j field. This is a representation of a bipartite weighted
    # graph with nodes representing the first function on the one side
    # (rows) and the nodes representing the second function on the other
    #  side (columns). The fields in the matrix are the weighted nodes
    # connecting each element from one side to the other.
    cost_matrix = [[relative_difference(difference, maxabs)
                    for cv2, difference, maxabs in lst]
                   for cv1, lst in diff_table]

    # The munkres algorithm will calculate a matching such that the sum of
    # the taken fields is minimal. It thus will associate each variable
    # from one function to one on the other function.
    matching = munkres.compute(cost_matrix)

    return get_difference([(diff_table[x][1][y][1], diff_table[x][1][y][2])
                           for x, y in matching],
                          average_calculation,
                          poly_postprocessing,
                          exp_postprocessing)
