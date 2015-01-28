"""
A Diff result represents a difference for one file.
"""
from coalib.results.LineDiff import LineDiff


class ConflictError(Exception):
    pass


class Diff:
    def __init__(self):
        self._changes = {}

    def _get_change(self, line_nr, min_line=1):
        if not isinstance(line_nr, int):
            raise TypeError("line_nr needs to be an integer.")
        if line_nr < min_line:
            raise ValueError("The given line number is not allowed.")

        return self._changes.get(line_nr, LineDiff())

    def __len__(self):
        return len(self._changes)

    def apply(self, file):
        """
        Applies this diff to the given file.

        :param file: A list of all lines in the file. (readlines) Will not be modified.
        :return: The modified file.
        """
        result = []
        current_line = 0

        # Note that line_nr counts from _1_ although 0 is possible when inserting lines before everything
        for line_nr in sorted(self._changes):
            result.extend(file[current_line:max(line_nr-1, 0)])
            linediff = self._changes[line_nr]
            if not linediff.delete and not linediff.change and line_nr > 0:
                result.append(file[line_nr-1])
            elif linediff.change:
                result.append(linediff.change[1])

            if linediff.add_after:
                result.extend(linediff.add_after)

            current_line = line_nr

        result.extend(file[current_line:])

        return result

    def __add__(self, other):
        """
        Adds another diff to this one. Will throw an exception if this is not possible.
        """
        if not isinstance(other, Diff):
            raise TypeError("Only diffs can be added to a diff.")

        for line_nr in other._changes:
            change = other._changes[line_nr]
            if change.delete is True:
                self.delete_line(line_nr)
            if change.add_after is not False:
                self.add_lines(line_nr, change.add_after)
            if change.change is not False:
                self.change_line(line_nr, change.change[0], change.change[1])

        return self

    def delete_line(self, line_nr):
        """
        Mark the given line nr as deleted. The first line is line number 1.
        """
        linediff = self._get_change(line_nr)
        linediff.delete = True
        self._changes[line_nr] = linediff

    def add_lines(self, line_nr_before, lines):
        """
        Adds lines after the given line number.

        :param line_nr_before: Line number of the line before the additions. Use 0 for insert lines before everything.
        :param lines: A list of lines to add.
        """
        if lines == []:
            return  # No action

        linediff = self._get_change(line_nr_before, min_line=0)
        if linediff.add_after is not False:
            raise ConflictError("Cannot add lines after the given line since there are already lines.")

        linediff.add_after = lines
        self._changes[line_nr_before] = linediff

    def change_line(self, line_nr, original_line, replacement):
        """
        Changes the given line with the given line number. The replacement will be there instead.
        """
        linediff = self._get_change(line_nr)
        if linediff.change is not False:
            raise ConflictError("An already changed line cannot be changed.")

        linediff.change = (original_line, replacement)
        self._changes[line_nr] = linediff
