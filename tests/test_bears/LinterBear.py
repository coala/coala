from coalib.bearlib.abstractions.Linter import linter


@linter(executable='echo',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<message>.*)')
class EchoBear:
    """
    A simple bear to test that collectors are importing also bears that are
    defined in another file *but* have baseclasses in the right file.

    (linter will create a new class that inherits from this class.)
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()
