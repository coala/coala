

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
    return [modified_results]


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
    return False


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
    return False


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
    return False
    ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
    