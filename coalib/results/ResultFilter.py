

def filter_results(original_file_dict,
                   modified_file_dict,
                   original_results,
                   modified_results):
    """
    Filters results for such ones that are unique across file changes

    :param original_file_dict: Dict of lists of file contents before the changes
    :param modified_file_dict: Dict of lists of file contents after the changes
    :param original_results:   List of results of the old files
    :param modified_results:   List of results of the new files
    :return:                   List of results from new files that are unique
                               from all those that existed in the old changes
    """
    uniques = []

    for m_r in modified_results:
        if True not in [basics_match(o_r, m_r) for o_r in original_results]:
            uniques.append(m_r)

    return uniques


def basics_match(original_result,
                 modified_result):
    """
    Checks whether the following properties of two results match:
    * origin
    * message
    * severity
    * debug_msg

    :param original_result: A result of the old files
    :param modified_result: A result of the new files
    :return:                Boolean value whether or not the properties match
    """
    # origin might be a class or class name
    original_origin = isinstance(original_result.origin, str) and \
        original_result.origin or original_result.origin.__name__()
    modified_origin = isinstance(modified_result.origin, str) and \
        modified_result.origin or modified_result.origin.__name__()

    # we cannot tolerate differences!
    if original_origin != modified_origin:
        return False

    elif original_result.message != modified_result.message:
        return False

    elif original_result.severity != modified_result.severity:
        return False

    elif original_result.debug_msg != modified_result.debug_msg:
        return False

    else:
        return True


def source_ranges_match(original_file_dict,
                        diff_dict,
                        original_result,
                        modified_result):
    """
    Checks whether the SourceRanges of two results match

    :param original_file_dict: Dict of lists of file contents before the changes
    :param diff_dict:          Dict of diffs describing the change in each file
    :param original_result:    A result of the old files
    :param modified_result:    A result of the new files
    :return:                   Boolean value whether the SourceRanges match
    """
    return False # pragma: no cover


def diffs_match(original_file_dict,
                modified_file_dict,
                diff_dict,
                original_result,
                modified_result):
    """
    Checks whether the Diffs of two results describe the same changes

    :param original_file_dict: Dict of lists of file contents before the changes
    :param modified_file_dict: Dict of lists of file contents after the changes
    :param diff_dict:          Dict of diffs describing the change in each file
    :param original_result:    A result of the old files
    :param modified_result:    A result of the new files
    :return:                   Boolean value whether the Diffs match
    """
    return False # pragma: no cover
