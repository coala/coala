import os.path

from coalib.misc.Decorators import generate_repr
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


# TODO Think about automatically lowering case when giving language and
#      docstyle because it's used in file lookup anyway and only the name
#      itself of them is important not the letter-case.
#      Maybe chose also an alternate representation
#      (higher-ing, pre-defined dict i.e.)
@generate_repr("language",
               "docstyle",
               ("doctype", DOCTYPES.reverse.get),
               "markers")
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
        :param docstyle: The documentation style/tool used to document code.
        :param doctype:  The type/format of the documentation. Needs to be a
                         value of the enumeration `DOCTYPES`.
        :param markers:  A tuple of markers/delimiters that identify the
                         documentation comment. See `DOCTYPES` for more
                         information about doctype markers.
        """
        self.language = language
        self.docstyle = docstyle
        self.doctype = doctype
        self.markers = markers

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

        :param language:           The programming language.
        :param docstyle:           The documentation style/tool used.
        :raises FileNotFoundError: Raised when the given docstyle was not
                                   found.
        :raises KeyError:          Raised when the given language is not
                                   defined for given docstyle.
        """

        try:
            docstyle_settings = ConfParser().parse(os.path.dirname(__file__) +
                                                   "/" + docstyle.lower() +
                                                   ".coalang")
        except FileNotFoundError:
            raise FileNotFoundError("Docstyle definition " + repr(docstyle) +
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

    def __eq__(self, other):
        return (other is not None and
                self.doctype == other.doctype and
                self.markers == other.markers and
                self.docstyle.lower() == other.docstyle.lower() and
                self.language.lower() == other.language.lower())
