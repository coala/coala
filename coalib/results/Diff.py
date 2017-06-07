import copy
import difflib
import logging

from unidiff import PatchSet

from coalib.results.LineDiff import LineDiff, ConflictError
from coalib.results.SourceRange import SourceRange
from coalib.results.TextRange import TextRange
from coala_utils.decorators import enforce_signature, generate_eq


@generate_eq('_file', 'modified', 'rename', 'delete')
class Diff:
    """
    A Diff result represents a difference for one file.
    """

    def __init__(self, file_list, rename=False, delete=False):
        """
        Creates an empty diff for the given file.

        :param file_list: The original (unmodified) file as a list of its
                          lines.
        :param rename:    False or str containing new name of file.
        :param delete:    True if file is set to be deleted.
        """
        self._changes = {}
        self._file = list(file_list)
        self._original = self._generate_linebreaks(self._file)
        self.rename = rename
        self.delete = delete

    @classmethod
    def from_string_arrays(cls, file_array_1, file_array_2, rename=False):
        """
        Creates a Diff object from two arrays containing strings.

        If this Diff is applied to the original array, the second array will be
        created.

        :param file_array_1: Original array
        :param file_array_2: Array to compare
        :param rename:       False or str containing new name of file.
        """
        result = cls(file_array_1, rename=rename)

        matcher = difflib.SequenceMatcher(None, file_array_1, file_array_2)
        # We use this because its faster (generator) and doesn't yield as much
        # useless information as get_opcodes.
        for change_group in matcher.get_grouped_opcodes(1):
            for (tag,
                 a_index_1,
                 a_index_2,
                 b_index_1,
                 b_index_2) in change_group:
                if tag == 'delete':
                    for index in range(a_index_1+1, a_index_2+1):
                        result.delete_line(index)
                elif tag == 'insert':
                    # We add after line, they add before, so dont add 1 here
                    result.add_lines(a_index_1,
                                     file_array_2[b_index_1:b_index_2])
                elif tag == 'replace':
                    result.modify_line(a_index_1+1,
                                       file_array_2[b_index_1])
                    result.add_lines(a_index_1+1,
                                     file_array_2[b_index_1+1:b_index_2])
                    for index in range(a_index_1+2, a_index_2+1):
                        result.delete_line(index)

        return result

    @classmethod
    def from_unified_diff(cls, unified_diff, original_file):
        """
        Creates a ``Diff`` object from given unified diff.

        If the provided unified diff does not contain any patch,
        the ``Diff`` object initialized from the original file is
        returned.

        :param unified_diff:  Unified diff string.
        :param original_file: The contents of the original file
                              (line-splitted).
        :raises RuntimeError: Raised when the context lines or the
                              lines to be removed do not match in
                              the original file and the unified diff.
        """
        patch_set = PatchSet(unified_diff.splitlines())

        diff = Diff(original_file)

        if not patch_set:
            return diff

        # FIXME Handle patches consisting of changes in more than one file
        file = patch_set[0]

        for hunk in file:
            file_line = hunk.source_start
            hunk_iterator = iter(hunk)

            try:
                while True:
                    line = next(hunk_iterator)
                    source_code = str(line)[1:]
                    if line.is_added:
                        add_set = []
                        # As ``Diff`` does not allow line additions to a
                        # position more than one time, add all the
                        # consecutive '+' lines at once.
                        try:
                            while line.is_added:
                                add_set.append(source_code)
                                line = next(hunk_iterator)
                                source_code = str(line)[1:]

                            diff.add_lines(file_line-1, add_set)

                        except StopIteration:
                            diff.add_lines(file_line-1, add_set)
                            break

                    original_line = original_file[file_line-1].rstrip('\n')

                    if line.is_removed:
                        if source_code != original_line:
                            raise RuntimeError(
                                'The line to delete does not match with '
                                'the line in the original file. '
                                'Line to delete: {!r}, '
                                'Original line #{!r}: {!r}'.format(
                                    source_code,
                                    file_line,
                                    original_line)
                                )
                        diff.delete_line(file_line)

                    else:
                        if source_code != original_line:
                            raise RuntimeError(
                                'Context lines do not match. '
                                'Line from unified diff: {!r}, '
                                'Original line #{!r}: {!r}'.format(
                                    source_code,
                                    file_line,
                                    original_line)
                                )

                    file_line += 1

            except StopIteration:
                pass

        return diff

    @classmethod
    def from_clang_fixit(cls, fixit, file):
        """
        Creates a Diff object from a given clang fixit and the file contents.

        :param fixit: A cindex.Fixit object.
        :param file:  A list of lines in the file to apply the fixit to.
        :return:      The corresponding Diff object.
        """
        assert isinstance(file, (list, tuple))

        oldvalue = '\n'.join(file[fixit.range.start.line-1:
                                  fixit.range.end.line])
        endindex = fixit.range.end.column - len(file[fixit.range.end.line-1])-1

        newvalue = (oldvalue[:fixit.range.start.column-1] +
                    fixit.value +
                    oldvalue[endindex:])
        new_file = (file[:fixit.range.start.line-1] +
                    type(file)(newvalue.splitlines(True)) +
                    file[fixit.range.end.line:])

        return cls.from_string_arrays(file, new_file)

    def _get_change(self, line_nr, min_line=1):
        if not isinstance(line_nr, int):
            raise TypeError('line_nr needs to be an integer.')
        if line_nr < min_line:
            raise IndexError('The given line number is not allowed.')

        return self._changes.get(line_nr, LineDiff())

    def stats(self):
        """
        Returns tuple containing number of additions and deletions in the diff.
        """
        additions = 0
        deletions = 0
        for line_diff in self._changes.values():
            if line_diff.change:
                additions += 1
                deletions += 1
            elif line_diff.delete:
                deletions += 1
            if line_diff.add_after:
                additions += len(line_diff.add_after)
        return additions, deletions

    def __len__(self):
        """
        Returns total number of additions and deletions in diff.
        """
        return sum(self.stats())

    @property
    def rename(self):
        """
        :return: string containing new name of the file.
        """
        return self._rename

    @rename.setter
    @enforce_signature
    def rename(self, rename: (str, False)):
        """
        :param rename: False or string containing new name of file.
        """
        self._rename = rename

    @property
    def delete(self):
        """
        :return: True if file is set to be deleted.
        """
        return self._delete

    @delete.setter
    @enforce_signature
    def delete(self, delete: bool):
        """
        :param delete: True if file is set to be deleted, False otherwise.
        """
        self._delete = delete

    @property
    def original(self):
        """
        Retrieves the original file.
        """
        return self._original

    def _raw_modified(self):
        """
        Calculates the modified file, after applying the Diff to the original.
        """
        result = []

        if self.delete:
            return result

        current_line = 0

        # Note that line_nr counts from _1_ although 0 is possible when
        # inserting lines before everything
        for line_nr in sorted(self._changes):
            result.extend(self._file[current_line:max(line_nr-1, 0)])
            linediff = self._changes[line_nr]
            if not linediff.delete and not linediff.change and line_nr > 0:
                result.append(self._file[line_nr-1])
            elif linediff.change:
                result.append(linediff.change[1])

            if linediff.add_after:
                result.extend(linediff.add_after)

            current_line = line_nr

        result.extend(self._file[current_line:])

        return result

    @property
    def modified(self):
        """
        Calculates the modified file, after applying the Diff to the original.

        This property also adds linebreaks at the end of each line.
        If no newline was present at the end of file before, this state will
        be preserved, except if the last line is deleted.
        """
        return self._generate_linebreaks(self._raw_modified())

    @property
    def unified_diff(self):
        """
        Generates a unified diff corresponding to this patch.

        Each change will be displayed on its own line. Additionally, the
        unified diff preserves the EOF-state of the original file. This
        means that the ``Diff`` will only have a linebreak on the last line,
        if that was also present in the original file.

        Note that the unified diff is not deterministic and thus not suitable
        for equality comparison.
        """

        list_unified_diff = list(difflib.unified_diff(
            self._file,
            self._raw_modified(),
            tofile=self.rename if isinstance(self.rename, str) else ''))

        return ''.join(self._generate_linebreaks(list_unified_diff))

    def __json__(self):
        """
        Override JSON export, using the unified diff is the easiest thing for
        the users.
        """
        return self.unified_diff

    def affected_code(self, filename):
        """
        Creates a list of SourceRange objects which point to the related code.
        Changes on continuous lines will be put into one SourceRange.

        :param filename: The filename to associate the SourceRange's to.
        :return:         A list of all related SourceRange objects.
        """
        return list(diff.range(filename)
                    for diff in self.split_diff(distance=0))

    def split_diff(self, distance=1):
        """
        Splits this diff into small pieces, such that several continuously
        altered lines are still together in one diff. All subdiffs will be
        yielded.

        A diff like this with changes being together closely won't be splitted:

        >>> diff = Diff.from_string_arrays([     'b', 'c', 'e'],
        ...                                ['a', 'b', 'd', 'f'])
        >>> len(list(diff.split_diff()))
        1

        If we set the distance to 0, it will be splitted:

        >>> len(list(diff.split_diff(distance=0)))
        2

        If a negative distance is given, every change will be yielded as an own
        diff, even if they are right beneath each other:

        >>> len(list(diff.split_diff(distance=-1)))
        3

        If a file gets renamed or deleted only, it will be yielded as is:

        >>> len(list(Diff([], rename='test').split_diff()))
        1

        An empty diff will not yield any diffs:

        >>> len(list(Diff([]).split_diff()))
        0

        :param distance: Number of unchanged lines that are allowed in between
                         two changed lines so they get yielded as one diff.
        """
        if not self:
            return

        last_line = -1
        this_diff = Diff(self._file, rename=self.rename, delete=self.delete)
        for line in sorted(self._changes.keys()):
            if line > last_line + distance + 1 and len(this_diff._changes) > 0:
                yield this_diff
                this_diff = Diff(self._file, rename=self.rename,
                                 delete=self.delete)

            last_line = line
            this_diff._changes[line] = self._changes[line]

        # If the diff contains no line changes, the loop above will not be run
        # else, this_diff will never be empty and thus this has to be yielded
        # always.
        yield this_diff

    def range(self, filename):
        """
        Calculates a SourceRange spanning over the whole Diff. If something is
        added after the 0th line (i.e. before the first line) the first line
        will be included in the SourceRange.

        The range of an empty diff will only affect the filename:

        >>> range = Diff([]).range("file")
        >>> range.file is None
        False
        >>> print(range.start.line)
        None

        :param filename: The filename to associate the SourceRange with.
        :return:         A SourceRange object.
        """
        if len(self._changes) == 0:
            return SourceRange.from_values(filename)

        start = min(self._changes.keys())
        end = max(self._changes.keys())
        return SourceRange.from_values(filename,
                                       start_line=max(1, start),
                                       end_line=max(1, end))

    def __add__(self, other):
        """
        Adds another diff to this one. Will throw an exception if this is not
        possible. (This will *not* be done in place.)
        """
        if not isinstance(other, Diff):
            raise TypeError('Only diffs can be added to a diff.')

        if self.rename != other.rename and False not in (self.rename,
                                                         other.rename):
            raise ConflictError('Diffs contain conflicting renamings.')

        result = copy.deepcopy(self)
        result.rename = self.rename or other.rename
        result.delete = self.delete or other.delete

        for line_nr in other._changes:
            change = other._changes[line_nr]
            if change.delete is True:
                result.delete_line(line_nr)
            if change.add_after is not False:
                result.add_lines(line_nr, change.add_after)
            if change.change is not False:
                result.modify_line(line_nr, change.change[1])

        return result

    def __bool__(self):
        """
        >>> bool(Diff([]))
        False
        >>> bool(Diff([], rename="some"))
        True
        >>> bool(Diff([], delete=True))
        True
        >>> bool(Diff.from_string_arrays(['1'], []))
        True

        :return: False if the patch has no effect at all when applied.
        """
        return (self.rename is not False or
                self.delete is True or
                self.modified != self.original)

    def delete_line(self, line_nr):
        """
        Mark the given line nr as deleted. The first line is line number 1.

        Raises an exception if line number doesn't exist in the diff.
        """
        if line_nr > len(self._file):
            raise IndexError('The given line number is out of bounds.')

        linediff = self._get_change(line_nr)
        linediff.delete = True
        self._changes[line_nr] = linediff

    def delete_lines(self, line_nr_start, line_nr_end):
        """
        Delete lines in a specified range, inclusively.

        The range must be valid, i.e. lines must exist in diff, else an
        exception is raised.
        """
        for line_nr in range(line_nr_start, line_nr_end + 1):
            self.delete_line(line_nr)

    def add_lines(self, line_nr_before, lines):
        """
        Adds lines after the given line number.

        :param line_nr_before: Line number of the line before the additions.
                               Use 0 for insert lines before everything.
        :param lines:          A list of lines to add.
        """
        if lines == []:
            return  # No action

        linediff = self._get_change(line_nr_before, min_line=0)
        if linediff.add_after is not False:
            raise ConflictError('Cannot add lines after the given line since '
                                'there are already lines.')

        linediff.add_after = lines
        self._changes[line_nr_before] = linediff

    def add_line(self, line_nr_before, line):
        """
        Adds line after the given line number.

        :param line_nr_before: Line number of the line before the addition.
                               Use 0 to insert line before everything.
        :param line:           Line to add.
        """
        return self.add_lines(line_nr_before, [line])

    def modify_line(self, line_nr, replacement):
        r"""
        Changes the given line with the given line number. The replacement will
        be there instead.

        Given an empty diff object:

        >>> diff = Diff(['Hey there! Gorgeous.\n',
        ...              "It's nice that we're here.\n"])

        We can change a line easily:

        >>> diff.modify_line(1,
        ...                  'Hey there! This is sad.\n')
        >>> diff.modified
        ['Hey there! This is sad.\n', "It's nice that we're here.\n"]

        We can even merge changes within one line:

        >>> diff.modify_line(1,
        ...                  'Hello. :( Gorgeous.\n')
        >>> diff.modified
        ['Hello. :( This is sad.\n', "It's nice that we're here.\n"]

        However, if we change something that has been changed before, we'll get
        a conflict:

        >>> diff.modify_line(1,  # +ELLIPSIS
        ...                  'Hello. This is not ok. Gorgeous.\n')
        Traceback (most recent call last):
         ...
        coalib.results.LineDiff.ConflictError: ...
        """
        linediff = self._get_change(line_nr)
        if linediff.change is not False and linediff.change[1] != replacement:
            if len(replacement) == len(linediff.change[1]) == 1:
                raise ConflictError('Cannot merge the given line changes.')

            # The following diffs are created from strings, instead of lists.
            orig_diff = Diff.from_string_arrays(linediff.change[0],
                                                linediff.change[1])
            new_diff = Diff.from_string_arrays(linediff.change[0],
                                               replacement)
            replacement = ''.join((orig_diff + new_diff)._raw_modified())

        linediff.change = (self._file[line_nr-1], replacement)
        self._changes[line_nr] = linediff

    def change_line(self, line_nr, original_line, replacement):
        logging.debug('Use of change_line method is deprecated. Instead '
                      'use modify_line method, without the original_line '
                      'argument')
        self.modify_line(line_nr, replacement)

    def replace(self, range, replacement):
        r"""
        Replaces a part of text. Allows to span multiple lines.

        This function uses ``add_lines`` and ``delete_lines`` accordingly, so
        calls of those functions on lines given ``range`` affects after usage
        or vice versa lead to ``ConflictError``.

        >>> from coalib.results.TextRange import TextRange
        >>> test_text = ['hello\n', 'world\n', '4lines\n', 'done\n']
        >>> def replace(range, text):
        ...     diff = Diff(test_text)
        ...     diff.replace(range, text)
        ...     return diff.modified
        >>> replace(TextRange.from_values(1, 5, 4, 3), '\nyeah\ncool\nno')
        ['hell\n', 'yeah\n', 'cool\n', 'none\n']
        >>> replace(TextRange.from_values(2, 1, 3, 5), 'b')
        ['hello\n', 'bes\n', 'done\n']
        >>> replace(TextRange.from_values(1, 6, 4, 3), '')
        ['hellone\n']

        :param range:       The ``TextRange`` that gets replaced.
        :param replacement: The replacement string. Can be multiline.
        """
        # Remaining parts of the lines not affected by the replace.
        first_part = (
            self._file[range.start.line - 1][:range.start.column - 1])
        last_part = self._file[range.end.line - 1][range.end.column - 1:]

        self.delete_lines(range.start.line, range.end.line)
        self.add_lines(range.start.line - 1,
                       (first_part + replacement + last_part).splitlines(True))

    def insert(self, position, text):
        r"""
        Inserts (multiline) text at arbitrary position.

        >>> from coalib.results.TextPosition import TextPosition
        >>> test_text = ['123\n', '456\n', '789\n']
        >>> def insert(position, text):
        ...     diff = Diff(test_text)
        ...     diff.insert(position, text)
        ...     return diff.modified
        >>> insert(TextPosition(2, 3), 'woopy doopy')
        ['123\n', '45woopy doopy6\n', '789\n']
        >>> insert(TextPosition(1, 1), 'woopy\ndoopy')
        ['woopy\n', 'doopy123\n', '456\n', '789\n']
        >>> insert(TextPosition(2, 4), '\nwoopy\ndoopy\n')
        ['123\n', '456\n', 'woopy\n', 'doopy\n', '\n', '789\n']

        :param position: The ``TextPosition`` where to insert text.
        :param text:     The text to insert.
        """
        self.replace(TextRange(position, position), text)

    def remove(self, range):
        r"""
        Removes a piece of text in a given range.

        >>> from coalib.results.TextRange import TextRange
        >>> test_text = ['nice\n', 'try\n', 'bro\n']
        >>> def remove(range):
        ...     diff = Diff(test_text)
        ...     diff.remove(range)
        ...     return diff.modified
        >>> remove(TextRange.from_values(1, 1, 1, 4))
        ['e\n', 'try\n', 'bro\n']
        >>> remove(TextRange.from_values(1, 5, 2, 1))
        ['nicetry\n', 'bro\n']
        >>> remove(TextRange.from_values(1, 3, 3, 2))
        ['niro\n']
        >>> remove(TextRange.from_values(2, 1, 2, 1))
        ['nice\n', 'try\n', 'bro\n']

        :param range: The range to delete.
        """
        self.replace(range, '')

    @staticmethod
    def _add_linebreaks(lines):
        """
        Validate that each line in lines ends with a
        newline character and appends one if that is not the case.

        :param lines: A list of strings, representing lines.
        """

        return [line
                if line.endswith('\n')
                else line + '\n'
                for line in lines]

    @staticmethod
    def _generate_linebreaks(lines):
        """
        Validate that each line in lines ends with a
        newline character and appends one if that is not the case.
        Exception is the last line in the list.

        :param lines: A list of strings, representing lines.
        """

        if lines == []:
            return []

        return Diff._add_linebreaks(lines[:-1]) + [lines[-1]]
