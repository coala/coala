import copy

from coalib.results.Diff import Diff, ConflictError


def filter_results(original_file_dict,
                   modified_file_dict,
                   original_results,
                   modified_results):
    """
    Filters results for such ones that are unique across file changes

    :param original_file_dict: Dict of lists of file contents before  changes
    :param modified_file_dict: Dict of lists of file contents after changes
    :param original_results:   List of results of the old files
    :param modified_results:   List of results of the new files
    :return:                   List of results from new files that are unique
                               from all those that existed in the old changes
    """
    # diffs_dict[file] is a diff between the original and modified file
    diffs_dict = {}
    for file in original_file_dict:
        diffs_dict[file] = Diff.from_string_arrays(original_file_dict[file],
                                                   modified_file_dict[file])

    orig_result_diff_dict_dict = remove_result_ranges_diffs(original_results,
                                                            original_file_dict)

    mod_result_diff_dict_dict = remove_result_ranges_diffs(modified_results,
                                                           modified_file_dict)

    for m_r in modified_results:
        for o_r in original_results:

            if basics_match(o_r, m_r):
                if source_ranges_match(original_file_dict,
                                       diffs_dict,
                                       orig_result_diff_dict_dict[o_r],
                                       mod_result_diff_dict_dict[m_r]):

                    # at least one original result matches completely
                    modified_results.remove(m_r)
                    break

    # only those ones left that have no perfect match
    return modified_results


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

    return all(getattr(original_result, member) ==
               getattr(modified_result, member)
               for member in ['origin', 'message', 'severity', 'debug_msg'])


def source_ranges_match(original_file_dict,
                        diff_dict,
                        original_result_diff_dict,
                        modified_result_diff_dict):
    """
    Checks whether the SourceRanges of two results match

    :param original_file_dict: Dict of lists of file contents before changes
    :param diff_dict:          Dict of diffs describing the changes per file
    :param original_result_diff_dict: diff for each file for this result
    :param modified_result_diff_dict: guess
    :return:                     Boolean value whether the SourceRanges match
    """
    for file_name in original_file_dict:

        try:  # fails if the affected range of the result get's modified
            original_total_diff = (diff_dict[file_name] +
                                   original_result_diff_dict[file_name])
        except ConflictError:
            return False

        # original file with file_diff and original_diff applied
        original_total_file = original_total_diff.modified
        # modified file with modified_diff applied
        modified_total_file = modified_result_diff_dict[file_name].modified
        if original_total_file != modified_total_file:
            return False
    return True


def remove_range(file_contents, source_range):
    """
    removes the chars covered by the sourceRange from the file

    :param file_contents: list of lines in the file
    :param source_range:  Source Range
    :return:              list of file contents without specified chars removed
    """
    if not file_contents:
        return []

    newfile = copy.deepcopy(file_contents)
    # attention: line numbers in the SourceRange are human-readable,
    # list indices start with 0

    if source_range.start.line == source_range.end.line:
        # if it's all in one line, replace the line by it's beginning and end
        newfile[source_range.start.line - 1] = (
            newfile[source_range.start.line - 1][:source_range.start.column-1]
            + newfile[source_range.start.line - 1][source_range.end.column:])
    else:
        # cut away after start
        newfile[source_range.start.line - 1] = (
            newfile[source_range.start.line - 1][:source_range.start.column-1])

        # cut away before end
        newfile[source_range.end.line - 1] = (
            newfile[source_range.end.line - 1][source_range.end.column:])

        # start: index = first line number ==> line after first line
        # end: index = last line -2 ==> line before last line

        for i in reversed(range(
                source_range.start.line, source_range.end.line - 1)):
            del newfile[i]

    return newfile


def remove_result_ranges_diffs(result_list, file_dict):
    """
    Calculates the diffs to all files in file_dict that describe the removal of
    each respective result's affected code.

    :param result_list: list of results
    :param file_dict:   dict of file contents
    :return:            returnvalue[result][file] is a diff of the changes the
                        removal of this result's affected code would cause for
                        the file.
    """
    result_diff_dict_dict = {}
    for original_result in result_list:
        mod_file_dict = copy.deepcopy(file_dict)

        for source_range in reversed(original_result.affected_code):
            file_name = source_range.file
            new_file = remove_range(mod_file_dict[file_name],
                                    source_range)
            mod_file_dict[file_name] = new_file

        diff_dict = {}
        for file_name in file_dict:
            diff_dict[file_name] = Diff.from_string_arrays(
                file_dict[file_name],
                mod_file_dict[file_name])

        result_diff_dict_dict[original_result] = diff_dict

    return result_diff_dict_dict
