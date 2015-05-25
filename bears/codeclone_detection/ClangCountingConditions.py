"""
This file contains counting conditions for use for count matrix based code
clone detection. (See http://goo.gl/8UuAW5 for general information about the
algorithm.)
"""


from coalib.bearlib.parsing.clang.cindex import CursorKind
from coalib.misc.Enum import enum


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
    Checks if the stack contains a cursor which is of the given kind and the
    stack also has a child of this element which number is in the allowed_nums
    list.

    :param stack:        The stack holding a tuple holding the parent cursors
                         and the child number.
    :param allowed_nums: List/iterator of child numbers allowed.
    :param kind:         The kind of the parent element.
    :return:             Number of matches.
    """
    is_kind_child = False
    count = 0
    for elem, child_num in stack:
        if is_kind_child and child_num in allowed_nums:
            count += 1

        if elem.kind == kind:
            is_kind_child = True
        else:
            is_kind_child = False

    return count


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


def _get_binop_operator(cursor):
    """
    Returns the operator token of a binary operator cursor.

    :param cursor: A cursor of kind BINARY_OPERATOR.
    :return:       The token object containing the actual operator or None.
    """
    children = list(cursor.get_children())
    operator_min_begin = (children[0].location.line,
                          children[0].location.column)
    operator_max_end = (children[1].location.line,
                        children[1].location.column)

    for token in cursor.get_tokens():
        if (operator_min_begin < (token.extent.start.line,
                                  token.extent.start.column) and
            operator_max_end >= (token.extent.end.line,
                                token.extent.end.column)):
            return token

    return None  # pragma: no cover


def _stack_contains_operators(stack, operators):
    """
    Checks if one of the given operators is within the stack.

    :param stack:     The stack holding a tuple holding the parent cursors
                      and the child number.
    :param operators: A list of strings. E.g. ["+", "-"]
    :return:          True if the operator was found.
    """
    for elem, child_num in stack:
        if elem.kind in [CursorKind.BINARY_OPERATOR,
                         CursorKind.COMPOUND_ASSIGNMENT_OPERATOR]:
            operator = _get_binop_operator(elem)
            # Not known how to reproduce but may be possible when evil macros
            # join the game.
            if operator is None:  # pragma: no cover
                continue

            if operator.spelling.decode() in operators:
                return True

    return False


ARITH_BINARY_OPERATORS = ['+', '-', '*', '/', '%', '&', '|']
COMPARISION_OPERATORS = ["==", "<=", ">=", "<", ">", "!=", "&&", "||"]
ADV_ASSIGNMENT_OPERATORS = [op + "=" for op in ARITH_BINARY_OPERATORS]
ASSIGNMENT_OPERATORS = ["="] + ADV_ASSIGNMENT_OPERATORS


def in_sum(cursor, stack):
    """
    A counting condition returning true if the variable is used in a sum
    statement, i.e. within the operators +, - and their associated compound
    operators.
    """
    return _stack_contains_operators(stack, ['+', '-', '+=', '-='])


def in_product(cursor, stack):
    """
    A counting condition returning true if the variable is used in a product
    statement, i.e. within the operators *, /, % and their associated compound
    operators.
    """
    return _stack_contains_operators(stack, ['*', '/', '%', '*=', '/=', '%='])


def in_binary_operation(cursor, stack):
    """
    A counting condition returning true if the variable is used in a binary
    operation, i.e. within the operators |, & and their associated compound
    operators.
    """
    return _stack_contains_operators(stack, ['&', '|', '&=', '|='])


def member_accessed(cursor, stack):
    return _stack_contains_kind(stack, CursorKind.MEMBER_REF_EXPR)


def used(cursor, stack):
    return True


def returned(cursor, stack):
    return _stack_contains_kind(stack, CursorKind.RETURN_STMT)


def is_inc_or_dec(cursor, stack):
    for elem, child_num in stack:
        if elem.kind == CursorKind.UNARY_OPERATOR:
            for token in elem.get_tokens():
                if token.spelling.decode() in ["--", "++"]:
                    return True

    return False


def is_condition(cursor, stack):
    return (_is_nth_child_of_kind(stack, [0], CursorKind.WHILE_STMT) != 0 or
            _is_nth_child_of_kind(stack, [0], CursorKind.IF_STMT) != 0 or
            FOR_POSITION.COND in _get_positions_in_for_loop(cursor, stack))


def in_condition(cursor, stack):
    # In every case the first child of IF_STMT is the condition itself
    # (non-NULL) so the second and third child are in the then/else branch
    return _is_nth_child_of_kind(stack, [1, 2], CursorKind.IF_STMT) == 1


def in_second_level_condition(cursor, stack):
    return _is_nth_child_of_kind(stack, [1, 2], CursorKind.IF_STMT) == 2


def in_third_level_condition(cursor, stack):
    return _is_nth_child_of_kind(stack, [1, 2], CursorKind.IF_STMT) > 2


def is_assignee(cursor, stack):
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
                        token.spelling.decode() in ASSIGNMENT_OPERATORS and
                        cursor_pos <= token_pos):
                    return True

    return is_inc_or_dec(cursor, stack)


def is_assigner(cursor, stack):
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
                if (token.spelling.decode() in ASSIGNMENT_OPERATORS and (
                        token_pos <= cursor_pos or
                        token.spelling.decode() != "=")):
                    return True

    return is_inc_or_dec(cursor, stack)


def _loop_level(cursor, stack):
    positions_in_for = _get_positions_in_for_loop(cursor, stack)
    return (positions_in_for.count(FOR_POSITION.INC) +
            positions_in_for.count(FOR_POSITION.BODY) +
            _is_nth_child_of_kind(stack, [1], CursorKind.WHILE_STMT))


def loop_content(cursor, stack):
    return _loop_level(cursor, stack) == 1


def second_level_loop_content(cursor, stack):
    return _loop_level(cursor, stack) == 2


def third_level_loop_content(cursor, stack):
    return _loop_level(cursor, stack) > 2


def is_param(cursor, stack):
    return cursor.kind == CursorKind.PARM_DECL


condition_dict = {"used": used,
                  "returned": returned,
                  "is_condition": is_condition,
                  "in_condition": in_condition,
                  "in_second_level_condition": in_second_level_condition,
                  "in_third_level_condition": in_third_level_condition,
                  "is_assignee": is_assignee,
                  "is_assigner": is_assigner,
                  "loop_content": loop_content,
                  "second_level_loop_content": second_level_loop_content,
                  "third_level_loop_content": third_level_loop_content,
                  "is_param": is_param,
                  "in_sum": in_sum,
                  "in_product": in_product,
                  "in_binary_operation": in_binary_operation,
                  "member_accessed": member_accessed}


def counting_condition(value):
    """
    This is a custom converter to convert a setting from coala into counting
    condition function objects for this bear only.

    :param value: An object that can be converted to a list.
    :return:      A list of functions (counting conditions)
    """
    str_list = list(value)
    result_list = []
    for elem in str_list:
        result_list.append(condition_dict.get(elem.lower()))

    return result_list
