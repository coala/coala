from pygments.lexers import guess_lexer_for_filename
from pyprint.ConsolePrinter import ConsolePrinter

from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.result_actions.ShowPatchAction import ShowPatchAction
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.parsing.FilterHelper import apply_filters
from coalib.coala_modes import mode_normal
from coalib.parsing.DefaultArgParser import default_arg_parser


OBJECT_INDEX = FILENAME_INDEX = 0
DEFAULT_BEAR = 'SpaceConsistencyBear'


def show_possibilities(console_printer, i, action):
    console_printer.print('[{:>4}]  {}. Apply patch (\'{}\')'.format('', i,
                                                                     action))


def create_arg_parser(files, bears):
    """
    A function that generates a `default_arg_parser`.

    :param files: A list that contains filenames.
    :param bears: A list that contains name of bears.
    :return:      An object of type `default_arg_parser`.
    """
    args = default_arg_parser().parse_args()
    args.files = files
    args.bears = bears
    args.default_actions = '*: ApplyPatchAction'

    return args


def filter_bears(language):
    """
    Filter bears by language.

    :param language: The language to filter with.
    :return:         A list of bears.
    """
    return list(apply_filters([['language', language]], None)[0]['cli'])


def find_language(filename):
    """
    Find the language used in `filename`.

    :param filename: The name of the file.
    :return:         The language used.
    """

    return guess_lexer_for_filename(filename, 'Error, no file '
                                    'found').name


class DefaultBear():
    def __init__(self):
        self.name = DEFAULT_BEAR


class GeneratePatchesAction(ResultAction):
    SUCCESS_MESSAGE = 'Patch generated successfully.'

    is_applicable = staticmethod(ShowPatchAction.is_applicable)

    def apply(self,
              result,
              original_file_dict,
              file_diff_dict):
        """
        (G)enerate patches
        """

        console_printer = ConsolePrinter()
        log_printer = LogPrinter()
        to_filename = sorted(result.diffs.items())[OBJECT_INDEX][FILENAME_INDEX]

        filtered_bears = filter_bears(find_language(to_filename))
        filtered_bears.insert(0, DefaultBear())
        possible_options = [b.name for b in filtered_bears]

        console_printer.print('[{:>4}] *0. Do Nothing'.format(''))

        # Let the user choose a bear that wants to apply on the files
        for i, action in enumerate(possible_options, 1):
            show_possibilities(console_printer, i, action)

        choose_action = str(input('[{:>4}]  Enter a number: '.format('')))
        if choose_action is '' or choose_action is '0':
            return False

        choose_action = int(choose_action)
        chosen_bear = [possible_options[choose_action - 1]]

        return mode_normal(console_printer, log_printer, create_arg_parser([
            to_filename], chosen_bear), debug=False)
