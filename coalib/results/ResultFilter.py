import copy
from difflib import SequenceMatcher

from coalib.results.Diff import ConflictError, Diff
from coalib.results.SourceRange import SourceRange


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

    renamed_files = ensure_files_present(original_file_dict,
                                         modified_file_dict)
    # diffs_dict[file] is a diff between the original and modified file
    diffs_dict = {}
    for file in original_file_dict:
        diffs_dict[file] = Diff.from_string_arrays(
            original_file_dict[file],
            modified_file_dict[renamed_files.get(file, file)])

    orig_result_diff_dict_dict = remove_result_ranges_diffs(original_results,
                                                            original_file_dict)

    mod_result_diff_dict_dict = remove_result_ranges_diffs(modified_results,
                                                           modified_file_dict)

    unique_results = []

    for m_r in reversed(modified_results):
        unique = True

        for o_r in original_results:

            if basics_match(o_r, m_r):
                if source_ranges_match(original_file_dict,
                                       diffs_dict,
                                       orig_result_diff_dict_dict[o_r],
                                       mod_result_diff_dict_dict[m_r],
                                       renamed_files):

                    # at least one original result matches completely
                    unique = False
                    break
        if unique:
            unique_results.append(m_r)

    return unique_results


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
                        modified_result_diff_dict,
                        renamed_files):
    """
    Checks whether the SourceRanges of two results match

    :param original_file_dict: Dict of lists of file contents before changes
    :param diff_dict:          Dict of diffs describing the changes per file
    :param original_result_diff_dict: diff for each file for this result
    :param modified_result_diff_dict: guess
    :param renamed_files:   A dictionary containing file renamings across runs
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
        modified_total_file = modified_result_diff_dict[
            renamed_files.get(file_name, file_name)].modified
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

    newfile = list(file_contents)
    # attention: line numbers in the SourceRange are human-readable,
    # list indices start with 0

    source_range = source_range.expand(file_contents)

    if source_range.start.line == source_range.end.line:
        # if it's all in one line, replace the line by it's beginning and end
        newfile[source_range.start.line - 1] = (
            newfile[source_range.start.line - 1][:source_range.start.column-1]
            + newfile[source_range.start.line - 1][source_range.end.column:])
        if newfile[source_range.start.line - 1] == "":
            del newfile[source_range.start.line - 1]
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

        # remove leftover empty lines
        # the first line here is actually the former `source_range.end.line -1`
        if newfile[source_range.start.line] == "":
            del newfile[source_range.start.line]
        if newfile[source_range.start.line - 1] == "":
            del newfile[source_range.start.line - 1]

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

        # gather all source ranges from this result
        source_ranges = []

        # SourceRanges must be sorted backwards and overlaps must be eliminated
        # this way, the deletion based on sourceRanges is not offset by
        # previous deletions in the same line that invalidate the indices.
        previous = None

        for source_range in sorted(original_result.affected_code, reverse=True):
            # previous exists and overlaps
            if previous is not None and source_range.overlaps(previous):
                combined_sr = SourceRange.join(previous, source_range)
                previous = combined_sr
            elif previous is None:
                previous = source_range
            # previous exists but it doesn't overlap
            else:
                source_ranges.append(previous)
                previous = source_range
        # don't forget last entry if there were any:
        if previous:
            source_ranges.append(previous)

        for source_range in source_ranges:
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


def ensure_files_present(original_file_dict, modified_file_dict):
    """
    Ensures that all files are available as keys in both dicts.

    :param original_file_dict: Dict of lists of file contents before  changes
    :param modified_file_dict: Dict of lists of file contents after changes
    :return:                   Return a dictionary of renamed files.
    """
    original_files = set(original_file_dict.keys())
    modified_files = set(modified_file_dict.keys())
    affected_files = original_files | modified_files
    original_unique_files = affected_files - modified_files
    renamed_files_dict = {}
    for file in filter(
            lambda filter_file: filter_file not in original_files,
            affected_files):
        for comparable_file in original_unique_files:
            s = SequenceMatcher(
                None,
                ''.join(modified_file_dict[file]),
                ''.join(original_file_dict[comparable_file]))
            if s.real_quick_ratio() >= 0.5 and s.ratio() > 0.5:
                renamed_files_dict[comparable_file] = file
                break
        else:
            original_file_dict[file] = []
    for file in filter(
            lambda filter_file: filter_file not in modified_files,
            affected_files):
        modified_file_dict[file] = []
    return renamed_files_dict
