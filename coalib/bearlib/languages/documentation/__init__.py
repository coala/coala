import os.path

from coalib.parsing.ConfParser import ConfParser


"""
A tuple of all registered docstyles.

After module initialization this turns into a dict, where the keys are the
docstyle names (so the tuple entries already standing here) and the values are
the configuration dictionaries.
"""
docstyles = ()


def get_docstyles():
    """
    Retrieves a dict of all registered docstyle definition files.

    :return: A dict with the docstyle name as keys and the corresponding
             filename as value.
    """
    return {elem : ConfParser().parse(os.path.dirname(__file__) + "/" + elem +
                   ".coalang")
            for elem in docstyles}


def get_docstyle_configuration(language, docstyle):
    """
    Returns the configuration for the given language and docstyle.

    :param language:  The programming language.
    :param docstyle:  The documentation style/tool (i.e. doxygen).
    :raises KeyError: Raised when the docstyle configuration does not exist for
                      given language and docstyle.
    """
    try:
        docstyle_settings = docstyles[docstyle.lower()]
    except KeyError:
        raise KeyError("Docstyle " + repr(docstyle) + " is not registered.")

    try:
        docstyle_settings = docstyle_settings[language.lower()]
    except KeyError:
        raise KeyError("Language {} is not defined for docstyle {}."
                       .format(repr(language), repr(docstyle)))

    return docstyle_settings


docstyles = get_docstyles()
