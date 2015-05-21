from munkres import Munkres
# Instantiate globally since this class is holding stateless public methods.
munkres = Munkres()


def exclude_function(count_matrix):
    """
    Determines heuristically whether or not it makes sense for clone
    detection to take this function into account.

    Applied heuristics:
     * Functions with only count vectors with a sum of all elements of 1
       or 0 are very likely only declarations or empty and to be ignored.

    :param count_matrix: A dictionary with count vectors representing all
                         variables for a function.
    :return:             True if the function is useless for evaluation.
    """
    return all(sum(cv.count_vector) < 2 for cv in count_matrix.values())


def get_count_matrices(count_vector_creator,
                       filenames,
                       progress_callback=lambda x: x):
    """
    Retrieves matrices holding count vectors for all variables for all
    functions in the given file.

    :param count_vector_creator: A object with a get_vectors_for_file method
                                 taking a filename as argument.
    :param filenames:            The files to create count vectors for.
    :param progress_callback:    A function with one float argument which is
                                 called after processing each file with the
                                 progress percentage (float) as an argument.
    :return:                     A dict holding a tuple of (file, line,
                                 function) as key and as value a dict with
                                 variable names as key and count vector
                                 objects as value.
    """
    result = {}
    maxlen = len(filenames)

    for i, filename in enumerate(filenames):
        progress_callback(100*(i/maxlen))
        count_dict = count_vector_creator.get_vectors_for_file(filename)
        for function in count_dict:
            if not exclude_function(count_dict[function]):
                result[(filename,
                        function[0],
                        function[1])] = count_dict[function]

    return result


# Coverage cannot be measured because this is in another process
def compare_functions(cm1, cm2):  # pragma: no cover
    """
    Compares the functions represented by the given count matrices.

    :param cm1: Count vector dict for the first function.
    :param cm2: Count vector dict for the second function.
    :return:    The difference between these functions, 0 is identical and
                1 is not similar at all.
    """
    assert isinstance(cm1, dict)
    assert isinstance(cm2, dict)
    if len(cm1) == 0 or len(cm2) == 0:
        return 1 if len(cm1) != len(cm2) else 0

    # The cost matrix holds the difference between the two variables i and
    # j in the i/j field. This is a representation of a bipartite weighted
    # graph with nodes representing the first function on the one side
    # (rows) and the nodes representing the second function on the other
    #  side (columns). The fields in the matrix are the weighted nodes
    # connecting each element from one side to the other.
    cost_matrix = [[cv1.difference(cv2)
                    for cv2 in cm2.values()]
                   for cv1 in cm1.values()]

    # Pad manually with ones. If we have one variable in one function and
    # no corresponding in the other this is 100% difference, so 1.
    cost_matrix = munkres.pad_matrix(cost_matrix, pad_value=1)

    # The munkres algorithm will calculate a matching such that the sum of
    # the taken fields is minimal. It thus will associate each variable
    # from one function to one on the other function.
    matching = munkres.compute(cost_matrix)

    # Sum it up, normalize it so we have a value in [0, 1]
    return (sum(cost_matrix[x][y] for x, y in matching) /
            max(len(cm1), len(cm2)))
