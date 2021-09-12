import re

from coalib.bearlib import deprecate_settings
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.settings.Setting import typed_list, language
from coalib.bearlib.languages.Language import Language
from coalib.bearlib.aspects import map_setting_to_aspect
from coalib.bearlib.aspects.Formatting import (
    Formatting,
    LineLength,
)


class LineLengthTestBear(
        LocalBear,
        aspects={
            'detect': [
                LineLength,
            ]},
        ):
    LANGUAGES = {'All'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting'}

    @map_setting_to_aspect(
        max_line_length=LineLength.max_line_length,
    )
    @deprecate_settings(indent_size='tab_width')
    def run(self,
            filename,
            file,
            language: language = Language['Unknown'],
            max_line_length: int = 79,
            indent_size: int = SpacingHelper.DEFAULT_TAB_WIDTH,
            ignore_length_regex: typed_list(str) = (),
            ):
        '''
        Yields results for all lines longer than the given maximum line length.
        :param language:            Programming language of the source code.
        :param max_line_length:     Maximum number of characters for a line,
                                    the newline character being excluded.
        :param indent_size:         Number of spaces per indentation level.
        :param ignore_length_regex: Lines matching each of the regular
                                    expressions in this list will be ignored.
        '''
        if 'max_line_length' in language.attributes:
            max_line_length = language.max_line_length

        ignore_regexes = [re.compile(regex) for regex in ignore_length_regex]

        for line_number, line in enumerate(file):
            line = line.expandtabs(indent_size)
            if len(line) > max_line_length + 1:
                if any(regex.search(line) for regex in ignore_regexes):
                    continue

                yield Result.from_values(
                    origin=self,
                    message='Line is longer than allowed.' +
                            ' ({actual} > {maximum})'.format(
                                actual=len(line)-1,
                                maximum=max_line_length),
                    file=filename,
                    line=line_number + 1,
                    column=max_line_length + 1,
                    end_line=line_number + 1,
                    end_column=len(line),
                    aspect=Formatting(language),
                    )
