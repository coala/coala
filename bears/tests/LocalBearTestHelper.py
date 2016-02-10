from contextlib import contextmanager, closing
from queue import Queue
from tempfile import NamedTemporaryFile
import unittest

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from bears.tests.BearTestHelper import generate_skip_decorator


@contextmanager
def prepare(lines, filename, prepare_lines, prepare_file):
    """
    Creates a temporary file (if filename is None) and saves the
    lines to it. Also adds a trailing newline to each line if needed.

    :param lines:         The lines to be prepared.
    :param filename:      The filename to be prepared.
                           - If it is None, A new tempfile will be created
                             (if prepare_file allows it).
                           - If it is a string, that is used as the filename.
                           - If it is a dictionary, it is passed as kwargs
                             to NamedTemporaryFile.
    :param prepare_lines: Whether to append newlines at each line if needed.
    :param prepare_file:  Whether to save lines in tempfile if needed.
    """
    if prepare_lines:
        for i, line in enumerate(lines):
            lines[i] = line if line.endswith("\n") else line + "\n"

    if not prepare_file and filename is None:
        filename = "dummy_file_name"

    if not isinstance(filename, str) and prepare_file:
        temp_file_kwargs = {}
        if isinstance(filename, dict):
            temp_file_kwargs = filename
        with NamedTemporaryFile(**temp_file_kwargs) as file:
            file.write(bytes("".join(lines), 'UTF-8'))
            yield lines, file.name
    else:
        yield lines, filename


class LocalBearTestHelper(unittest.TestCase):  # pragma: no cover
    """
    This is a helper class for simplification of testing of local bears.

    Please note that all abstraction will prepare the lines so you don't need
    to do that if you use them.

    If you miss some methods, get in contact with us, we'll be happy to help!
    """
    def check_valid(self,
                    local_bear,
                    lines,
                    filename,
                    valid=True,
                    prepare_lines=True,
                    prepare_file=True):
        """
        Asserts that a check of the given lines with the given local bear does
        not yield any results.

        :param local_bear:    The local bear to check with.
        :param lines:         The lines to check. (string or List of strings)
        :param filename:      The filename, if it matters.
        :param valid:         Whether the lines are valid or not.
        :param prepare_lines: Whether to append newlines at each line if
                              needed. Use this with caution when disabling,
                              since bears expect to have a \n at the end of
                              each line.
        :param prepare_file:  Whether to create tempfile is filename is None.
                              Use this with caution when disabling, since
                              some bears read the filename directly.
        """
        if isinstance(lines, str):
            lines = [lines]

        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear,
                              LocalBear,
                              msg="The given bear is not a local bear.")
        self.assertIsInstance(lines,
                              list,
                              msg="The given lines are not a list.")

        with prepare(lines, filename, prepare_lines, prepare_file) \
             as (lines, filename):
            if valid:
                self.assertEqual(
                    list(local_bear.execute(filename, lines)),
                    [],
                    msg="The local bear '{}' yields a result although it "
                        "shouldn't.".format(local_bear.__class__.__name__))
            else:
                self.assertNotEqual(
                    len(list(local_bear.execute(filename, lines))),
                    0,
                    msg="The local bear '{}' yields no result although it "
                        "should.".format(local_bear.__class__.__name__))

    def check_results(self,
                      local_bear,
                      lines,
                      filename,
                      results=[],
                      check_order=False,
                      prepare_lines=True,
                      prepare_file=True):
        """
        Asserts that a check of the given line with the given local bear does
        yield exactly the given results.

        :param local_bear:    The local bear to check with.
        :param lines:         The lines to check. (string or List of strings)
        :param filename:      The filename, if it matters.
        :param results:       The expected results.
        :param check_order:   Assert also that the results are in the same
                              order (defaults to False)
        :param prepare_lines: Whether to append newlines at each line if
                              needed. Use this with caution when disabling,
                              since bears expect to have a \n at the end of
                              each line.
        :param prepare_file:  Whether to create tempfile is filename is None.
                              Use this with caution when disabling, since
                              some bears read the filename directly.
        """
        if isinstance(lines, str):
            lines = [lines]
        if isinstance(results, Result):
            results = [results]

        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear,
                              LocalBear,
                              msg="The given bear is not a local bear.")
        self.assertIsInstance(lines,
                              list,
                              msg="The given lines are not a list.")
        self.assertIsInstance(results,
                              list,
                              msg="The given results are not a list.")

        msg = ("The local bear '{}' doesn't yield the right results or the "
               "order may be wrong.".format(local_bear.__class__.__name__))
        with prepare(lines, filename, prepare_lines, prepare_file) \
             as (lines, filename):
            if not check_order:
                self.assertEqual(sorted(local_bear.execute(filename, lines)),
                                 sorted(results),
                                 msg=msg)
            else:
                self.assertEqual(list(local_bear.execute(filename, lines)),
                                 results,
                                 msg=msg)


def verify_local_bear(bear,
                      valid_files=(),
                      invalid_files=(),
                      filename=None,
                      settings={}):
    """
    Generates a test for a local bear by checking the given valid and invalid
    file contents. Simply use it on your module level like:

    YourTestName = verify_local_bear(YourBear, (['valid line'],),
                                     (['invalid line'],))

    :param bear:          The Bear class to test.
    :param valid_files:   An iterable of files as a string list that won't
                          yield results.
    :param invalid_files: An iterable of files as a string list that must
                          yield results.
    :param filename:      The filename to use for valid and invalid files.
                           - If it is None, A new tempfile will be created
                             (if prepare_file allows it).
                           - If it is a string, that is used as the filename.
                           - If it is a dictionary, it is passed as kwargs
                             to NamedTemporaryFile.
    :param settings:      A dictionary of keys and values (both string) from
                          which settings will be created that will be made
                          available for the tested bear.
    :return:              A unittest.TestCase object.
    """
    @generate_skip_decorator(bear)
    class LocalBearTest(LocalBearTestHelper):

        def setUp(self):
            self.section = Section('name')
            self.uut = bear(self.section, Queue())
            for name, value in settings.items():
                self.section.append(Setting(name, value))

        def test_valid_files(self):
            for file in valid_files:
                self.check_valid(self.uut, file, filename, valid=True)

        def test_invalid_files(self):
            for file in invalid_files:
                self.check_valid(self.uut, file, filename, valid=False)

    return LocalBearTest
