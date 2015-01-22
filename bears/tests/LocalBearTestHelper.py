import unittest
from coalib.bears.LocalBear import LocalBear


class LocalBearTestHelper(unittest.TestCase):  # pragma: no cover
    """
    This is a helper class for simplification of testing of local bears.

    Please note that all abstraction will prepare the lines so you don't need to do that if you use them.

    If you miss some methods, get in contact with us, we'll be happy to help!
    """
    @staticmethod
    def prepare_lines(lines):
        """
        Adds a trailing newline to each line if needed. This is needed since the bears expect every line to have such a
        newline at the end.

        :param lines: The lines to be prepared. This list will be altered so you don't have to use the return value.
        :return: The lines if you want to reuse them directly.
        """
        for i, line in enumerate(lines):
            lines[i] = line if line.endswith("\n") else line+"\n"

        return lines

    def assertLinesValid(self, local_bear, lines, filename="default"):
        """
        Asserts that a check of the given lines with the given local bear does not yield any results.

        :param local_bear: The local bear to check with.
        :param lines: The lines to check. (List of strings)
        :param filename: The filename, if it matters.
        """
        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear, LocalBear, msg="The given bear is no local bear.")
        self.assertIsInstance(lines, list, msg="The given lines are not a list.")
        self.assertEqual(local_bear.run(filename, LocalBearTestHelper.prepare_lines(lines)),
                         [],
                         msg="The local bear '{}' yields a result "
                             "although it shouldn't.".format(local_bear.__class__.__name__))

    def assertLineValid(self, local_bear, line, filename="default"):
        """
        Asserts that a check of the given lines with the given local bear does not yield any results.

        :param local_bear: The local bear to check with.
        :param line: The lines to check. (List of strings)
        :param filename: The filename, if it matters.
        """
        self.assertLinesValid(local_bear, [line], filename)

    def assertLinesInvalid(self, local_bear, lines, filename="default"):
        """
        Asserts that a check of the given lines with the given local bear does yield any results.

        :param local_bear: The local bear to check with.
        :param lines: The lines to check. (List of strings)
        :param filename: The filename, if it matters.
        """
        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear, LocalBear, msg="The given bear is no local bear.")
        self.assertIsInstance(lines, list, msg="The given lines are not a list.")
        self.assertNotEqual(len(local_bear.run(filename, LocalBearTestHelper.prepare_lines(lines))),
                            0,
                            msg="The local bear '{}' yields no result "
                                "although it should.".format(local_bear.__class__.__name__))

    def assertLineInvalid(self, local_bear, line, filename="default"):
        """
        Asserts that a check of the given lines with the given local bear does yield any results.

        :param self: The unittest.TestCase object for assertions.
        :param local_bear: The local bear to check with.
        :param line: The lines to check. (List of strings)
        :param filename: The filename, if it matters.
        """
        self.assertLinesInvalid(local_bear, [line], filename)

    def assertLinesYieldResults(self, local_bear, lines, results, filename="default", check_order=False):
        """
        Asserts that a check of the given lines with the given local bear does yield exactly the given results.

        :param local_bear: The local bear to check with.
        :param lines: The lines to check. (List of strings)
        :param results: The expected results.
        :param filename: The filename, if it matters.
        :param check_order: Assert also that the results are in the same order (defaults to False)
        """
        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear, LocalBear, msg="The given bear is no local bear.")
        self.assertIsInstance(lines, list, msg="The given lines are not a list.")
        self.assertIsInstance(results, list, msg="The given results are not a list.")

        if not check_order:
            self.assertEqual(sorted(local_bear.run(filename, LocalBearTestHelper.prepare_lines(lines))),
                             sorted(results),
                             msg="The local bear '{}' yields not the right "
                                 "results or the order may be wrong.".format(local_bear.__class__.__name__))
        else:
            self.assertEqual(local_bear.run(filename, LocalBearTestHelper.prepare_lines(lines)),
                             results,
                             msg="The local bear '{}' yields not the right "
                                 "results or the order may be wrong.".format(local_bear.__class__.__name__))

    def assertLineYieldsResults(self, local_bear, line, results, filename="default", check_order=False):
        """
        Asserts that a check of the given line with the given local bear does yield exactly the given results.

        :param local_bear: The local bear to check with.
        :param line: The line to check. (String)
        :param results: The expected results.
        :param filename: The filename, if it matters.
        :param check_order: Assert also that the results are in the same order (defaults to False)
        """
        self.assertLinesYieldResults(local_bear, [line], results, filename, check_order)

    def assertLineYieldsResult(self, local_bear, line, result, filename="default"):
        """
        Asserts that a check of the given line with the given local bear does yield the given result.

        :param local_bear: The local bear to check with.
        :param line: The line to check. (String)
        :param result: The expected result.
        :param filename: The filename, if it matters.
        """
        self.assertLinesYieldResults(local_bear, [line], [result], filename, False)

    def assertLinesYieldResult(self, local_bear, lines, result, filename="default"):
        """
        Asserts that a check of the given lines with the given local bear does yield exactly the given result.

        :param local_bear: The local bear to check with.
        :param lines: The lines to check. (String)
        :param result: The expected result.
        :param filename: The filename, if it matters.
        """
        self.assertLinesYieldResults(local_bear, lines, [result], filename, False)
