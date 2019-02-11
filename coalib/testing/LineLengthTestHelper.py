import logging
import queue

from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper


def verify_line_length(bear,
                       source_file,
                       filename=None,
                       settings={},
                       aspects=None,
                       force_linebreaks=True,
                       create_tempfile=True,
                       timeout=None,
                       tempfile_kwargs={}):
    """
    Generates a test for a local bear by checking the max_line_length setting.
    Simply use it on your module level like:

    YourTestName = verify_line_length(YourBear, 'source code',))

    :param bear:             The Bear class to test.
    :param source_file:      Source file as a string to test line length.
    :param filename:         The filename to use for valid and invalid files.
    :param settings:         A dictionary of keys and values (both string) from
                             which settings will be created that will be made
                             available for the tested bear.
    :param aspects:          A list of aspect objects along with the name
                             and value of their respective tastes.
    :param force_linebreaks: Whether to append newlines at each line
                             if needed. (Bears expect a \\n for every line)
    :param create_tempfile:  Whether to save lines in tempfile if needed.
    :param timeout:          Unused.  Use pytest-timeout or similar.
    :param tempfile_kwargs:  Kwargs passed to tempfile.mkstemp() if tempfile
                             needs to be created.
    :return:                 A unittest.TestCase object.
    """
    if timeout:
        logging.warning('timeout is ignored as the timeout set in the repo '
                        'configuration will be sufficient. Use pytest-timeout '
                        'or similar to achieve same result.')

    @generate_skip_decorator(bear)
    class LineLengthTest(LocalBearTestHelper):

        def setUp(self):
            self.section = Section('name')
            self.uut = bear(self.section,
                            queue.Queue())
            for name, value in settings.items():
                self.section.append(Setting(name, value))
            if aspects:
                self.section.aspects = aspects

        def test_source_file(self):
            max_line = max(source_file.splitlines(), key=len)
            max_line_length = len(max_line)
            self.section.append(Setting('max_line_length', max_line_length))
            self.check_validity(self.uut,
                                source_file.splitlines(keepends=True),
                                filename,
                                valid=True,
                                force_linebreaks=force_linebreaks,
                                create_tempfile=create_tempfile,
                                tempfile_kwargs=tempfile_kwargs)
            self.section.append(Setting('max_line_length', max_line_length - 1))
            self.check_validity(self.uut,
                                source_file.splitlines(keepends=True),
                                filename,
                                valid=False,
                                force_linebreaks=force_linebreaks,
                                create_tempfile=create_tempfile,
                                tempfile_kwargs=tempfile_kwargs)

    return LineLengthTest
