from queue import Queue
import unittest

from coalib.bears.LocalBear import LocalBear
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
    def prepare_lines(lines):
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
                         prepare_lines=True):
        """
        Asserts that a check of the given lines with the given local bear does
        not yield any results.

        :param local_bear:    The local bear to check with.
        :param lines:         The lines to check. (List of strings)
        :param filename:      The filename, if it matters.
        :param prepare_lines: Whether to append newlines at each line if
                              needed. Use this with caution when disabling,
                              since bears expect to have a \n at the end of
                              each line.
        """
        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear,
                              LocalBear,
                              msg="The given bear is no local bear.")
        self.assertIsInstance(lines,
                              list,
                              msg="The given lines are not a list.")

        if prepare_lines:
            lines = LocalBearTestHelper.prepare_lines(lines)

        self.assertEqual(
            list(local_bear.execute(filename, lines)),
            [],
            msg="The local bear '{}' yields a result although it "
                "shouldn't.".format(local_bear.__class__.__name__))

    def assertLineValid(self,
                        local_bear,
                        line,
                        filename="default",
                        prepare_lines=True):
        """
        Asserts that a check of the given lines with the given local bear does
        not yield any results.

        :param local_bear:    The local bear to check with.
        :param line:          The lines to check. (List of strings)
        :param filename:      The filename, if it matters.
        :param prepare_lines: Whether to append newlines at each line if
                              needed. Use this with caution when disabling,
                              since bears expect to have a \n at the end of
                              each line.
        """
        self.assertLinesValid(local_bear, [line], filename, prepare_lines)

    def assertLinesInvalid(self,
                           local_bear,
                           lines,
                           filename="default",
                           prepare_lines=True):
        """
        Asserts that a check of the given lines with the given local bear does
        yield any results.

        :param local_bear:    The local bear to check with.
        :param lines:         The lines to check. (List of strings)
        :param filename:      The filename, if it matters.
        :param prepare_lines: Whether to append newlines at each line if
                              needed. Use this with caution when disabling,
                              since bears expect to have a \n at the end of
                              each line.
        """
        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear,
                              LocalBear,
                              msg="The given bear is no local bear.")
        self.assertIsInstance(lines,
                              list,
                              msg="The given lines are not a list.")

        if prepare_lines:
            lines = LocalBearTestHelper.prepare_lines(lines)

        self.assertNotEqual(
            len(list(local_bear.execute(filename, lines))),
            0,
            msg="The local bear '{}' yields no result although it "
                "should.".format(local_bear.__class__.__name__))

    def assertLineInvalid(self,
                          local_bear,
                          line,
                          filename="default",
                          prepare_lines=True):
        """
        Asserts that a check of the given lines with the given local bear does
        yield any results.

        :param self:          The unittest.TestCase object for assertions.
        :param local_bear:    The local bear to check with.
        :param line:          The lines to check. (List of strings)
        :param filename:      The filename, if it matters.
        :param prepare_lines: Whether to append newlines at each line if
                              needed. Use this with caution when disabling,
                              since bears expect to have a \n at the end of
                              each line.
        """
        self.assertLinesInvalid(local_bear, [line], filename, prepare_lines)

    def assertLinesYieldResults(self,
                                local_bear,
                                lines,
                                results,
                                filename="default",
                                check_order=False):
        """
        Asserts that a check of the given lines with the given local bear does
        yield exactly the given results.

        :param local_bear:  The local bear to check with.
        :param lines:       The lines to check. (List of strings)
        :param results:     The expected results.
        :param filename:    The filename, if it matters.
        :param check_order: Assert also that the results are in the same order
                            (defaults to False)
        """
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

        if not check_order:
            self.assertEqual(
                sorted(local_bear.execute(
                    filename,
                    LocalBearTestHelper.prepare_lines(lines))),
                sorted(results),
                msg="The local bear '{}' yields not the right results or the "
                    "order may be wrong.".format(
                    local_bear.__class__.__name__))
        else:
            self.assertEqual(
                list(local_bear.execute(
                    filename,
                    LocalBearTestHelper.prepare_lines(lines))),
                results,
                msg="The local bear '{}' yields not the right results or the "
                    "order may be wrong.".format(
                    local_bear.__class__.__name__))

    def assertLineYieldsResults(self,
                                local_bear,
                                line,
                                results,
                                filename="default",
                                check_order=False):
        """
        Asserts that a check of the given line with the given local bear does
        yield exactly the given results.

        :param local_bear:  The local bear to check with.
        :param line:        The line to check. (String)
        :param results:     The expected results.
        :param filename:    The filename, if it matters.
        :param check_order: Assert also that the results are in the same order
                            (defaults to False)
        """
        self.assertLinesYieldResults(local_bear,
                                     [line],
                                     results,
                                     filename,
                                     check_order)

    def assertLineYieldsResult(self,
                               local_bear,
                               line,
                               result,
                               filename="default"):
        """
        Asserts that a check of the given line with the given local bear does
        yield the given result.

        :param local_bear: The local bear to check with.
        :param line:       The line to check. (String)
        :param result:     The expected result.
        :param filename:   The filename, if it matters.
        """
        self.assertLinesYieldResults(local_bear,
                                     [line],
                                     [result],
                                     filename,
                                     False)

    def assertLinesYieldResult(self,
                               local_bear,
                               lines,
                               result,
                               filename="default"):
        """
        Asserts that a check of the given lines with the given local bear does
        yield exactly the given result.

        :param local_bear: The local bear to check with.
        :param lines:      The lines to check. (String)
        :param result:     The expected result.
        :param filename:   The filename, if it matters.
        """
        self.assertLinesYieldResults(local_bear,
                                     lines,
                                     [result],
                                     filename,
                                     False)


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
                self.assertLinesValid(self.uut, file, filename=filename)

        def test_invalid_files(self):
            for file in invalid_files:
                self.assertLinesInvalid(self.uut, file, filename=filename)

    return LocalBearTest
