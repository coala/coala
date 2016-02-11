from queue import Queue
import unittest

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from bears.tests.BearTestHelper import generate_skip_decorator


class LocalBearTestHelper(unittest.TestCase):  # pragma: no cover
    """
    This is a helper class for simplification of testing of local bears.

    Please note that all abstraction will prepare the lines so you don't need
    to do that if you use them.

    If you miss some methods, get in contact with us, we'll be happy to help!
    """
    @staticmethod
    def force_linebreaks(lines):
        """
        Adds a trailing newline to each line if needed. This is needed since
        the bears expect every line to have such a newline at the end.

        This function does not modify the given argument in-place, it returns
        a modified copy instead.

        :param lines: The lines to be prepared. This list will be altered so
                      you don't have to use the return value.
        :return:      The lines with a \n appended.
        """
        modified_lines = []
        for line in lines:
            modified_lines.append(line if line.endswith("\n") else line+"\n")

        return modified_lines

    def assertLinesValid(self,
                         local_bear,
                         lines,
                         filename="default",
                         valid=True,
                         force_linebreaks=True):
        """
        Asserts that a check of the given lines with the given local bear
        either yields or does not yield any results.

        :param local_bear:       The local bear to check with.
        :param lines:            The lines to check. (string if single line
                                 or List of strings)
        :param filename:         The filename, if it matters.
        :param valid:            Whether the lines are valid or not.
        :param force_linebreaks: Whether to append newlines at each line if
                                 needed. Use this with caution when disabling,
                                 since bears expect to have a \n at the end of
                                 each line.
\        """
        if isinstance(lines, str):
            lines = [lines]

        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear,
                              LocalBear,
                              msg="The given bear is no local bear.")
        self.assertIsInstance(lines,
                              list,
                              msg="The given lines are not a list.")

        if force_linebreaks:
            lines = LocalBearTestHelper.force_linebreaks(lines)
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

    def assertLinesYieldResults(self,
                                local_bear,
                                lines,
                                results,
                                filename="default",
                                check_order=False,
                                force_linebreaks=True):
        """
        Asserts that a check of the given lines with the given local bear does
        yield exactly the given results.

        :param local_bear:       The local bear to check with.
        :param lines:            The lines to check. (string if single line
                                 or List of strings)
        :param results:          The expected result or list of results.
        :param filename:         The filename, if it matters.
        :param force_linebreaks: Whether to append newlines at each line if
                                 needed. Use this with caution when disabling,
                                 since bears expect to have a \n at the end of
                                 each line.
        """
        if isinstance(lines, str):
            lines = [lines]
        if isinstance(results, Result):
            results = [results]

        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear,
                              LocalBear,
                              msg="The given bear is no local bear.")
        self.assertIsInstance(lines,
                              list,
                              msg="The given lines are not a list.")
        self.assertIsInstance(results,
                              list,
                              msg="The given results are not a list.")

        if force_linebreaks:
            lines = LocalBearTestHelper.force_linebreaks(lines)
        if not check_order:
            self.assertEqual(
                sorted(local_bear.execute(filename, lines)),
                sorted(results),
                msg="The local bear '{}' yields not the right results or the "
                    "order may be wrong.".format(
                    local_bear.__class__.__name__))
        else:
            self.assertEqual(
                list(local_bear.execute(filename, lines)),
                results,
                msg="The local bear '{}' yields not the right results or the "
                    "order may be wrong.".format(
                    local_bear.__class__.__name__))


def verify_local_bear(bear,
                      valid_files,
                      invalid_files,
                      filename='default',
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
                self.assertLinesValid(self.uut, file, filename, valid=True)

        def test_invalid_files(self):
            for file in invalid_files:
                self.assertLinesValid(self.uut, file, filename, valid=False)

    return LocalBearTest
