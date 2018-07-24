from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.bearlib.aspects import map_setting_to_aspect
from coalib.bearlib.aspects.Formatting import (
    Formatting,
    LineLength,
)
from coalib.bearlib.aspects import (
    AspectList,
    get as get_aspect,
)


class AspectsGeneralTestBear(
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
    CAN_FIX = {'Formatting'}

    @map_setting_to_aspect(
        max_line_length=LineLength.max_line_length,
    )
    def run(self,
            filename,
            file,
            max_line_length: int = 100,
            ):
        if file:
            for line in file:
                if len(line) > max_line_length + 1:
                    yield Result.from_values(
                                origin=self,
                                message='Line is longer than allowed.',
                                file=filename,
                                aspect=Formatting('Unknown'),
                                )
