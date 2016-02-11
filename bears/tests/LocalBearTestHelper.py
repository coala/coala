from queue import Queue
import unittest

from coalib.bears.LocalBear import LocalBear
from coalib.misc.ContextManagers import prepare_file
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

    def check_validity(self,
                       local_bear,
                       lines,
                       filename=None,
                       valid=True,
                       force_linebreaks=True,
                       create_tempfile=True,
                       tempfile_kwargs={}):
        """
        Asserts that a check of the given lines with the given local bear
        either yields or does not yield any results.

        :param local_bear:       The local bear to check with.
        :param lines:            The lines to check. (string if single line
                                 or List of strings)
        :param filename:         The filename, if it matters.
        :param valid:            Whether the lines are valid or not.
        :param force_linebreaks: Whether to append newlines at each line
                                 if needed. (Bears expect a \\n for every line)
        :param create_tempfile:  Whether to save lines in tempfile if needed.
        :param tempfile_kwargs:  Kwargs passed to tempfile.mkstemp().
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

        with prepare_file(lines,
                          filename,
                          force_linebreaks=force_linebreaks,
                          create_tempfile=create_tempfile,
                          tempfile_kwargs=tempfile_kwargs) as (lines, filename):

            bear_output = list(local_bear.execute(filename, lines))

            if valid:
                msg = ("The local bear '{}' yields a result although it "
                       "shouldn't.".format(local_bear.__class__.__name__))
                self.assertEqual(bear_output, [], msg=msg)
            else:
                msg = ("The local bear '{}' yields no result although it "
                       "should.".format(local_bear.__class__.__name__))
                self.assertNotEqual(len(bear_output), 0, msg=msg)

    def check_results(self,
                      local_bear,
                      lines,
                      results,
                      filename=None,
                      check_order=False,
                      force_linebreaks=True,
                      create_tempfile=True,
                      tempfile_kwargs={}):
        """
        Asserts that a check of the given lines with the given local bear does
        yield exactly the given results.

        :param local_bear:       The local bear to check with.
        :param lines:            The lines to check. (string if single line
                                 or List of strings)
        :param results:          The expected result or list of results.
        :param filename:         The filename, if it matters.
        :param force_linebreaks: Whether to append newlines at each line
                                 if needed. (Bears expect a \\n for every line)
        :param create_tempfile:  Whether to save lines in tempfile if needed.
        :param tempfile_kwargs:  Kwargs passed to tempfile.mkstemp().
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

        with prepare_file(lines,
                          filename,
                          force_linebreaks=force_linebreaks,
                          create_tempfile=create_tempfile,
                          tempfile_kwargs=tempfile_kwargs) as (lines, filename):

            msg = ("The local bear '{}' doesn't yield the right results. Or the"
                   " order may be wrong.".format(local_bear.__class__.__name__))
            bear_output = list(local_bear.execute(filename, lines))

            if not check_order:
                self.assertEqual(sorted(bear_output), sorted(results), msg=msg)
            else:
                self.assertEqual(bear_output, results, msg=msg)


def verify_local_bear(bear,
                      valid_files,
                      invalid_files,
                      filename=None,
                      settings={},
                      force_linebreaks=True,
                      create_tempfile=True,
                      tempfile_kwargs={}):
    """
    Generates a test for a local bear by checking the given valid and invalid
    file contents. Simply use it on your module level like:

    YourTestName = verify_local_bear(YourBear, (['valid line'],),
                                     (['invalid line'],))

    :param bear:             The Bear class to test.
    :param valid_files:      An iterable of files as a string list that won't
                             yield results.
    :param invalid_files:    An iterable of files as a string list that must
                             yield results.
    :param filename:         The filename to use for valid and invalid files.
    :param settings:         A dictionary of keys and values (both string) from
                             which settings will be created that will be made
                             available for the tested bear.
    :param force_linebreaks: Whether to append newlines at each line
                             if needed. (Bears expect a \\n for every line)
    :param create_tempfile:  Whether to save lines in tempfile if needed.
    :param tempfile_kwargs:  Kwargs passed to tempfile.mkstemp() if tempfile
                             needs to be created.
    :return:                 A unittest.TestCase object.
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
                self.check_validity(self.uut,
                                    file,
                                    filename,
                                    valid=True,
                                    force_linebreaks=force_linebreaks,
                                    create_tempfile=create_tempfile,
                                    tempfile_kwargs=tempfile_kwargs)

        def test_invalid_files(self):
            for file in invalid_files:
                self.check_validity(self.uut,
                                    file,
                                    filename,
                                    valid=False,
                                    force_linebreaks=force_linebreaks,
                                    create_tempfile=create_tempfile,
                                    tempfile_kwargs=tempfile_kwargs)

    return LocalBearTest
