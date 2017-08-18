from collections import Iterable, namedtuple
from glob import iglob
import os.path

from coala_utils.decorators import (
    enforce_signature, generate_eq, generate_repr)
from coalib.parsing.ConfParser import ConfParser


@generate_repr()
@generate_eq('language', 'docstyle', 'markers')
class DocstyleDefinition:
    """
    The DocstyleDefinition class holds values that identify a certain type of
    documentation comment (for which language, documentation style/tool used
    etc.).
    """
    Metadata = namedtuple('Metadata', ('param_start', 'param_end',
                                       'exception_start', 'exception_end',
                                       'return_sep'))
    ClassPadding = namedtuple('ClassPadding',
                              ('top_padding', 'bottom_padding'))
    FunctionPadding = namedtuple('FunctionPadding',
                                 ('top_padding', 'bottom_padding'))
    DocstringTypeRegex = namedtuple('DocstringTypeRegex',
                                    ('class_sign', 'func_sign'))

    @enforce_signature
    def __init__(self, language: str, docstyle: str, markers: (Iterable, str),
                 metadata: Metadata, class_padding: ClassPadding,
                 function_padding: FunctionPadding,
                 docstring_type_regex: DocstringTypeRegex,
                 docstring_position: str):
        """
        Instantiates a new DocstyleDefinition.

        :param language:
            The case insensitive programming language of the
            documentation comment, e.g. ``"CPP"`` for C++ or
            ``"PYTHON3"``.
        :param docstyle:
            The case insensitive documentation style/tool used
            to document code, e.g. ``"default"`` or ``"doxygen"``.
        :param markers:
            An iterable of marker/delimiter string iterables
            or a single marker/delimiter string iterable that
            identify a documentation comment. See ``markers``
            property for more details on markers.
        :param metadata:
            A namedtuple consisting of certain attributes that
            form the layout of the certain documentation comment
            e.g. ``param_start`` defining the start symbol of
            the parameter fields and ``param_end`` defining the
            end.
        :param class_padding:
            A namedtuple consisting of values about
            blank lines before and after the documentation of
            ``docstring_type`` class.
        :param function_padding:
            A namedtuple consisting of values about
            blank lines before and after the documentation of
            ``docstring_type`` function.
        :param docstring_type_regex:
            A namedtuple consisting of regex
            about ``class`` and ``function`` of a language, which
            is used to determine ``docstring_type`` of
            DocumentationComment.
        :param docstring_position:
            Defines the position where the regex of
            docstring type is present(i.e. ``top`` or ``bottom``).
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
                raise ValueError('Length of a given marker set was not 3 (was '
                                 'actually {}).'.format(length))

        self._metadata = metadata
        self._class_padding = class_padding
        self._function_padding = function_padding
        self._docstring_type_regex = docstring_type_regex
        self._docstring_position = docstring_position

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

    @property
    def class_padding(self):
        """
        A namedtuple ``ClassPadding`` consisting of values about blank lines
        before and after the documentation of ``docstring_type`` class.

        These values are official standard of following blank lines before and
        after the documentation of ``docstring_type`` class.
        """
        return self._class_padding

    @property
    def function_padding(self):
        """
        A namedtuple ``FunctionPadding`` consisting of values about blank
        lines before and after the documentation of ``docstring_type``
        function.

        These values are official standard of following blank lines before and
        after the documentation of ``docstring_type`` function.
        """
        return self._function_padding

    @property
    def docstring_type_regex(self):
        """
        A namedtuple ``DocstringTypeRegex`` consisting of regex about ``class``
        and ``function`` of a language, which is used to determine
        ``docstring_type`` of DocumentationComment.
        """
        return self._docstring_type_regex

    @property
    def docstring_position(self):
        """
        Defines the position, where the regex of docstring type is present.
        Depending on different languages the docstrings are present below or
        above the defined class or function. This expicitly defines where the
        class regex or function regex is present(i.e. ``top`` or ``bottom``).
        """
        return self._docstring_position

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
            coalang_dir or os.path.dirname(__file__), docstyle + '.coalang')

        try:
            docstyle_settings = language_config_parser.parse(coalang_file)
        except FileNotFoundError:
            raise FileNotFoundError('Docstyle definition ' + repr(docstyle) +
                                    ' not found.')

        language = language.lower()

        try:
            docstyle_settings = docstyle_settings[language]
        except KeyError:
            raise KeyError('Language {!r} is not defined for docstyle {!r}.'
                           .format(language, docstyle))

        metadata_settings = ('param_start', 'param_end',
                             'exception_start', 'exception_end',
                             'return_sep')

        metadata = cls.Metadata(*(str(docstyle_settings.get(req_setting, ''))
                                  for req_setting in metadata_settings))

        try:
            class_padding = cls.ClassPadding(
                *(int(padding) for padding in tuple(
                    docstyle_settings['class_padding'])))
        except IndexError:
            class_padding = cls.ClassPadding('', '')

        try:
            function_padding = cls.FunctionPadding(
                *(int(padding) for padding in tuple(
                    docstyle_settings['function_padding'])))
        except IndexError:
            function_padding = cls.FunctionPadding('', '')

        try:
            docstring_type_regex = cls.DocstringTypeRegex(
                *(str(sign) for sign in tuple(
                    docstyle_settings['docstring_type_regex'])))
        except IndexError:
            docstring_type_regex = cls.DocstringTypeRegex('', '')

        try:
            docstring_position = docstyle_settings['docstring_position'].value
        except IndexError:
            docstring_position = ''

        ignore_keys = (('class_padding', 'function_padding',
                        'docstring_type_regex', 'docstring_position') +
                       metadata_settings)

        marker_sets = (tuple(value)
                       for key, value in
                       docstyle_settings.contents.items()
                       if key not in ignore_keys and
                       not key.startswith('comment'))

        return cls(language, docstyle, marker_sets, metadata, class_padding,
                   function_padding, docstring_type_regex, docstring_position)

    @staticmethod
    def get_available_definitions():
        """
        Returns a sequence of pairs with ``(docstyle, language)`` which are
        available when using ``load()``.

        :return: A sequence of pairs with ``(docstyle, language)``.
        """
        pattern = os.path.join(os.path.dirname(__file__), '*.coalang')

        for coalang_file in iglob(pattern):
            docstyle = os.path.splitext(os.path.basename(coalang_file))[0]
            # Ignore files that are not lowercase, as coalang files have to be.
            if docstyle.lower() == docstyle:
                parser = ConfParser(remove_empty_iter_elements=False)
                for language in parser.parse(coalang_file):
                    yield docstyle, language.lower()
