from collections import Iterable, namedtuple
from glob import iglob
import os.path

from coala_utils.decorators import (
    enforce_signature, generate_eq, generate_repr)
from coalib.parsing.ConfParser import ConfParser


@generate_repr()
@generate_eq("language", "docstyle", "markers")
class DocstyleDefinition:
    """
    The DocstyleDefinition class holds values that identify a certain type of
    documentation comment (for which language, documentation style/tool used
    etc.).
    """
    Metadata = namedtuple("Metadata", ("param_start", "param_end",
                                       "return_sep"))

    @enforce_signature
    def __init__(self, language: str, docstyle: str, markers: (Iterable, str),
                 metadata: Metadata):
        """
        Instantiates a new DocstyleDefinition.

        :param language: The case insensitive programming language of the
                         documentation comment, e.g. ``"CPP"`` for C++ or
                         ``"PYTHON3"``.
        :param docstyle: The case insensitive documentation style/tool used
                         to document code, e.g. ``"default"`` or ``"doxygen"``.
        :param markers:  An iterable of marker/delimiter string iterables
                         or a single marker/delimiter string iterable that
                         identify a documentation comment. See ``markers``
                         property for more details on markers.
        :param metadata: A namedtuple consisting of certain attributes that
                         form the layout of the certain documentation comment
                         e.g. ``param_start`` defining the start symbol of
                         the parameter fields and ``param_end`` defining the
                         end.
        """
        self._language = language.lower()
        self._docstyle = docstyle.lower()

        # Check and modify tuple if only one marker_set exists.
        markers = tuple(markers)
        if len(markers) == 3 and all(isinstance(x, str) for x in markers):
            markers = (markers,)

        self._markers = tuple(tuple(marker_set) for marker_set in markers)

        # Check marker set dimensions.
        for marker_set in self._markers:
            length = len(marker_set)
            if length != 3:
                raise ValueError("Length of a given marker set was not 3 (was "
                                 "actually {}).".format(length))

        self._metadata = metadata

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
        ``(("/**", "*", "*/"),)`` would match following documentation comment:

        ::

            /**
             * This is documentation.
             */

        It's also possible to supply an empty each-line marker
        (``("/**", "", "*/")``):

        ::

            /**
             This is more documentation.
             */

        Markers are matched "greedy", that means it will match as many
        each-line markers as possible. I.e. for ``("///", "///", "///")``):

        ::

            /// Brief documentation.
            ///
            /// Detailed documentation.

        :return: A tuple of marker/delimiter string tuples that identify a
                 documentation comment.
        """
        return self._markers

    @property
    def metadata(self):
        """
        A namedtuple of certain attributes present in the documentation.

        These attributes are used to define parts of the documentation.
        """
        return self._metadata

    @classmethod
    @enforce_signature
    def load(cls, language: str, docstyle: str, coalang_dir=None):
        """
        Loads a ``DocstyleDefinition`` from the coala docstyle definition files.

        This function considers all settings inside the according coalang-files
        as markers, except ``param_start``, ``param_end`` and ``return_sep``
        which are considered as special metadata markers.

        .. note::

            When placing new coala docstyle definition files, these must
            consist of only lowercase letters and end with ``.coalang``!

        :param language:           The case insensitive programming language of
                                   the documentation comment as a string.
        :param docstyle:           The case insensitive documentation
                                   style/tool used to document code, e.g.
                                   ``"default"`` or ``"doxygen"``.
        :param coalang_dir:        Path to directory with coalang docstyle
                                   definition files. This replaces the default
                                   path if given.
        :raises FileNotFoundError: Raised when the given docstyle was not
                                   found.
        :raises KeyError:          Raised when the given language is not
                                   defined for given docstyle.
        :return:                   The ``DocstyleDefinition`` for given language
                                   and docstyle.
        """

        docstyle = docstyle.lower()

        language_config_parser = ConfParser(remove_empty_iter_elements=False)

        coalang_file = os.path.join(
            coalang_dir or os.path.dirname(__file__), docstyle + ".coalang")

        try:
            docstyle_settings = language_config_parser.parse(coalang_file)
        except FileNotFoundError:
            raise FileNotFoundError("Docstyle definition " + repr(docstyle) +
                                    " not found.")

        language = language.lower()

        try:
            docstyle_settings = docstyle_settings[language]
        except KeyError:
            raise KeyError("Language {!r} is not defined for docstyle {!r}."
                           .format(language, docstyle))

        metadata_settings = ("param_start", "param_end", "return_sep")

        metadata = cls.Metadata(*(str(docstyle_settings.get(req_setting, ""))
                                  for req_setting in metadata_settings))

        marker_sets = (tuple(value)
                       for key, value in
                       docstyle_settings.contents.items()
                       if key not in metadata_settings and
                       not key.startswith("comment"))

        return cls(language, docstyle, marker_sets, metadata)

    @staticmethod
    def get_available_definitions():
        """
        Returns a sequence of pairs with ``(docstyle, language)`` which are
        available when using ``load()``.

        :return: A sequence of pairs with ``(docstyle, language)``.
        """
        language_config_parser = ConfParser(remove_empty_iter_elements=False)
        pattern = os.path.join(os.path.dirname(__file__), "*.coalang")

        for coalang_file in iglob(pattern):
            docstyle = os.path.splitext(os.path.basename(coalang_file))[0]
            # Ignore files that are not lowercase, as coalang files have to be.
            if docstyle.lower() == docstyle:
                for language in language_config_parser.parse(coalang_file):
                    yield docstyle, language.lower()
