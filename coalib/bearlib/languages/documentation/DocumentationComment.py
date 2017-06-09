from collections import namedtuple

from coala_utils.decorators import generate_eq, generate_repr


@generate_repr()
@generate_eq('documentation', 'language', 'docstyle',
             'indent', 'marker', 'range')
class DocumentationComment:
    """
    The DocumentationComment holds information about a documentation comment
    inside source-code, like position etc.
    """
    Parameter = namedtuple('Parameter', 'name, desc')
    ExceptionValue = namedtuple('ExceptionValue', 'name, desc')
    ReturnValue = namedtuple('ReturnValue', 'desc')
    Description = namedtuple('Description', 'desc')

    def __init__(self, documentation, docstyle_definition,
                 indent, marker, range):
        """
        Instantiates a new DocumentationComment.

        :param documentation:
            The documentation text.
        :param docstyle_definition:
            The ``DocstyleDefinition`` instance that defines what docstyle is
            being used in the documentation.
        :param indent:
            The string of indentation used in front of the first marker of the
            documentation.
        :param marker:
            The three-element tuple with marker strings, that identified this
            documentation comment.
        :param range:
            The position range of type ``TextRange``.
        """
        self.documentation = documentation
        self.docstyle_definition = docstyle_definition
        self.indent = indent
        self.marker = marker
        self.range = range

    def __str__(self):
        return self.documentation

    @property
    def language(self):
        return self.docstyle_definition.language

    @property
    def docstyle(self):
        return self.docstyle_definition.docstyle

    @property
    def metadata(self):
        return self.docstyle_definition.metadata

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
        if self.language == 'python' and self.docstyle == 'default':
            return self._parse_documentation_with_symbols(
                (':param ', ':'), (':raises ', ':'), ':return:')
        elif self.language == 'python' and self.docstyle == 'doxygen':
            return self._parse_documentation_with_symbols(
                ('@param ', ' '), ('@raises ', ' '), '@return ')
        elif self.language == 'java' and self.docstyle == 'default':
            return self._parse_documentation_with_symbols(
                ('@param  ', ' '), ('@raises  ', ' '), '@return ')
        elif self.language == 'golang' and self.docstyle == 'golang':
            # golang does not have param, return markers
            return self.documentation.splitlines(keepends=True)
        else:
            raise NotImplementedError(
                'Documentation parsing for {0.language!r} in {0.docstyle!r}'
                ' has not been implemented yet'.format(self))

    def _parse_documentation_with_symbols(self,
                                          param_identifiers,
                                          exception_identifiers,
                                          return_identifiers):
        """
        Parses documentation based on parameter, exception and return symbols.

        :param param_identifiers:
            A tuple of two strings with which a parameter starts and ends.
        :param exception_identifiers:
            A tuple of two strings with which an exception starts and ends.
        :param return_identifiers:
            The string with which a return description starts.
        :return:
            The list of all the parsed sections of the documentation. Every
            section is a named tuple of either ``Description``, ``Parameter``,
            ``ExceptionValue`` or ``ReturnValue``.
        """
        lines = self.documentation.splitlines(keepends=True)

        parse_mode = self.Description

        cur_param = ''

        desc = ''
        parsed = []

        for line in lines:

            stripped_line = line.strip()

            if stripped_line.startswith(param_identifiers[0]):
                parse_mode = self.Parameter
                # param_offset contains the starting column of param's name.
                param_offset = line.find(
                    param_identifiers[0]) + len(param_identifiers[0])
                # splitted contains the whole line from the param's name,
                # which in turn is further divided into its name and desc.
                splitted = line[param_offset:].split(param_identifiers[1], 1)
                cur_param = splitted[0].strip()

                param_desc = splitted[1]
                # parsed section is added to the final list.
                parsed.append(self.Parameter(name=cur_param, desc=param_desc))

            elif stripped_line.startswith(exception_identifiers[0]):
                parse_mode = self.ExceptionValue
                exception_offset = line.find(
                    exception_identifiers[0]) + len(exception_identifiers[0])
                splitted = line[exception_offset:].split(
                    exception_identifiers[1], 1)
                cur_exception = splitted[0].strip()

                exception_desc = splitted[1]
                parsed.append(self.ExceptionValue(
                    name=cur_exception, desc=exception_desc))

            elif stripped_line.startswith(return_identifiers):
                parse_mode = self.ReturnValue
                return_offset = line.find(
                    return_identifiers) + len(return_identifiers)
                retval_desc = line[return_offset:]
                parsed.append(self.ReturnValue(desc=retval_desc))

            # These conditions will take care if the parsed section
            # descriptions are not on the same line as that of it's
            # name. Further, adding the parsed section to the final list.
            elif parse_mode == self.ReturnValue:
                retval_desc += line
                parsed.pop()
                parsed.append(self.ReturnValue(desc=retval_desc))

            elif parse_mode == self.ExceptionValue:
                exception_desc += line
                parsed.pop()
                parsed.append(self.ExceptionValue(
                    name=cur_exception, desc=exception_desc))

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

    @classmethod
    def from_metadata(cls, doccomment, docstyle_definition,
                      marker, indent, range):
        r"""
        Assembles a list of parsed documentation comment metadata.

        This function just assembles the documentation comment
        itself, without the markers and indentation.

        >>> from coalib.bearlib.languages.documentation.DocumentationComment \
        ...     import DocumentationComment
        >>> from coalib.bearlib.languages.documentation.DocstyleDefinition \
        ...     import DocstyleDefinition
        >>> from coalib.results.TextRange import TextRange
        >>> Description = DocumentationComment.Description
        >>> Parameter = DocumentationComment.Parameter
        >>> python_default = DocstyleDefinition.load("python3", "default")
        >>> parsed_doc = [Description(desc='\nDescription\n'),
        ...               Parameter(name='age', desc=' Age\n')]
        >>> str(DocumentationComment.from_metadata(
        ...         parsed_doc, python_default,
        ...         python_default.markers[0], 4,
        ...         TextRange.from_values(0, 0, 0, 0)))
        '\nDescription\n:param age: Age\n'

        :param doccomment:
            The list of parsed documentation comment metadata.
        :param docstyle_definition:
            The ``DocstyleDefinition`` instance that defines what docstyle is
            being used in a documentation comment.
        :param marker:
            The markers to be used in the documentation comment.
        :param indent:
            The indentation to be used in the documentation comment.
        :param range:
            The range of the documentation comment.
        :return:
            A ``DocumentationComment`` instance of the assembled documentation.
        """
        assembled_doc = ''
        for section in doccomment:
            section_desc = section.desc.splitlines(keepends=True)

            if isinstance(section, cls.Parameter):
                assembled_doc += (docstyle_definition.metadata.param_start +
                                  section.name +
                                  docstyle_definition.metadata.param_end)

            elif isinstance(section, cls.ExceptionValue):
                assembled_doc += (docstyle_definition.metadata.exception_start
                                  + section.name
                                  + docstyle_definition.metadata.exception_end)

            elif isinstance(section, cls.ReturnValue):
                assembled_doc += docstyle_definition.metadata.return_sep

            assembled_doc += ''.join(section_desc)

        return DocumentationComment(assembled_doc, docstyle_definition, indent,
                                    marker, range)

    def assemble(self):
        """
        Assembles parsed documentation to the original documentation.

        This function assembles the whole documentation comment, with the
        given markers and indentation.
        """
        lines = self.documentation.splitlines(keepends=True)
        assembled = self.indent + self.marker[0]
        if len(lines) == 0:
            return self.marker[0] + self.marker[2]
        assembled += lines[0]
        assembled += ''.join('\n' if line == '\n' and not self.marker[1]
                             else self.indent + self.marker[1] + line
                             for line in lines[1:])
        return (assembled if self.marker[1] == self.marker[2] else
                (assembled +
                 (self.indent if lines[-1][-1] == '\n' else '') +
                 self.marker[2]))
