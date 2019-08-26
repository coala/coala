from coalib.nestedlib.parsers.Parser import Parser, create_nl_section, get_file
import regex as re

# `regex` module is used instead of `re` since `re` does not have the
# capability to compile regex statements that have the same group names.


class PyJinjaParser(Parser):

    JINJA_STATEMENT_PATTERN = (
        r'(?P<open>{%[+-]?)(?P<content>.*?)(?P<close>[+-]?%})')
    JINJA_VAR_PATTERN = (
        r'(?P<open>{{)(?P<content>.*?)(?P<close>}})')
    JINJA_RE = re.compile(
        '|'.join([JINJA_STATEMENT_PATTERN, JINJA_VAR_PATTERN]))

    append_prev_section = True
    """
    append_prev_section is a boolean variable.

    This determines if a new section needs to be created for the current line or
    if it can be appended to the previous nl_sections.

    This is needed because we do not want to mix the contents from a mixed lang
    line and a pure line. This helps in better maintainability of nl_sections.
    """

    def new_nl_section(self, file, language, nl_sections=None, start_line=None,
                       start_column=None, end_line=None, end_column=None):
        """
        Create a new nl_section.

        :param file:         The name of the original nested languges file.
        :param language:     The language of the current line.
        :param nl_sections:  The list of nested languages sections present in
                             file
        :param start_line:   The line number where the Nested Language Section
                             starts. The first line is 1.
        :param start_column: The column number where the Nested Language
                             Section
                             starts. The first column is 1.
        :param end_line:     The line number where the Nested Language Section
                             end.
        :param end_column:   The column number where the Nested Language Section
                             starts.
        """
        prev_nl_section = nl_sections[-1] if nl_sections else None
        index = 1 if not prev_nl_section else (prev_nl_section.index + 1)
        nl_section = create_nl_section(file=file,
                                       index=index,
                                       language=language,
                                       start_line=start_line,
                                       start_column=start_column,
                                       end_line=end_line,
                                       end_column=end_column)

        nl_sections.append(nl_section)
        return nl_sections

    def update_nl_section(self, nl_sections=None, end_line=None,
                          end_column=None):
        """
        Update the end line and the end column of the last Nested Language
        Section present in nl_sections.

        This happens when the line above the current line has the same language
        as that of current line. Instead of creating a new section for the
        current line, we append it to the last nl_section present in
        nl_sections.

        :param nl_sections:  The list of nested languages sections present in
                             file
        :param end_line:     The line number where the Nested Language Section
                             end.
        :param end_column:   The column number where the Nested Language Section
                             starts.
        """
        prev_nl_section = nl_sections[-1]
        prev_nl_section.end.line = end_line
        prev_nl_section.end.column = end_column
        prev_nl_section.linted_end.line = end_line
        prev_nl_section.linted_end.column = end_column
        return nl_sections

    def pure_line_sections(self, file, line, nl_sections=None, language=None,
                           line_number=None, start_column=None,
                           end_column=None):
        """
        Create sections from a pure line.

        Example of Pure Lines are:
        >> "{% for x in y %}"
        >> "{% set var1 = value1 %}"
        >> "print("Bye Bye")"

        If the line is made up of only one language. There are two things that
        can be done.
        1. If the language of the last nl_section is different than the lang of
        the current line, then create a new nl_section for the current line.

        2. If the language of the last nl_section is same as that of the current
        line, update the end_line and end_column values of the last
        nl_section. This is equivalent to appending the current line to the
        previous nl_section.

        :param file:         The name of the original nested languges file.
        :param line:         The current line.
        :param nl_sections:  The list of nested languages sections present in
                             file
        :param language:     The language of the current line.
        :param line_number:  The line number of the current line correspondnig
                             to the original Nested language file.
        :param start_column: The column number where the Nested Language Section
                             starts. The first column is 1.
        :param end_column:   The column number where the Nested Language Section
                             starts.
        """
        prev_nl_section = nl_sections[-1] if nl_sections else None
        if((not prev_nl_section or
                not (prev_nl_section.language == language))
                or not self.append_prev_section):
            """
            Create a new nl_section if there are no nl_section present
            or if the language of the previous section do not match
            with the language of the current line.
            """
            nl_sections = self.new_nl_section(file=file,
                                              language=language,
                                              nl_sections=nl_sections,
                                              start_line=line_number,
                                              start_column=start_column,
                                              end_line=line_number,
                                              end_column=end_column)

            self.append_prev_section = True
        else:
            """
            If the language of pervious section and the current line are
            same, append current line to the previous section. You
            do that by updating the `end` attribute of the previous
            nl section
            """
            nl_sections = self.update_nl_section(nl_sections, line_number,
                                                 len(line)-1)
        return nl_sections

    def check_pure_jinja_line(self, line):
        """
        Check if the line is pure Jinja.

        Update the values of self.append_prev_section and PURE_JINJA_LINE
        accordingly. To check if a line is pure jinja2, check if the content
        before and after the match object is white space. If it is, then it is
        purely jinja2

        :param line:         The current line.
        """
        pure_jinja_line = False

        start_column = 0
        end_column = len(line)-1
        match = self.JINJA_RE.search(line)
        num_jinja_elem = len(re.findall(self.JINJA_RE, line))

        if (num_jinja_elem > 1):
            return pure_jinja_line

        elif match.start() == start_column and match.end() == end_column:
            pure_jinja_line = True
            return pure_jinja_line

        elif match.start() == start_column and match.end() < end_column:
            content_after_match = line[match.end():end_column+1]
            if (content_after_match.isspace()):
                pure_jinja_line = True
            return pure_jinja_line

        elif match.start() > start_column and match.end() == end_column:
            content_before_match = line[0:match.start()]
            if (content_before_match.isspace()):
                pure_jinja_line = True
            return pure_jinja_line

        else:
            # Check if match.start() > start_column and match.end() < end_column
            content_before_match = line[0:match.start()]
            content_after_match = line[match.end():end_column+1]
            if content_before_match.isspace() and content_after_match.isspace():
                pure_jinja_line = True
            return pure_jinja_line

    def segre_mixed_line(self, file, line, nl_sections, line_number=None,
                         match=None, cursor=None):
        """
        Segregate the line made of up mixed languages into Nested Language
        sections.

        A line that is made up of both Jinja and Python are called as mixed
        language lines.
        Examples of mixed language lines are:
        >> "{% endif %} x = 40 {{ }}"
        >> "y = {{ var }} if x > 40 else {{ var2 }}"
        >> "{% set x = thanos %} print("He rocks")"

        Also, due to the way parser works it detects a pure jinja2 line with
        white spaces infront of it as a mixed language line. In order to
        overcome this we check if the characters before the first match of the
        jinja2 element are whitespaces. If it is - we create a pure jinja2 line
        section or append it to the previous nl_section if the language is same.

        :param file:         The name of the original nested languges file.
        :param line:         The current line.
        :param nl_sections:  The list of nested languages sections present in
                             file
        :param line_number:  The line number of the current line correspondnig
                             to the original Nested language file.
        :param match:        The match object which detected the Jinja element.
        :param cursor:       The cursor points to the next character in the
                             line that has to be read.

        """
        content_before_match = line[cursor:match.start()]

        if (content_before_match.isspace()):

            nl_sections = self.pure_line_sections(file=file,
                                                  line=line,
                                                  nl_sections=nl_sections,
                                                  language='jinja2',
                                                  line_number=line_number,
                                                  start_column=cursor+1,
                                                  end_column=match.end())

        else:
            # Python Section
            nl_sections = self.new_nl_section(file=file,
                                              language='python',
                                              nl_sections=nl_sections,
                                              start_line=line_number,
                                              start_column=cursor+1,
                                              end_line=line_number,
                                              end_column=match.start())

            # Jinja Section
            nl_sections = self.new_nl_section(file=file,
                                              language='jinja2',
                                              nl_sections=nl_sections,
                                              start_line=line_number,
                                              start_column=match.start()+1,
                                              end_line=line_number,
                                              end_column=match.end())

        return nl_sections

    def parse_line(self, line, nl_sections=None, line_number=None,
                   file=None):
        """
        Parse the current line and returns a list of nl_section.

        :param file:         The name of the original nested languges file.
        :param line:         The current line.
        :param nl_sections:  The list of nested languages sections present in
                             file
        :param line_number:  The line number of the current line correspondnig
                             to the original Nested language file.
        """
        line_number = line_number if (line_number) else 1

        start_column = 0

        # len(line) also includes the newline character - hence we subtract one
        end_column = len(line) - 1

        # The cursor points to the next character in the line that has to be
        # read. The cursor is needed when we have a mixed language line. This
        # keeps track of all the jinja2 elements that have been read on the
        # current line.
        cursor = start_column

        # Check the line is empty.
        # If the line is empty and there is a nl_section present before it
        # append the line to it. Else create a new nl_section of any language
        # it does not matter
        if not line.strip():
            prev_nl_section = nl_sections[-1] if nl_sections else None
            if not prev_nl_section:
                nl_sections = self.new_nl_section(file=file,
                                                  language='jinja2',
                                                  nl_sections=nl_sections,
                                                  start_line=line_number,
                                                  start_column=1,
                                                  end_column=end_column)
            else:
                nl_sections = self.update_nl_section(nl_sections, line_number,
                                                     1)
            return nl_sections

        # Check if the line has any Jinja elements. If not it's pure Python
        if not self.JINJA_RE.search(line):
            lang_cur_line = 'python'

            self.pure_line_sections(file=file,
                                    line=line,
                                    nl_sections=nl_sections,
                                    language=lang_cur_line,
                                    line_number=line_number,
                                    start_column=cursor+1,
                                    end_column=end_column)

            return nl_sections

        else:
            """
            If the line contains Jinja Elements. There can be three cases:
            1. Pure Jinja Line
            2. Combination of Jinja and Python

            If it's a pure Jinja Line, we create a new nl_section if the
            language of previous section is different than the current
            section. If the language is same, we directly append this line
            to the previous nl_section.

            If it's a combination of Jinja and Python. We create a seperate
            nl_sections for each of element.

            >> line = '{{ var }} = print("Bye Bye")'
            >> nl_sections = parse_line(line, nl_sections = [])
            ['test.py: 1 : jinja2  : L1 C1  : L1 C9  : L1 C1  : L1 C9',
            'test.py: 2 : python : L1 C10 : L1 C28 : L1 C10 : L1 C28'
            ]
            """

            """
            Get a list of all Jinja Elements. And on the basis of the start
            column and end column of the Jinja Element we make the sections
            accordingly.
            """
            match_objects = self.JINJA_RE.finditer(line)

            """
            If it's a mixed language line, do not append it to previous
            section.

            If the line has only one Jinja Element, it can still be a mixed
            language line. So we check if the span values of the match object
            is equal to the start_column which is zero and end_column which
            is len(line) - 1. If it is then it's a Pure Jinja Line.
            """
            pure_jinja_line = self.check_pure_jinja_line(line)

            if not pure_jinja_line:
                self.append_prev_section = False

            for match in match_objects:
                lang_cur_line = 'jinja2'

                if(match.start() == cursor and match.end() == end_column):
                    """
                    If the first match object spans the entire line that means
                    that the line is a Pure jinja2 line.
                    Eg:
                    >> line = "{% set x = 0 %}"
                    """
                    nl_sections = self.pure_line_sections(
                                                        file=file,
                                                        line=line,
                                                        nl_sections=nl_sections,
                                                        language=lang_cur_line,
                                                        line_number=line_number,
                                                        start_column=cursor+1,
                                                        end_column=match.end())

                    cursor = match.end()

                elif(match.start() == cursor and match.end() < end_column):
                    """
                    If the Jinja elements starts at the start of line, but it
                    ends at a position less than the end_column of the line.
                    Make a Jinja Section of the element and shift the cursor
                    to one character after the end of the jinja2 element/

                    Assume cursor is 0 and end_column is 24. As you see below
                    the first jinja2 element starts at cursor i.e 0 but the it
                    end at 14 which is less than the end column.

                    >> line = "{% set x = 0 %} x = 40  {{ var1 }}"
                    """
                    nl_sections = self.new_nl_section(file=file,
                                                      language='jinja2',
                                                      nl_sections=nl_sections,
                                                      start_line=line_number,
                                                      start_column=cursor+1,
                                                      end_line=line_number,
                                                      end_column=match.end())
                    cursor = match.end()

                elif(match.start() > cursor and match.end() == end_column):
                    """
                    If the match object starts at a column which is not the
                    starting of the line, that mean that it has some content
                    before it.

                    The content before the match object can either be a
                    collection of spaces or python code.

                    If it's spaces then that means that the entire line is pure
                    jinja2 and we need to make one section.

                    Else we make two sections, one for python that includes the
                    text before the match object and another for jinja2.

                    >> line = "x = 40 {% set x = 0 %}"

                    Assume the cursor is zero and end_column is `len(line) - 1`.
                    The Jinja element `{% set x = 0 %}` starts at a column
                    greater than cursor but ends at the end_column.
                    """

                    nl_sections = self.segre_mixed_line(file=file,
                                                        nl_sections=nl_sections,
                                                        line=line,
                                                        line_number=line_number,
                                                        match=match,
                                                        cursor=cursor)
                    cursor = match.end()

                else:
                    """
                    Check:
                    if match.start() > cursor and match.end() < end_column.

                    The match object starts at a column which is greater than
                    the cursor and end at a column less than the end_column.



                    This deals with the Jinja elements present somewhere in the
                    middle of the line.
                    >> line = "x = 40 {% set x = 0 %} {{ var1 }}"

                    Assume the cursor is zero and end_column is `len(line) - 1`.
                    The Jinja element `{% set x = 0 %}` represents this
                    scenario.
                    """
                    nl_sections = self.segre_mixed_line(file=file,
                                                        nl_sections=nl_sections,
                                                        line=line,
                                                        line_number=line_number,
                                                        match=match,
                                                        cursor=cursor)

                    cursor = match.end()

                self.append_prev_section = True

            if not cursor == end_column:
                """
                If the cursor is not equal to the length of line that means we
                have some python code after all the Jinja elements on the line.
                i.e present on the last of line.

                eg: "x = 14 {% set y = 10 %} z = 30 "

                There might also be the condition where there are spaces left at
                the end of the line. If it is present. Then add those to the
                previous jinja2 section.

                If we run our parse, the code until above would only have made
                nl_sections until the {% set y = 10 %}. There was no nl_section
                made for z = 30. That's why we make the nl_section for that.
                """

                content_after_match = line[cursor:end_column+1]

                # If we have only one Jinja Element and after that we have space
                # the line will be considered as pure
                if (content_after_match.isspace()):

                    nl_sections = self.update_nl_section(
                                                        nl_sections=nl_sections,
                                                        end_line=line_number,
                                                        end_column=len(line)-1)

                else:
                    nl_sections = self.new_nl_section(file=file,
                                                      language='python',
                                                      nl_sections=nl_sections,
                                                      start_line=line_number,
                                                      start_column=cursor+1,
                                                      end_line=line_number,
                                                      end_column=len(line)-1)

            # If the present line was not a pure Jinja line, the next line
            # should not be appended to the current line.
            if not pure_jinja_line:
                self.append_prev_section = False

        return nl_sections

    def make_nl_sections(self, file_contents, filename):
        nl_sections = []
        line_number = 0

        for line in file_contents:
            line_number += 1
            nl_sections = self.parse_line(line,
                                          line_number=line_number,
                                          nl_sections=nl_sections,
                                          file=filename)

        return nl_sections

    def parse(self, filename):
        """
        Return a list of nl_sections.

        :param file_contents: The contents of the original nested file.

        >>> from coalib.nestedlib.parsers.PyJinjaParser import PyJinjaParser
        >>> file_contents = ("for x in y:\\n",
        ...                  "{% if x is True %}\\n",
        ...                  "\\t{% set var3 = value3 %}\\n",
        ...                  "{% elif %}\\n",
        ...                  "\\t\\t{{ var }} = print('Bye Bye')\\n")

        >>> parser = PyJinjaParser()
        >>> nl_sections = parser.make_nl_sections(file_contents, 'test.py')

        >>> str(nl_sections[0])
        '...test.py: 1: python: L1 C1: L1 C11: L1 C1: L1 C11'

        >>> str(nl_sections[1])
        '...test.py: 2: jinja2: L2 C1: L4 C10: L2 C1: L4 C10'

        >>> str(nl_sections[2])
        '...test.py: 3: jinja2: L5 C1: L5 C11: L5 C1: L5 C11'

        >>> str(nl_sections[3])
        '...test.py: 4: python: L5 C12: L5 C30: L5 C12: L5 C30'

        The details of the ouput from the parser is as follows

        :The first column:     The name of the file the original nested language
                               file.
        :The second column:    The language of the nl_section
        :The third column:     The index of the section.
        :The fourth column:    The start of that section in the original nested
                               file.
        :The fifth column:     The end of that section in the original nested
                               file.
        :The sixth column:     The start of that section in the original nested
                               file.
        :The seventh column:   The start of that section in the original nested
                               file.
        """
        # A list to store all the nl_section in the file

        file_contents = get_file(filename)

        nl_sections = self.make_nl_sections(file_contents, filename)
        return nl_sections
