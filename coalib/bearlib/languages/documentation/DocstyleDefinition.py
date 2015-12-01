import os.path

from coalib.misc.Compatability import FileNotFoundError
from coalib.misc.Decorators import generate_eq, generate_repr
from coalib.misc.Enum import enum
from coalib.parsing.ConfParser import ConfParser


"""
Possible values for the type/format of the documentation.

- standard:
  The standard doctype is identified by a start, stop and each-line marker. The
  each-line marker specifies the prefix of following lines after the start
  marker.

  For example

  ```
  /**
   * documentation
   */
  ```

  is a standard doctype with the markers `/**`, `*`, `*/`.

- simple:
  Nearly like standard doctype, but there's no each-line marker, just start and
  stop.

  For example

  ```
  '''
  documentation
  '''
  ```

  is a simple doctype with the markers `'''`, `'''`.

- continuous:
  The continuous doctype needs a start and each-line marker. Documentation
  starts with the start marker (obviously) and continues as long as each
  following line has the same prefix like the each-line marker.

  For example

  ```
  ## documentation
  #
  #  more detailed documentation
  ```

  is a continuous doctype with the markers `##`, `#`.
"""
DOCTYPES = enum("standard", "simple", "continuous")


@generate_repr("language",
               "docstyle",
               ("doctype", DOCTYPES.reverse.get),
               "markers")
@generate_eq("language", "docstyle", "doctype", "markers")
class DocstyleDefinition:
    """
    The DocstyleDefinition class holds values that identify a certain type
    of documentation comment (for which language, documentation style/tool
    used, type of documentation and delimiters/markers).
    """

    def __init__(self, language, docstyle, doctype, markers):
        """
        Instantiates a new DocstyleDefinition.

        :param language: The programming language of the documentation comment.
                         For example `"CPP"` for C++ or `"PYTHON3"` for
                         Python 3.
                         The given string is automatically lowered, so passing
                         i.e. "CPP" or "cpp" makes no difference.
        :param docstyle: The documentation style/tool used to document code.
                         For example `"default"` or `"doxygen"`.
                         The given string is automatically lowered, so passing
                         i.e. "default" or "DEFAULT" makes no difference.
        :param doctype:  The type/format of the documentation. Needs to be a
                         value of the enumeration `DOCTYPES`.
        :param markers:  A tuple of marker/delimiter strings that identify the
                         documentation comment. See `DOCTYPES` for more
                         information about doctype markers.
        """
        self._language = language.lower()
        self._docstyle = docstyle.lower()
        self._doctype = doctype
        self._markers = markers

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
    def doctype(self):
        """
        The type/format of the documentation.

        :return: A value from `DOCTYPES` enumeration.
        """
        return self._doctype

    @property
    def markers(self):
        """
        The string markers that identify a documentation comment.

        See `DOCTYPES` for more information about doctype markers.

        :return: A tuple of marker/delimiter strings that identify the
                 documentation comment.
        """
        return self._markers

    @staticmethod
    def _get_prefixed_settings(settings, prefix):
        """
        Retrieves all settings with their name matching the given prefix.

        :param settings: The settings dictionary to search in.
        :param prefix:   The prefix all returned settings shall have.
        :return:         A dict with setting-names as keys and setting-values
                         as values.
        """
        return {setting : settings[setting]
                for setting in filter(lambda x: x.startswith(prefix),
                                      settings)}

    @classmethod
    def load(cls, language, docstyle):
        """
        Yields all DocstyleDefinition's defined for the given language and
        docstyle from the coala docstyle definition files.

        The marker settings are loaded from the according coalang-files and are
        prefixed like this:

        `doc-marker-<DOCTYPE>`

        where <DOCTYPE> is a value of the enumeration `DOCTYPES`.

        :param language:           The programming language. For example
                                   `"CPP"` for C++ or `"PYTHON3"` for Python 3.
        :param docstyle:           The documentation style/tool used. For
                                   example `"default"` or `"doxygen"`.
        :raises FileNotFoundError: Raised when the given docstyle was not
                                   found. This is a compatability exception
                                   from `coalib.misc.Compatability` module.
        :raises KeyError:          Raised when the given language is not
                                   defined for given docstyle.
        :return:                   An iterator yielding `DocstyleDefinition`s
                                   for given language and docstyle.
        """

        try:
            docstyle_settings = ConfParser().parse(os.path.dirname(__file__) +
                                                   "/" + docstyle.lower() +
                                                   ".coalang")
        except FileNotFoundError as ex:
            raise type(ex)("Docstyle definition " + repr(docstyle) +
                           " not found.")

        try:
            docstyle_settings = docstyle_settings[language.lower()]
        except KeyError:
            raise KeyError("Language {} is not defined for docstyle {}."
                           .format(repr(language), repr(docstyle)))

        for doctype in DOCTYPES.str_dict:
            settings = DocstyleDefinition._get_prefixed_settings(
                docstyle_settings,
                "doc-marker-" + doctype)

            for marker_setting in settings.values():
                yield cls(language,
                          docstyle,
                          DOCTYPES.str_dict[doctype],
                          tuple(marker_setting))
