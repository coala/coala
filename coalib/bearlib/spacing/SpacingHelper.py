from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable
from coala_utils.decorators import enforce_signature


class SpacingHelper(SectionCreatable):
    DEFAULT_TAB_WIDTH = 4

    def __init__(self, tab_width: int=DEFAULT_TAB_WIDTH):
        """
        Creates a helper object for spacing operations.

        :param tab_width: The number of spaces which visually equals a tab.
        """
        SectionCreatable.__init__(self)
        if not isinstance(tab_width, int):
            raise TypeError("The 'tab_width' parameter should be an integer.")

        self.tab_width = tab_width

    @enforce_signature
    def get_indentation(self, line: str):
        """
        Checks the lines indentation.

        :param line: A string to check for indentation.
        :return:     The indentation count in spaces.
        """
        # TODO: maybe use line.rsplit('\t') to prevent expandtabs wasting time
        # expanding tabs after the first non-whitespace.
        no_tabs = line.expandtabs(self.tab_width)
        no_indent = no_tabs.lstrip(' ')
        return len(no_tabs)-len(no_indent)

    @enforce_signature
    def replace_tabs_with_spaces(self, line: str):
        """
        Replaces tabs in this line with the appropriate number of spaces.

        Example: " \t" will be converted to "    ", assuming the tab_width is
        set to 4.

        :param line: The string with tabs to replace.
        :return:     A string with no tabs.
        """
        return line.expandtabs(self.tab_width)

    @enforce_signature
    def replace_spaces_with_tabs(self, line: str):
        """
        Replaces spaces with tabs where possible. However in no case only one
        space will be replaced by a tab.

        Example: " \t   a_text   another" will be converted to
        "\t   a_text\tanother", assuming the tab_width is set to 4.

        :param line: The string with spaces to replace.
        :return:     The converted string.
        """
        # TODO: Strip leading tabs, to optimise lines that already tab indented

        # Cache tab_width; also ensure it is consistent throughout algorithm
        tab_width = self.tab_width
        no_tabs = line.expandtabs(tab_width)
        chunks = []

        for i in range(0, len(no_tabs), tab_width):
            chunk = no_tabs[i:i + tab_width]
            non_whitespace = chunk.rstrip(' \t')

            if len(non_whitespace) == tab_width - 1 and chunk[-1] == ' ':
                if len(no_tabs) <= i + tab_width:
                    chunks.append(non_whitespace + line[-1])
                    break

                lookahead = no_tabs[i + tab_width]

                if lookahead in ['\t', ' ']:
                    chunks.append(non_whitespace + '\t')
                else:
                    chunks.append(non_whitespace + ' ')
            elif len(non_whitespace) != tab_width and len(chunk) == tab_width:
                chunks.append(non_whitespace + '\t')
            else:
                chunks.append(chunk)

        return ''.join(chunks)
