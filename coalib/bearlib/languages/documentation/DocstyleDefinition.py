from coalib.misc.Decorators import generate_eq, generate_repr


@generate_repr()
@generate_eq("language", "docstyle", "markers")
class DocstyleDefinition:
    """
    The DocstyleDefinition class holds values that identify a certain type of
    documentation comment (for which language, documentation style/tool used
    etc.).
    """

    def __init__(self, language, docstyle, markers):
        """
        Instantiates a new DocstyleDefinition.

        :param language: The case insensitive programming language of the
                         documentation comment, e.g. `"CPP"` for C++ or
                         `"PYTHON3"`.
        :param docstyle: The case insensitive documentation style/tool used
                         to document code, e.g. `"default"` or `"doxygen"`.
        :param markers:  An iterable of marker/delimiter string iterables that
                         identify a documentation comment. See `markers`
                         property for more details on markers.
        """
        self._language = language.lower()
        self._docstyle = docstyle.lower()
        self._markers = tuple(tuple(marker_set) for marker_set in markers)

        # Check marker set dimensions.
        for marker_set in self._markers:
            length = len(marker_set)
            if length != 3:
                raise ValueError("Length of a given marker set was not 3 (was "
                                 "actually {}).".format(length))

    @property
    def language(self):
        """
        The programming language.

        :return: A lower-case string defining the programming language (i.e.
                 "cpp" or "python").
        """
        return self._language

    @property
    def docstyle(self):
        """
        The documentation style/tool used to document code.

        :return: A lower-case string defining the docstyle (i.e. "default" or
                 "doxygen").
        """
        return self._docstyle

    @property
    def markers(self):
        """
        A tuple of marker sets that identify a documentation comment.

        Marker sets consist of 3 entries where the first is the start-marker,
        the second one the each-line marker and the last one the end-marker.
        For example a marker tuple with a single marker set
        `(("/**", "*", "*/"),)` would match following documentation comment:

        ```
        /**
         * This is documentation.
         */
        ```

        It's also possible to supply an empty each-line marker
        (`("/**", "", "*/")`):

        ```
        /**
         This is more documentation.
         */
        ```

        Markers are matched "greedy", that means it will match as many
        each-line markers as possible. I.e. for `("///", "///", "///")`):

        ```
        /// Brief documentation.
        ///
        /// Detailed documentation.
        ```

        :return: A tuple of marker/delimiter string tuples that identify a
                 documentation comment.
        """
        return self._markers
