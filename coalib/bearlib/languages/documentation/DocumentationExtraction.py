from warnings import warn

from coalib.bearlib.languages.documentation import get_docstyle_configuration
from coalib.parsing.StringProcessing import search_in_between


def _get_prefixed_settings(settings, prefix):
    """
    Retrieves all settings with their name matching the given prefix.

    :param settings: The settings dictionary to search in.
    :param prefix:   The prefix all returned settings shall have.
    :return:         A dict with setting-names as keys and setting-values as
                     values.
    """
    return {setting : settings[setting]
            for setting in filter(lambda x: x.startswith(prefix), settings)}


def extract_documentation(content, language, docstyle):
    """
    Extracts all documentation texts inside the given source-code-string.

    This function supports three different extraction modes:
    - standard:
      The standard modes needs a start, stop and each-line marker. The
      each-line marker specifies the prefix of following lines after the start
      marker.
    - simple:
      Nearly like standard mode, but there's no each-line marker, just start
      and stop.
    - continuous:
      The continuous mode needs a start and each-line marker. Documentation
      starts with the start marker (obviously) and continues as long as each
      following line has the same prefix like the each-line marker.

    The marker settings are loaded from the according coalang-files and are
    prefixed like this:

    `doc-marker-<MODE>`

    where <MODE> is one of the above mentioned extraction modes (standard,
    simple, continuous).

    :param content:  The source-code-string where to extract documentation
                     from.
    :param language: The programming language used.
    :param docstyle: The documentation style/tool used (i.e. doxygen).
    :return:         An iterator returning each documentation text found in the
                     content.
    """
    docstyle_settings = get_docstyle_configuration(language, docstyle)

    # Search for each setting with the prefix 'doc-marker' following the
    # appropriate mode.
    modes = ("standard", "simple", "continuous")
    markers = tuple(_get_prefixed_settings(docstyle_settings,
                                           "doc-marker-" + mode)
                    for mode in modes)

    markers_standard, markers_simple, markers_continuous = markers

    # standard mode.
    for setting, marker in markers_standard.items():
        try:
            marker_start, marker_eachline, marker_stop = marker

            for match in search_in_between(marker_start, marker_stop, content):
                it = iter(match.splitlines(keepends=True))
                docstring = next(it)
                docstring += "".join(line.lstrip(" \t")
                                     .replace(marker_eachline, "", 1)
                                     for line in it)

                yield docstring

        # Raised when unpacking values from 'marker' fails.
        except ValueError:
            warn(
                "Setting {} for language {} defined in docstyle {} has an "
                "invalid format. It has to be a three-element tuple. For more "
                "information about documentation extraction settings see "
                "`extract_documentation`.\n"
                "Skipping this marker setting.".format(repr(setting),
                                                       repr(language),
                                                       repr(docstyle)),
                ResourceWarning)

    # simple mode.
    for setting, marker in markers_simple.items():
        try:
            marker_start, marker_stop = marker

            for match in search_in_between(marker_start, marker_stop, content):
                it = iter(match.splitlines(keepends=True))
                docstring = next(it)
                docstring += "".join(line.lstrip(" \t") for line in it)

                yield docstring

        except ValueError:
            warn(
                "Setting {} for language {} defined in docstyle {} has an "
                "invalid format. It has to be a two-element tuple. For more "
                "information about documentation extraction settings see "
                "`extract_documentation`.\n"
                "Skipping this marker setting.".format(repr(setting),
                                                       repr(language),
                                                       repr(docstyle)),
                ResourceWarning)

    # continuous mode.
    for setting, marker in markers_continuous.items():
        try:
            marker_start, marker_ongoing = marker

            pos = content.find(marker_start)
            while pos != -1:
                it = iter(content[pos + len(marker_start):]
                          .splitlines(keepends=True))

                docstring = next(it)
                pos += len(marker_start) + len(docstring)

                for line in it:
                    lstripped_line = line.lstrip(" \t")
                    # Search until the ongoing-marker runs out.
                    if lstripped_line.startswith(marker_ongoing):
                        docstring += lstripped_line[len(marker_ongoing):]
                    else:
                        break

                    pos += len(line)

                yield docstring

                pos = content.find(marker_start, pos)

        except ValueError:
            warn(
                "Setting {} for language {} defined in docstyle {} has an "
                "invalid format. It has to be a two-element tuple. For more "
                "information about documentation extraction settings see "
                "`extract_documentation`.\n"
                "Skipping this marker setting.".format(repr(setting),
                                                       repr(language),
                                                       repr(docstyle)),
                ResourceWarning)
