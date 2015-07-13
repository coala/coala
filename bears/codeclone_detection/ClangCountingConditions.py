"""
This file contains counting conditions for use for count matrix based code
clone detection. (See http://goo.gl/8UuAW5 for general information about the
algorithm.)
"""


from coalib.bearlib.parsing.clang.cindex import CursorKind
from coalib.misc.Enum import enum


def is_function_declaration(cursor):
    """
    Checks if the given clang cursor is a function declaration.

    :param cursor: A clang cursor from the AST.
    :return:       A bool.
    """
    return cursor.kind == CursorKind.FUNCTION_DECL


def get_identifier_name(cursor):
    """
    Retrieves the identifier name from the given clang cursor.

    :param cursor: A clang cursor from the AST.
    :return:       The identifier as string.
    """
    return cursor.displayname.decode()


def is_literal(cursor):
    """
    :param cursor: A clang cursor from the AST.
    :return:       True if the cursor is a literal of any kind..
    """
    return cursor.kind in [CursorKind.INTEGER_LITERAL,
                           CursorKind.FLOATING_LITERAL,
                           CursorKind.IMAGINARY_LITERAL,
                           CursorKind.STRING_LITERAL,
                           CursorKind.CHARACTER_LITERAL,
                           CursorKind.OBJC_STRING_LITERAL,
                           CursorKind.CXX_BOOL_LITERAL_EXPR,
                           CursorKind.CXX_NULL_PTR_LITERAL_EXPR]


def is_reference(cursor):
    """
    Determines if the cursor is a reference to something, i.e. an identifier
    of a function or variable.

    :param cursor: A clang cursor from the AST.
    :return:       True if the cursor is a reference.
    """
    return cursor.kind in [CursorKind.VAR_DECL,
                           CursorKind.PARM_DECL,
                           CursorKind.DECL_REF_EXPR]


def _stack_contains_kind(stack, kind):
    """
    Checks if a cursor with the given kind is within the stack.

    :param stack: The stack holding a tuple holding the parent cursors and the
                  child number.
    :param kind:  The kind of the cursor to search for.
    :return:      True if the kind was found.
    """
    for elem, dummy in stack:
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


def is_function(stack):
    """
    Checks if the cursor on top of the stack is used as a method or as a
    variable.

    :param stack: A stack holding a tuple holding the parent cursors and the
                  child number.
    :return:      True if this is used as a function, false otherwise.
    """
    return _is_nth_child_of_kind(stack, [0], CursorKind.CALL_EXPR) != 0


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


def _get_positions_in_for_loop(stack):
    """
    Investigates all FOR_STMT objects in the stack and checks for each in
    what position the given cursor is.

    :param cursor: The cursor to investigate.
    :param stack:  The stack of parental cursors.
    :return:       A list of semantic FOR_POSITION's within for loops.
    """
    results = []
    for elem, dummy in stack:
        if elem.kind == CursorKind.FOR_STMT:
            results.append(_get_position_in_for_tokens(
                elem.get_tokens(),
                (stack[-1][0].location.line, stack[-1][0].location.column)))

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
    for elem, dummy in stack:
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


def in_sum(stack):
    """
    A counting condition returning true if the variable is used in a sum
    statement, i.e. within the operators +, - and their associated compound
    operators.
    """
    return _stack_contains_operators(stack, ['+', '-', '+=', '-='])


def in_product(stack):
    """
    A counting condition returning true if the variable is used in a product
    statement, i.e. within the operators *, /, % and their associated compound
    operators.
    """
    return _stack_contains_operators(stack, ['*', '/', '%', '*=', '/=', '%='])


def in_binary_operation(stack):
    """
    A counting condition returning true if the variable is used in a binary
    operation, i.e. within the operators |, & and their associated compound
    operators.
    """
    return _stack_contains_operators(stack, ['&', '|', '&=', '|='])


