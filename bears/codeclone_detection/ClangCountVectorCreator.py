from bears.codeclone_detection.CountVector import CountVector
from bears.codeclone_detection.ClangCountingConditions import (
    is_reference,
    get_identifier_name,
    is_literal,
    is_function_declaration)
from coalib.bearlib.parsing.clang.cindex import Cursor, Index


class ClangCountVectorCreator:
    """
    This object uses clang to create a count vector for each function for given
    counting conditions. The counting conditions are clang specific and they
    are called like this:

      condition(stack)

    While stack is a stack (i.e. list) holding a tuple holding the parent
    cursors and the child number. (E.g. if a cursor is the third child of
    its parent its child number is two, counted from zero.)

    The ClangCountVectorCreator will only count variables local to each
    function.
    """
    def __init__(self,
                 conditions=None,
                 weightings=None):
        """
        Creates a new ClangCountVectorCreator.

        :param conditions:      The counting conditions as list of function
                                objects, each shall return true when getting
                                data indicating that this occurrence should
                                be counted.
        :param weightings:      Optional factors to weight counting conditions.
                                Defaults to 1 for all conditions.
        """
        self.conditions = conditions
        self.weightings = weightings
        self.count_vectors = {}
        self.stack = []

    def count_identifier(self, identifier):
        if identifier not in self.count_vectors:
            self.count_vectors[identifier] = (
                CountVector(identifier, self.conditions, self.weightings))

        self.count_vectors[identifier].count_reference(self.stack)

    def _get_vector_for_function(self, cursor, child_num=0):
        """
        Creates a CountVector object for the given cursor.

        Note: this function uses self.count_vectors for storing its results.
        This is done knowingly because passing back and forth mutable objects
        is not nice and yields in bigger complexity IMHO.

        This function creates a CountVector object for all variables found in
        self.local_vars and in the tree elements below the given one, stores it
        in self.count_vectors.

        :param cursor: Clang cursor to iterate over.
        """
        assert isinstance(cursor, Cursor)
        self.stack.append((cursor, child_num))

        if is_reference(cursor):
            self.count_identifier(get_identifier_name(cursor))
        if is_literal(cursor):
            tokens = list(cursor.get_tokens())
            if tokens:
                # Mangle constants with $ (-> no valid C identifier), first
                # token is the constant, semicolon and similar things may
                # follow, don't want them
                self.count_identifier("#" + tokens[0].spelling.decode())

        for i, child in enumerate(cursor.get_children()):
            self._get_vector_for_function(child, i)

        self.stack.pop()

    def _get_vectors_for_cursor(self, cursor, filename):
        """
        Maps all functions in/under the given cursor to their count vectors
        if they are defined in the given file.

        :param cursor:   The cursor to traverse.
        :param filename: Absolute path to the file.
        :return:         The dictionary holding CountVectors for all variables
                         in all functions.
        """
        assert isinstance(cursor, Cursor)
        file = cursor.location.file
        if file is not None:
            file = file.name.decode()

        if str(file) == str(filename) and is_function_declaration(cursor):
            self._get_vector_for_function(cursor)

            result = {(cursor.extent.start.line,
                       get_identifier_name(cursor)): self.count_vectors}
            # Reset local states
            self.count_vectors = {}
            self.stack = []
        else:
            result = {}
            for child in cursor.get_children():
                result.update(self._get_vectors_for_cursor(child, filename))

        return result

    def get_vectors_for_file(self, filename, include_paths=()):
        """
        Creates a dictionary associating each function name within the given
        file with another dictionary associating each variable name (local to
        the function) with a CountVector object. Functions of included files
        will not be analyzed.

        :param filename: The path to the file to parse.
        :return:         The dictionary holding CountVectors for all variables
                         in all functions.
        """
        args = ["-I"+path for path in include_paths]
        root = Index.create().parse(filename, args=args).cursor

        return self._get_vectors_for_cursor(root, filename)
