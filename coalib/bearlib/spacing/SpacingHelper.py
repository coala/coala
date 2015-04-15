from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable


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

    def get_indentation(self, line):
        """
        Checks the lines indentation.

        :param line: A string to check for indentation.
        :return:     The indentation count in spaces.
        """
        if not isinstance(line, str):
            raise TypeError("The 'line' parameter should be a string.")

        count = 0
        for char in line:
            if char == ' ':
                count += 1
                continue

            if char == '\t':
                count += self.tab_width - (count % self.tab_width)
                continue

            break

        return count

    def replace_tabs_with_spaces(self, line):
        """
        Replaces tabs in this line with the appropriate number of spaces.

        Example: " \t" will be converted to "    ", assuming the tab_width is
        set to 4.

        :param line: The string with tabs to replace.
        :return:     A string with no tabs.
        """
        if not isinstance(line, str):
            raise TypeError("The 'line' parameter should be a string.")

        result = ""
        tabless_position = 0
        for char in line:
            if char == '\t':
                space_count = (self.tab_width - tabless_position
                               % self.tab_width)
                result += space_count * " "
                tabless_position += space_count
                continue

            result += char
            tabless_position += 1

        return result

    def replace_spaces_with_tabs(self, line):
        """
        Replaces spaces with tabs where possible. However in no case only one
        space will be replaced by a tab.

        Example: " \t   a_text   another" will be converted to
        "\t   a_text\tanother", assuming the tab_width is set to 4.

        :param line: The string with spaces to replace.
        :return:     The converted string.
        """
        if not isinstance(line, str):
            raise TypeError("The 'line' parameter should be a string.")

        currspaces = 0
        result = ""
        # Tracking the index of the string isnt enough because tabs are
        # spanning over multiple columns
        tabless_position = 0
        for char in line:
            if char == " ":
                currspaces += 1
                tabless_position += 1
            elif char == "\t":
                space_count = (self.tab_width - tabless_position
                               % self.tab_width)
                currspaces += space_count
                tabless_position += space_count
            else:
                result += currspaces*" " + char
                currspaces = 0
                tabless_position += 1

            # tabless_position is now incremented to point _after_ the current
            # char
            if tabless_position % self.tab_width == 0:
                if currspaces > 1:
                    result += "\t"
                else:
                    result += currspaces*" "

                currspaces = 0

        result += currspaces*" "

        return result
