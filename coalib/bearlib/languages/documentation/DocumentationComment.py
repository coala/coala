from collections import namedtuple

from coala_decorators.decorators import generate_eq, generate_repr


@generate_repr()
@generate_eq("documentation", "language", "docstyle",
             "indent", "marker", "range")
class DocumentationComment:
    """
    The DocumentationComment holds information about a documentation comment
    inside source-code, like position etc.
    """
    Parameter = namedtuple('Parameter', 'name, desc')
    ReturnValue = namedtuple('ReturnValue', 'desc')
    Description = namedtuple('Description', 'desc')

    def __init__(self, documentation, language,
                 docstyle, indent, marker, range):
        """
        Instantiates a new DocumentationComment.

        :param documentation: The documentation text.
        :param language:      The language of the documention.
        :param docstyle:      The docstyle used in the documentation.
        :param indent:        The string of indentation used in front
                              of the first marker of the documentation.
        :param marker:        The three-element tuple with marker strings,
                              that identified this documentation comment.
        :param range:         The position range of type TextRange.
        """
        self.documentation = documentation
        self.language = language.lower()
        self.docstyle = docstyle.lower()
        self.indent = indent
        self.marker = marker
        self.range = range

    def __str__(self):
        return self.documentation

    def parse(self):
        """
        Parses documentation independent of language and docstyle.

        :return:
            The list of all the parsed sections of the documentation. Every
            section is a namedtuple of either ``Description`` or ``Parameter``
            or ``ReturnValue``.
        :raises NotImplementedError:
            When no parsing method is present for the given language and
            docstyle.
        """
        if self.language == "python" and self.docstyle == "default":
            return self._parse_documentation_with_symbols(
                (":param ", ": "), ":return: ")
        elif self.language == "python" and self.docstyle == "doxygen":
            return self._parse_documentation_with_symbols(
                ("@param ", " "), "@return ")
        elif self.language == "java" and self.docstyle == "default":
            return self._parse_documentation_with_symbols(
                ("@param  ", " "), "@return ")
        else:
            raise NotImplementedError(
                "Documentation parsing for {0.language!r} in {0.docstyle!r}"
                " has not been implemented yet".format(self))

    def _parse_documentation_with_symbols(self, param_identifiers,
                                          return_identifiers):
        """
        Parses documentation based on parameter and return symbols.

        :param param_identifiers:
            A tuple of two strings with which a parameter starts and ends.
        :param return_identifiers:
            The string with which a return description starts.
        :return:
            The list of all the parsed sections of the documentation. Every
            section is a namedtuple of either ``Description`` or ``Parameter``
            or ``ReturnValue``.
        """
        lines = self.documentation.splitlines(keepends=True)

        parse_mode = self.Description

        cur_param = ""

        desc = ""
        parsed = []

        for line in lines:

            stripped_line = line.strip()

            if stripped_line.startswith(param_identifiers[0]):
                parse_mode = self.Parameter
                param_offset = line.find(
                    param_identifiers[0]) + len(param_identifiers[0])
                splitted = line[param_offset:].split(param_identifiers[1], 1)
                cur_param = splitted[0].strip()
                # For cases where the param description is not on the
                # same line, but on subsequent lines.
                try:
                    param_desc = splitted[1]
                except IndexError:
                    param_desc = ""
                parsed.append(self.Parameter(name=cur_param, desc=param_desc))

            elif stripped_line.startswith(return_identifiers):
                parse_mode = self.ReturnValue
                return_offset = line.find(
                    return_identifiers) + len(return_identifiers)
                retval_desc = line[return_offset:]
                parsed.append(self.ReturnValue(desc=retval_desc))

            elif parse_mode == self.ReturnValue:
                retval_desc += line
                parsed.pop()
                parsed.append(self.ReturnValue(desc=retval_desc))

            elif parse_mode == self.Parameter:
                param_desc += line
                parsed.pop()
                parsed.append(self.Parameter(name=cur_param, desc=param_desc))

            else:
                desc += line
                # This is inside a try-except for cases where the list
                # is empty and has nothing to pop.
                try:
                    parsed.pop()
                except IndexError:
                    pass
                parsed.append(self.Description(desc=desc))

        return parsed
