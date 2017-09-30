from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.results.Diff import Diff
from coalib.results.TextRange import TextRange
from coalib.bearlib.languages.documentation.DocumentationExtraction import (
    extract_documentation_with_markers)


class DocBaseClass:
    """
    DocBaseClass holds important functions which will extract, parse
    and generates diffs for documentation. All bears that processes
    documentation should inherit from this.
    """

    @staticmethod
    def extract(content, language, docstyle):
        """
        Extracts all documentation texts inside the given source-code-string
        using the coala docstyle definition files.

        The documentation texts are sorted by their order appearing in
        ``content``.

        For more information about how documentation comments are
        identified and extracted, see DocstyleDefinition.doctypes enumeration.

        :param content:            The source-code-string where to extract
                                   documentation from. Needs to be a list
                                   or tuple where each string item is a
                                   single line(including ending whitespaces
                                   like ``\\n``).
        :param language:           The programming language used.
        :param docstyle:           The documentation style/tool used
                                   (e.g. doxygen).
        :raises FileNotFoundError: Raised when the docstyle definition file
                                   was not found.
        :raises KeyError:          Raised when the given language is not
                                   defined in given docstyle.
        :raises ValueError:        Raised when a docstyle definition setting
                                   has an invalid format.
        :return:                   An iterator returning instances of
                                   DocumentationComment or MalformedComment
                                   found in the content.
        """
        docstyle_definition = DocstyleDefinition.load(language, docstyle)
        return extract_documentation_with_markers(
                        content, docstyle_definition)

    @staticmethod
    def generate_diff(file, doc_comment, new_comment):
        """
        Generates diff between the original doc_comment and its fix
        new_comment which are instances of DocumentationComment.

        :param doc_comment:
            Original instance of DocumentationComment.
        :param new_comment:
            Fixed instance of DocumentationComment.
        :return:
            Diff instance.
        """
        diff = Diff(file)

        # We need to update old comment positions, as `assemble()`
        # prepends indentation for first line.
        old_range = TextRange.from_values(
            doc_comment.range.start.line,
            1,
            doc_comment.range.end.line,
            doc_comment.range.end.column)

        # Clearing cached assemble() so a fresh one is fetched.
        new_comment.assemble.cache_clear()

        diff.replace(old_range, new_comment.assemble())
        return diff

    def process_documentation(self, *args, **kwargs):
        """
        Checks and handles the fixing part of documentation.

        :return:
            A tuple of processed documentation and warning_desc.
        """
        raise NotImplementedError('This function has to be implemented for a '
                                  'documentation bear.')
