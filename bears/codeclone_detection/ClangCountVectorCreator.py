import os
from bears.codeclone_detection.CountVector import CountVector
from coalib.bearlib.parsing.clang.cindex import Cursor, CursorKind, Index


def get_include_paths(file_path, setting_path):
    """
    Creates a list of include paths that likely resolve all includes.

    :param file_path:    The path to the file to analyze.
    :param setting_path: The path of the coafile.
    :return:             All directories that lie in between the common subpath
                         of those two and the file_path.
    """
    path = os.path.dirname(os.path.commonprefix(
        [os.path.abspath(file_path), os.path.abspath(setting_path)]))
    result = [path]
    for directory in file_path[len(path)+1:].split(os.path.sep)[:-1]:
        path = os.path.join(path, directory)
        result.append(path)

    return result


class ClangCountVectorCreator:
    """
    This object uses clang to create a count vector for each function for given
    counting conditions. The counting conditions are clang specific and they
    are called like this:

      condition(cursor, stack)

    While cursor is a clang cursor and stack is a stack holding a tuple
    holding the parent cursors and the child number. (E.g. if a cursor is
    the third child of its parent its child number is two, counted from zero.)

    The ClangCountVectorCreator will only count variables local to each
    function.
    """
    @staticmethod
    def is_function_declaration(cursor):
        return cursor.kind == CursorKind.FUNCTION_DECL

    @staticmethod
    def is_variable_declaration(cursor):
        return (cursor.kind == CursorKind.VAR_DECL or
                cursor.kind == CursorKind.PARM_DECL)

    @staticmethod
    def get_identifier_name(cursor):
        return cursor.displayname.decode()

    def is_variable_reference(self, cursor):
        return (self.get_identifier_name(cursor) in self.count_vectors and
                (cursor.kind is CursorKind.DECL_REF_EXPR or
                 self.is_variable_declaration(cursor)))

    def __init__(self,
                 conditions=None,
                 weightings=None,
                 definition_path=None):
        """
        Creates a new ClangCountVectorCreator.

        :param conditions:      The counting conditions as list of function
                                objects, each shall return true when getting
                                data indicating that this occurrence should
                                be counted.
        :param weightings:      Optional factors to weight counting conditions.
                                Defaults to 1 for all conditions.
        :param definition_path: section["files"].origin, i.e. the path where
                                the user defined the files. Include paths will
                                be guessed with the help of this information if
                                it is available.
        """
        self.conditions = conditions
        self.weightings = weightings
        self.definition_path = definition_path
        self.count_vectors = {}
        self.stack = []

    def create_count_vector(self, name):
        """
        Creates a new CountVector object with the given name and the metadata
        associated with this object.

        :param name: The name of the variable to count for.
        :return:     The new CountVector object.
        """
        return CountVector(name, self.conditions, self.weightings)

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

        identifier = self.get_identifier_name(cursor)
        if self.is_variable_declaration(cursor):
            self.count_vectors[identifier] = (
                self.create_count_vector(identifier))

        if self.is_variable_reference(cursor):
            self.count_vectors[identifier].count_reference(cursor,
                                                           self.stack)

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

        if str(file) == str(filename) and self.is_function_declaration(cursor):
            self._get_vector_for_function(cursor)

            result = {(cursor.extent.start.line,
                       self.get_identifier_name(cursor)): self.count_vectors}
            # Reset local states
            self.count_vectors = {}
            self.stack = []
        else:
            result = {}
            for child in cursor.get_children():
                result.update(self._get_vectors_for_cursor(child, filename))

        return result

    def get_vectors_for_file(self, filename):
        """
        Creates a dictionary associating each function name within the given
        file with another dictionary associating each variable name (local to
        the function) with a CountVector object. Functions of included files
        will not be analyzed.

        :param filename: The path to the file to parse.
        :return:         The dictionary holding CountVectors for all variables
                         in all functions.
        """
        if self.definition_path is not None:
            include_paths = get_include_paths(filename, self.definition_path)
        else:
            include_paths = []

        args = ["-I"+path for path in include_paths]
        root = Index.create().parse(filename, args=args).cursor

        return self._get_vectors_for_cursor(root, filename)
