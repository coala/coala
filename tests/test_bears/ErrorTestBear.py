from coalib.bearlib.abstractions.Linter import linter


@linter(executable='I_do_not_exist',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<message>.*)')
class ErrorTestBear:
    """
    Causes error when run due to missing executable.
    """
    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()
