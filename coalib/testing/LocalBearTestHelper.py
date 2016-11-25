import queue
import unittest
from contextlib import contextmanager

import pytest

from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.bears.LocalBear import LocalBear
from coala_utils.ContextManagers import prepare_file
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@contextmanager
def execute_bear(bear, *args, **kwargs):
    try:
        bear_output_generator = bear.execute(*args, **kwargs)
        assert bear_output_generator is not None, \
            'Bear returned None on execution\n'
        yield bear_output_generator
    except Exception as err:
        msg = []
        while not bear.message_queue.empty():
            msg.append(bear.message_queue.get().message)
        raise AssertionError(str(err) + ' \n' + '\n'.join(msg))
    return list(bear_output_generator)


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
        :param lines:            The lines to check. (List of strings)
        :param filename:         The filename, if it matters.
        :param valid:            Whether the lines are valid or not.
        :param force_linebreaks: Whether to append newlines at each line
                                 if needed. (Bears expect a \\n for every line)
        :param create_tempfile:  Whether to save lines in tempfile if needed.
        :param tempfile_kwargs:  Kwargs passed to tempfile.mkstemp().
        """
        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear,
                              LocalBear,
                              msg='The given bear is not a local bear.')
        self.assertIsInstance(lines,
                              (list, tuple),
                              msg='The given lines are not a list.')

        with prepare_file(lines, filename,
                          force_linebreaks=force_linebreaks,
                          create_tempfile=create_tempfile,
                          tempfile_kwargs=tempfile_kwargs) as (file, fname), \
                execute_bear(local_bear, fname, file) as bear_output:
            if valid:
                msg = ("The local bear '{}' yields a result although it "
                       "shouldn't.".format(local_bear.__class__.__name__))
                self.assertEqual(bear_output, [], msg=msg)
            else:
                msg = ("The local bear '{}' yields no result although it "
                       'should.'.format(local_bear.__class__.__name__))
                self.assertNotEqual(len(bear_output), 0, msg=msg)
            return bear_output

    def check_results(self,
                      local_bear,
                      lines,
                      results,
                      filename=None,
                      check_order=False,
                      force_linebreaks=True,
                      create_tempfile=True,
                      tempfile_kwargs={},
                      settings={}):
        """
        Asserts that a check of the given lines with the given local bear does
        yield exactly the given results.

        :param local_bear:       The local bear to check with.
        :param lines:            The lines to check. (List of strings)
        :param results:          The expected list of results.
        :param filename:         The filename, if it matters.
        :param force_linebreaks: Whether to append newlines at each line
                                 if needed. (Bears expect a \\n for every line)
        :param create_tempfile:  Whether to save lines in tempfile if needed.
        :param tempfile_kwargs:  Kwargs passed to tempfile.mkstemp().
        :param settings:         A dictionary of keys and values (both strings)
                                 from which settings will be created that will
                                 be made available for the tested bear.
        """
        assert isinstance(self, unittest.TestCase)
        self.assertIsInstance(local_bear,
                              LocalBear,
                              msg='The given bear is not a local bear.')
        self.assertIsInstance(lines,
                              (list, tuple),
                              msg='The given lines are not a list.')
        self.assertIsInstance(results,
                              list,
                              msg='The given results are not a list.')

        with prepare_file(lines, filename,
                          force_linebreaks=force_linebreaks,
                          create_tempfile=create_tempfile,
                          tempfile_kwargs=tempfile_kwargs) as (file, fname), \
                execute_bear(local_bear, fname, file,
                             **settings) as bear_output:
            msg = ("The local bear '{}' doesn't yield the right results. Or "
                   'the order may be wrong.'
                   .format(local_bear.__class__.__name__))
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
                      timeout=None,
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
    :param timeout:          The total time to run the test for.
    :param tempfile_kwargs:  Kwargs passed to tempfile.mkstemp() if tempfile
                             needs to be created.
    :return:                 A unittest.TestCase object.
    """
    @pytest.mark.timeout(timeout)
    @generate_skip_decorator(bear)
    class LocalBearTest(LocalBearTestHelper):

        def setUp(self):
            self.section = Section('name')
            self.uut = bear(self.section,
                            queue.Queue())
            for name, value in settings.items():
                self.section.append(Setting(name, value))

        def test_valid_files(self):
            self.assertIsInstance(valid_files, (list, tuple))
            for file in valid_files:
                self.check_validity(self.uut,
                                    file.splitlines(keepends=True),
                                    filename,
                                    valid=True,
                                    force_linebreaks=force_linebreaks,
                                    create_tempfile=create_tempfile,
                                    tempfile_kwargs=tempfile_kwargs)

        def test_invalid_files(self):
            self.assertIsInstance(invalid_files, (list, tuple))
            for file in invalid_files:
                self.check_validity(self.uut,
                                    file.splitlines(keepends=True),
                                    filename,
                                    valid=False,
                                    force_linebreaks=force_linebreaks,
                                    create_tempfile=create_tempfile,
                                    tempfile_kwargs=tempfile_kwargs)

    return LocalBearTest
