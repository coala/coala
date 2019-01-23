from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.bearlib.aspects import map_setting_to_aspect
from coalib.bearlib.aspects.Formatting import (
    Formatting,
    LineLength,
)
class LineLengthTestBear(
      LocalBear,
        aspects ={
                'detect': [
                    LineLength,
                ]}
        ):
    LANGUAGES = {'all'}
    @map_setting_to_aspect(
        max_line_length = LineLength.max_line_length,
    )
    def run(self,
            filename,
            file,
            max_line_length: int = 79):
            '''
            Detects if a line has more then ``max_line_length`` characters.
            :param max_line_length:
                Maximum no of characters that are allowed in a line.
                Default is 79.
            '''
            if file:
                for line in file:
                    if len(line) > max_line_length + 1:
                        yield Result.from_values(
                                    origin = self,
                                    message = 'Line is longer then allowed.',
                                    severity= RESULT_SEVERITY.NORMAL,
                                    file = filename)
