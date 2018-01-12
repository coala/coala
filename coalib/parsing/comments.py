import re


IGNORE_REGEX = r'\s(\wgnore|\woqa)(\s\S+)+'


def read_ignore_comments(original_line, start_comment, end_comment=''):
    """
    Read Ignore Comment(s) already present in the line.

    :param original_line: Searching for ignore statements is done in this line.
    :param start_comment: Comment delimiter used at the start of comment.
    :param end_comment:   Comment delimiter used at the end of comment in case
                          of multiline comments.
    :return:              List of bears ignored using ignore comments.
    """
    if start_comment not in original_line:
        return

    if end_comment is not '':
        end_comment = ' ' + end_comment

    ignore_regex = re.compile(re.escape(start_comment) + IGNORE_REGEX
                              + re.escape(end_comment))
    ignore_comments = [ignore_comment.group() for ignore_comment in
                       ignore_regex.finditer(original_line.rstrip())]
    ignored_bear_list = []

    for ignore_comment in ignore_comments:
        ignore = ignore_comment.replace(',', '').replace('and ', '')
        ignored_bears = ignore.split()[2:]
        if end_comment is not '':
            ignored_bears.pop()
        for bear in ignored_bears:
            ignored_bear_list.append(bear)

    return ignored_bear_list