def member_accessed(stack):
    """
    Returns true if a member of the cursor is accessed or the cursor is the
    accessed member.
    """
    return _stack_contains_kind(stack, CursorKind.MEMBER_REF_EXPR)


# pylint: disabled=unused-argument
def used(stack):
    """
    Returns true.
    """
    return True


def returned(stack):
    """
    Returns true if the cursor on top is used in a return statement.
    """
    return _stack_contains_kind(stack, CursorKind.RETURN_STMT)


def is_inc_or_dec(stack):
    """
    Returns true if the cursor on top is inc- or decremented.
    """
    for elem, dummy in stack:
        if elem.kind == CursorKind.UNARY_OPERATOR:
            for token in elem.get_tokens():
                if token.spelling.decode() in ["--", "++"]:
                    return True

    return False


def is_condition(stack):
    """
    Returns true if the cursor on top is used as a condition.
    """
    return (_is_nth_child_of_kind(stack, [0], CursorKind.WHILE_STMT) != 0 or
            _is_nth_child_of_kind(stack, [0], CursorKind.IF_STMT) != 0 or
            FOR_POSITION.COND in _get_positions_in_for_loop(stack))


def in_condition(stack):
    """
    Returns true if the cursor on top is in the body of one condition.
    """
    # In every case the first child of IF_STMT is the condition itself
    # (non-NULL) so the second and third child are in the then/else branch
    return _is_nth_child_of_kind(stack, [1, 2], CursorKind.IF_STMT) == 1


def in_second_level_condition(stack):
    """
    Returns true if the cursor on top is in the body of two nested conditions.
    """
    return _is_nth_child_of_kind(stack, [1, 2], CursorKind.IF_STMT) == 2


def in_third_level_condition(stack):
    """
    Returns true if the cursor on top is in the body of three or more nested
    conditions.
    """
    return _is_nth_child_of_kind(stack, [1, 2], CursorKind.IF_STMT) > 2


def is_assignee(stack):
    """
    Returns true if the cursor on top is assigned something.
    """
    cursor_pos = (stack[-1][0].extent.end.line, stack[-1][0].extent.end.column)
    for elem, dummy in stack:
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

    return is_inc_or_dec(stack)


def is_assigner(stack):
    """
    Returns true if the cursor on top is used for an assignment on the RHS.
    """
    cursor_pos = (stack[-1][0].extent.start.line,
                  stack[-1][0].extent.start.column)
    for elem, dummy in stack:
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

    return is_inc_or_dec(stack)


def _loop_level(stack):
    """
    Investigates the stack to determine the loop level.

    :param stack: A stack of clang cursors.
    :return:      An integer representing the level of nested loops.
    """
    positions_in_for = _get_positions_in_for_loop(stack)
    return (positions_in_for.count(FOR_POSITION.INC) +
            positions_in_for.count(FOR_POSITION.BODY) +
            _is_nth_child_of_kind(stack, [1], CursorKind.WHILE_STMT))


def loop_content(stack):
    """
    Returns true if the cursor on top is within a first level loop.
    """
    return _loop_level(stack) == 1


def second_level_loop_content(stack):
    """
    Returns true if the cursor on top is within a second level loop.
    """
    return _loop_level(stack) == 2


def third_level_loop_content(stack):
    """
    Returns true if the cursor on top is within a third (or higher) level loop.
    """
    return _loop_level(stack) > 2


def is_param(stack):
    """
    Returns true if the cursor on top is a parameter declaration.
    """
    return stack[-1][0].kind == CursorKind.PARM_DECL


def is_called(stack):
    """
    Yields true if the cursor is a function that is called. (Function pointers
    are counted too.)
    """
    return (_stack_contains_kind(stack, CursorKind.CALL_EXPR) and
            is_function(stack))


def is_call_param(stack):
    """
    Yields true if the cursor is a parameter to another function.
    """
    return (_stack_contains_kind(stack, CursorKind.CALL_EXPR) and
            not is_function(stack))


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
                  "is_called": is_called,
                  "is_call_param": is_call_param,
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
