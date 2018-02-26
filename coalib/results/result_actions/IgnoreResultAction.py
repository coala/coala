from coalib.bearlib.languages import Language
from coalib.bearlib.languages.Language import UnknownLanguageError
from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coala_utils.FileUtils import detect_encoding
from os.path import exists
from os.path import isfile
import shutil
import logging

from coala_utils.decorators import enforce_signature


class IgnoreResultAction(ResultAction):

    SUCCESS_MESSAGE = 'An ignore comment was added to your source code.'

    @staticmethod
    @enforce_signature
    def is_applicable(result: Result,
                      original_file_dict,
                      file_diff_dict,
                      applied_actions=()):
        """
        For being applicable, the result has to point to a number of files
        that have to exist i.e. have not been previously deleted.
        Additionally, the action should not have been applied to the current
        result before.
        """
        if IgnoreResultAction.__name__ in applied_actions:
            return 'An ignore comment was already added for this result.'

        if len(result.affected_code) == 0:
            return 'The result is not associated with any source code.'

        filenames = set(src.renamed_file(file_diff_dict)
                        for src in result.affected_code)
        if any(exists(filename) for filename in filenames):
            return True
        return ("The result is associated with source code that doesn't "
                'seem to exist.')

    def apply(self, result, original_file_dict, file_diff_dict, language: str,
              no_orig: bool=False):
        """
        Add (I)gnore comment
        """
        source_range = next(filter(lambda sr: exists(sr.file),
                                   result.affected_code))
        filename = source_range.file
        ignore_diff = Diff(original_file_dict[filename])
        line = original_file_dict[filename][source_range.start.line-1]
        spaces = ' '*(len(line)-len(line.lstrip()))

        ignore_comment, multiline = self.encase_ignore_comment(language, spaces)

        if not ignore_comment:
            return file_diff_dict

        original_line, new_line, position = self.get_diff(
                        result.origin, original_file_dict[filename],
                        source_range.start.line-1, ignore_comment, multiline)

        ignore_diff.change_line(position, original_line, new_line)

        if filename in file_diff_dict:
            ignore_diff = file_diff_dict[filename] + ignore_diff
        else:
            if not no_orig and isfile(filename):
                shutil.copy2(filename, filename + '.orig')

        file_diff_dict[filename] = ignore_diff

        new_filename = ignore_diff.rename if ignore_diff.rename else filename
        with open(new_filename, mode='w',
                  encoding=detect_encoding(new_filename)) as file:
            file.writelines(ignore_diff.modified)

        return file_diff_dict

    def encase_ignore_comment(self, language, spaces: str=''):
        r"""
        Returns a tuple consisting of a formattable string of Ignore
        Comment depending on the language and a boolean variable stating
        if the Comment is in Multiline format or not.
        Supports Single Line Comments

        :param language:
            The language in which the source file is written.
        :param spaces:
            The indentation of each line.

        >>> IgnoreResultAction().encase_ignore_comment("css")
        ('/* {} */\n', True)

        And Multiline Comments

        >>> IgnoreResultAction().encase_ignore_comment("c")
        ('// {}\n', False)
        """
        try:
            comment_delimiter = Language[
                language].get_default_version().comment_delimiter
            ignore_comment = (spaces + str(comment_delimiter) + ' {}\n')
            multiline = False
        except AttributeError:
            # singleline comments not supported by language
            try:
                multiline_comment_delimiter = Language[
                    language].get_default_version().multiline_comment_delimiters
                start_comment, end_comment = next(iter(
                                        multiline_comment_delimiter.items()))
                ignore_comment = (spaces + str(start_comment) + ' {} ' +
                                  str(end_comment) + '\n')
                multiline = True
            except UnknownLanguageError:
                # multiline comments also not supported by language
                logging.warning(
                    'coala does not support Ignore in "{language}". Consider'
                    ' opening an issue at https://github.com/coala/coala/issues'
                    ' so we can add support for this language.'.format(
                        language=language))
                ignore_comment = multiline = None

        return ignore_comment, multiline

    def get_diff(self, origin, file, index, ignore_comment, multiline):
        r"""
        Returns a tuple consisting of Original Line, Changed Line and
        its position in the file

        >>> ignore_comment = '// {}\n'
        >>> file = ['1\n', '2\n', '3\n']
        >>> IgnoreResultAction().get_diff('origin', file, 1,
        ...                               ignore_comment, False)
        ('2\n', '// Start Ignoring origin\n2\n// Stop Ignoring\n', 2)

        >>> file = ['1\n', '// Start Ignoring origin\n', '2\n',
        ...         '// Stop Ignoring\n', '3\n']
        >>> IgnoreResultAction().get_diff('origin2', file, 2,
        ...                               ignore_comment, False)
        ('// Start Ignoring origin\n', '// Start Ignoring origin, origin2\n', 2)

        >>> file = ['1\n', '// Start Ignoring origin\n', '2\n',
        ...         '// Stop Ignoring\n', '3\n']
        >>> for i in range(2,25):
        ...     _, file[1], _ = IgnoreResultAction().get_diff(
        ...                     'origin'+str(i), file, 2, ignore_comment, False)
        """
        if file[index+1] != ignore_comment.format('Stop Ignoring'):
            new_line = (ignore_comment.format('Start Ignoring ' + origin) +
                        file[index] + ignore_comment.format('Stop Ignoring'))
            original_line = file[index]
            position = index+1

        elif len(file[index-1] + ', ' + origin) > 80:
            new_line = file[index-1].split()
            new_line = (' '.join(new_line[1:len(new_line)-1])
                        if multiline is True
                        else
                        ' '.join(new_line[1:len(new_line)]))
            new_line = (ignore_comment.format(new_line + ',') +
                        ignore_comment.format(origin))
            original_line = file[index-1]
            position = index

        else:
            new_line = file[index-1].split()
            new_line = (' '.join(new_line[1:len(new_line)-1])
                        if multiline is True
                        else
                        ' '.join(new_line[1:len(new_line)]))
            new_line = ignore_comment.format(new_line + ', ' + origin)
            original_line = file[index-1]
            position = index

        return original_line, new_line, position
