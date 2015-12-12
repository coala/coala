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

    #  orig_result_diff_dict_dict[result][file] is a diff of the changes this
    # result would apply to the file

    orig_result_diff_dict_dict = {}
    for original_result in original_results:
        orig_file_dict_copy = copy.deepcopy(original_file_dict)

        for source_range in original_result.affected_code:
            file_name = source_range.file
            new_file = remove_range(orig_file_dict_copy[file_name],
                                    source_range)
            orig_file_dict_copy[file_name] = new_file

        diff_dict = {}
        for file_name in original_file_dict:
            diff_dict[file_name] = Diff.from_string_arrays(
                original_file_dict[file_name],
                orig_file_dict_copy[file_name])

        orig_result_diff_dict_dict[original_result] = diff_dict

    # same thing for modified results. and yes this should really be in a
    # function... but as long as both of these are not, code clone detection
    # won't find them >:)
    # fixme: yeah....

    mod_result_diff_dict_dict = {}
    for modified_result in modified_results:
        mod_file_dict_copy = copy.deepcopy(modified_file_dict)

        for source_range in modified_result.affected_code:
            file_name = source_range.file
            new_file = remove_range(mod_file_dict_copy[file_name],
                                    source_range)
            mod_file_dict_copy[file_name] = new_file

        diff_dict = {}
        for file_name in modified_file_dict:
            diff_dict[file_name] = Diff.from_string_arrays(
                modified_file_dict[file_name],
                mod_file_dict_copy[file_name])

        mod_result_diff_dict_dict[modified_result] = diff_dict

    for m_r in modified_results:
        for o_r in original_results:

            if basics_match(o_r, m_r):
                if source_ranges_match(original_file_dict,
                                       modified_file_dict,
                                       diffs_dict,
                                       o_r,
                                       orig_result_diff_dict_dict[o_r],
                                       m_r,
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

    # we cannot tolerate differences!
    if original_result.origin != modified_result.origin:
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
                        modified_file_dict,
                        diff_dict,
                        original_result,
                        original_result_diff_dict,
                        modified_result,
                        modified_result_diff_dict):
    """
    Checks whether the SourceRanges of two results match

    :param original_file_dict: Dict of lists of file contents before changes
    :param modified_file_dict: Dict of lists of file contents after changes
    :param diff_dict:          Dict of diffs describing the changes per file
    :param original_result:    A result of the old files
    :param original_result_diff_dict: diff for each file for this result
    :param modified_result:    A result of the new files
    :param modified_result_diff_dict: guess
    :return:                     Boolean value whether the SourceRanges match
    """
    for file_name in original_file_dict:

        try:  # fails if the affected range of the result get's modified
            original_total_diff = \
                diff_dict[file_name] + original_result_diff_dict[file_name]
        except ConflictError:
            return False

        # original file with file_diff and original_diff applied
        original_total_file = original_total_diff.modified
        # modified file with modified_diff applied
        modified_total_file = modified_result_diff_dict[file_name].modified
        if original_total_file != modified_total_file:
            return False
    return True


def diffs_match(original_file_dict,
                modified_file_dict,
                diff_dict,
                original_result,
                modified_result):
    """
    Checks whether the Diffs of two results describe the same changes

    :param original_file_dict: Dict of lists of file contents before changes
    :param modified_file_dict: Dict of lists of file contents after changes
    :param diff_dict:          Dict of diffs describing the change in each file
    :param original_result:    A result of the old files
    :param modified_result:    A result of the new files
    :return:                   Boolean value whether the Diffs match
    """
    return False # pragma: no cover


def remove_range(file_contents, source_range):
    """
    removes the chars covered by the sourceRange from the file

    :param file_contents: list of lines in the file
    :param source_range:  Source Range
    :return:              list of file contents without specified chars removed
    """

    # fixme: line or column could be None -.-
    # this is not the fixing it deserves, but the one it needs right now:
    if source_range.start.line is None:
        return copy.deepcopy(file_contents)

    newfile = copy.deepcopy(file_contents)
    # attention: line numbers in the SourceRange are human-readable,
    # list indices start with 0

    if source_range.start.line == source_range.end.line:
        # if it's all in one line, replace the line by it's beginning and end
        newfile[source_range.start.line - 1] = \
            newfile[source_range.start.line - 1][:source_range.start.column-1]\
        + newfile[source_range.start.line - 1][source_range.end.column:]
    else:
        # cut away after start
        newfile[source_range.start.line - 1] = \
            newfile[source_range.start.line - 1][:source_range.start.column-1]

        # cut away before end
        newfile[source_range.end.line - 1] = \
            newfile[source_range.end.line - 1][source_range.end.column:]

        # start: index = first line number ==> line after first line
        # end: index = last line -2 ==> line before last line

        for i in reversed(range(
                source_range.start.line, source_range.end.line -1)):
            del newfile[i]

    return newfile
