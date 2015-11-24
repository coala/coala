import copy
import difflib


def basics_match(original_result,
                 modified_result):

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


def _source_ranges_match(original_file,
                         modified_file,
                         original_source_range,
                         modified_source_range):

    # FIXME: performance wants to live, too! (This runs every time... lol -_-)
    diff = difflib.ndiff(original_file, modified_file)

    o0 = copy.copy(original_source_range.start.line)
    o1 = copy.copy(original_source_range.end.line)
    m0 = copy.copy(modified_source_range.start.line)
    m1 = copy.copy(modified_source_range.start.line)

    actual_line_index = 1
    for dline in diff:
        if dline.startswith('?'):
            pass
        elif dline.startswith(' '):
            actual_line_index += 1
        elif dline.startswith('-'):
            if actual_line_index < m0:
                m0 -= 1
                m1 -= 1
            elif actual_line_index <= m1:
                return False
            else:
                break
        elif dline.startswith('+'):
            if actual_line_index <= m0:
                m0 += 1
                m1 += 1
            elif actual_line_index <= m1:
                return False
            else:
                break
            actual_line_index += 1

    return (o0 == m0) and (o1 == m1)


def source_ranges_match(original_file_dict,
                        modified_file_dict,
                        original_result,
                        modified_result):

    # TODO: a long source range could be split into consecutive parts
    source_range_pairs = zip(original_result.affected_code,
                             modified_result.affected_code)

    for source_range_pair in source_range_pairs:
        if not _source_ranges_match(
                original_file_dict[source_range_pair[0].file],
                modified_file_dict[source_range_pair[0].file],
                source_range_pair[0],
                source_range_pair[1]):
            return False
    return True


def diffs_match(original_file_dict,
                modified_file_dict,
                original_result,
                modified_result):
    return True


def everything_matches(original_file_dict,
                       modified_file_dict,
                       original_result,
                       modified_result):

    params = [original_file_dict,
              modified_file_dict,
              original_result,
              modified_result]

    #print("orig: {}\nmod: {}\nbasic: {}\nsr:    {}\ndiffs:{}\n\n".format(
        #original_result, modified_result,
        #basics_match(original_result, modified_result),
        #source_ranges_match(*params),
        #diffs_match(*params)))


    return basics_match(original_result, modified_result) and \
        source_ranges_match(*params) and \
        diffs_match(*params)


def filter_results(original_file_dict,
                   modified_file_dict,
                   original_results,
                   modified_results):
    uniques = [m_r for m_r in modified_results if True not in
               [everything_matches(original_file_dict,
                                   modified_file_dict,
                                   o_r,
                                   m_r) for o_r in original_results]]

    return uniques
