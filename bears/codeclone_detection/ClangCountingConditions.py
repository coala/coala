"""
This file contains counting conditions for use for count matrix based code
clone detection. (See http://goo.gl/8UuAW5 for general information about the
algorithm.)
"""


from coalib.bearlib.parsing.clang.cindex import CursorKind
from coalib.misc.Enum import enum
from coalib.settings.Setting import Setting


def _stack_contains_kind(stack, kind):
    """
    Checks if a cursor with the given kind is within the stack.

    :param stack: The stack holding a tuple holding the parent cursors and the
                  child number.
    :param kind:  The kind of the cursor to search for.
    :return:      True if the kind was found.
    """
    for elem, child_num in stack:
        if elem.kind == kind:
            return True

    return False


def _is_nth_child_of_kind(stack, allowed_nums, kind):
    """
    Checks if the stack contains a cursor with is of the given kind and the
    stack also has a child of this element which number is in the allowed_nums
    list.

    :param stack:        The stack holding a tuple holding the parent cursors
                         and the child number.
    :param allowed_nums: List/iterator of child numbers allowed.
    :param kind:         The kind of the parent element.
    :return:             True if the described situation matches.
    """
    is_kind_child = False
    for elem, child_num in stack:
        if is_kind_child and child_num in allowed_nums:
            return True

        if elem.kind == kind:
            is_kind_child = True
        else:
            is_kind_child = False

    return False


FOR_POSITION = enum("UNKNOWN", "INIT", "COND", "INC", "BODY")


def _get_position_in_for_tokens(tokens, position):
    """
    Retrieves the semantic position of the given position in a for loop. It
    operates under the assumptions that the given tokens represent a for loop
    and that the given position is within the tokens.

    :param tokens:   The tokens representing the for loop (clang extent)
    :param position: A tuple holding (line, column) of the position to
                     identify.
    :return:         A FOR_POSITION object indicating where the position is
                     semantically.
    """
    state = FOR_POSITION.INIT
    next_state = state
    opened_brackets = 0
    for token in tokens:
        if token.spelling.decode() == ";":
            next_state = state + 1
        elif token.spelling.decode() == "(":
            opened_brackets += 1
        elif token.spelling.decode() == ")":
            opened_brackets -= 1
            # Closed bracket for for condition, otherwise syntax error by clang
            if opened_brackets == 0:
                next_state = FOR_POSITION.BODY

        if next_state is not state:
            token_position = (token.extent.start.line,
                              token.extent.start.column)
            if position <= token_position:
                return state
            # Last state, if we reach it the position must be in body
            elif next_state == FOR_POSITION.BODY:
                return next_state

            state = next_state

    # We probably have a macro here, clang doesn't preprocess them. I don't see
    # a chance of getting macros parsed right here in the limited time
    # available. For our heuristic approach we'll just not count for loops
    # realized through macros. FIXME: This is not covered in the tests because
    # it contains a known bug that needs to be fixed, that is: macros destroy
    # everything.
    return FOR_POSITION.UNKNOWN  # pragma: no cover


def _get_positions_in_for_loop(cursor, stack):
    """
    Investigates all FOR_STMT objects in the stack and checks for each in
    what position the given cursor is.

    :param cursor: The cursor to investigate.
    :param stack:  The stack of parental cursors.
    :return:       A list of semantic FOR_POSITION's within for loops.
    """
    results = []
    for elem, child_num in stack:
        if elem.kind == CursorKind.FOR_STMT:
            results.append(_get_position_in_for_tokens(
                elem.get_tokens(),
                (cursor.location.line, cursor.location.column)))

    return results


arith_binary_operators = ['+', '-', '*', '/', '&', '|']
comparision_operators = ["==", "<=", ">=", "<", ">", "!=", "&&", "||"]
adv_assignment_operators = [op + "=" for op in arith_binary_operators]
assignment_operators = ["="] + adv_assignment_operators


def used(cursor, stack):
    return True


def returned(cursor, stack):
    return _stack_contains_kind(stack, CursorKind.RETURN_STMT)


def is_condition(cursor, stack):
    return (_is_nth_child_of_kind(stack, [0], CursorKind.WHILE_STMT) or
            _is_nth_child_of_kind(stack, [0], CursorKind.IF_STMT) or
            FOR_POSITION.COND in _get_positions_in_for_loop(cursor, stack))


def in_condition(cursor, stack):
    # In every case the first child of IF_STMT is the condition itself
    # (non-NULL) so the second and third child are in the then/else branch
    return _is_nth_child_of_kind(stack, [1, 2], CursorKind.IF_STMT)


def is_assignee(cursor, stack):
    # TODO count unary ops like ++/--
    cursor_pos = (cursor.extent.end.line, cursor.extent.end.column)
    for elem, child_num in stack:
        if (
                elem.kind == CursorKind.BINARY_OPERATOR or
                elem.kind == CursorKind.COMPOUND_ASSIGNMENT_OPERATOR):
            for token in elem.get_tokens():
                token_pos = (token.extent.start.line,
                             token.extent.start.column)
                # This needs to be an assignment and cursor has to be on LHS
                if (
                        token.spelling.decode() in assignment_operators and
                        cursor_pos <= token_pos):
                    return True

    return False


def is_assigner(cursor, stack):
    # TODO count unary ops like ++/--
    cursor_pos = (cursor.extent.start.line, cursor.extent.start.column)
    for elem, child_num in stack:
        if (
                elem.kind == CursorKind.BINARY_OPERATOR or
                elem.kind == CursorKind.COMPOUND_ASSIGNMENT_OPERATOR):
            for token in elem.get_tokens():
                token_pos = (token.extent.end.line, token.extent.end.column)
                # This needs to be an assignment and cursor has to be on RHS
                # or if we have something like += its irrelevant on which side
                # it is because += reads on both sides
                if (token.spelling.decode() in assignment_operators and (
                        token_pos <= cursor_pos or
                        token.spelling.decode() != "=")):
                    return True

    return False


def loop_content(cursor, stack):
    positions_in_for = _get_positions_in_for_loop(cursor, stack)
    return (_is_nth_child_of_kind(stack, [1], CursorKind.WHILE_STMT) or
            FOR_POSITION.INC in positions_in_for or
            FOR_POSITION.BODY in positions_in_for)


condition_dict = {"used": used,
                  "returned": returned,
                  "is_condition": is_condition,
                  "in_condition": in_condition,
                  "is_assignee": is_assignee,
                  "is_assigner": is_assigner,
                  "loop_content": loop_content}


def counting_condition(value):
    """
    This is a custom converter to convert a setting from coala into counting
    condition function objects for this bear only.

    :param value: A Setting
    :return:      A list of functions (counting conditions)
    """
    assert isinstance(value, Setting)

    str_list = list(value)
    result_list = []
    for elem in str_list:
        result_list.append(condition_dict.get(elem.lower()))

    return result_list
