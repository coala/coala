from termcolor import colored

try:
    # This import has side effects and is needed to make input() behave nicely
    import readline  # pylint: disable=unused-import
except ImportError:  # pragma: no cover
    pass
import os.path

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.misc.DictUtilities import inverse_dicts
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.results.Result import Result
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction
from coalib.results.result_actions.PrintDebugMessageAction import (
    PrintDebugMessageAction)
from coalib.results.result_actions.PrintMoreInfoAction import (
    PrintMoreInfoAction)
from coalib.results.result_actions.ShowPatchAction import ShowPatchAction
from coalib.results.RESULT_SEVERITY import (
    RESULT_SEVERITY, RESULT_SEVERITY_COLORS)
from coalib.settings.Setting import Setting

from pygments import highlight
from pygments.formatters import (TerminalTrueColorFormatter,
                                 TerminalFormatter)
from pygments.filters import VisibleWhitespaceFilter
from pygments.lexers import TextLexer, get_lexer_for_filename
from pygments.style import Style
from pygments.token import Token
from pygments.util import ClassNotFound


class BackgroundSourceRangeStyle(Style):
    styles = {
        Token: 'bold bg:#BB4D3E #111'
    }


class BackgroundMessageStyle(Style):
    styles = {
        Token: 'bold bg:#eee #111'
    }


def highlight_text(text, lexer=TextLexer(), style=None):
    if style:
        formatter = TerminalTrueColorFormatter(style=style)
    else:
        formatter = TerminalTrueColorFormatter()
    return highlight(text, lexer, formatter)[:-1]


STR_GET_VAL_FOR_SETTING = ("Please enter a value for the setting \"{}\" ({}) "
                           "needed by {}: ")
STR_LINE_DOESNT_EXIST = ("The line belonging to the following result "
                         "cannot be printed because it refers to a line "
                         "that doesn't seem to exist in the given file.")
STR_PROJECT_WIDE = "Project wide:"
FILE_NAME_COLOR = "blue"
FILE_LINES_COLOR = "blue"
CAPABILITY_COLOR = "green"
HIGHLIGHTED_CODE_COLOR = 'red'
SUCCESS_COLOR = 'green'
REQUIRED_SETTINGS_COLOR = 'green'
CLI_ACTIONS = (OpenEditorAction(),
               ApplyPatchAction(),
               PrintDebugMessageAction(),
               PrintMoreInfoAction(),
               ShowPatchAction())
DIFF_EXCERPT_MAX_SIZE = 4


def format_lines(lines, line_nr=""):
    return '\n'.join("|{:>4}| {}".format(line_nr, line)
                     for line in lines.rstrip("\n").split('\n'))


def print_section_beginning(console_printer, section):
    """
    Will be called after initialization current_section in
    begin_section()

    :param console_printer: Object to print messages on the console.
    :param section:         The section that will get executed now.
    """
    console_printer.print("Executing section {name}...".format(
        name=section.name))


def nothing_done(log_printer):
    """
    Will be called after processing a coafile when nothing had to be done,
    i.e. no section was enabled/targeted.

    :param log_printer: A LogPrinter object.
    """
    log_printer.warn("No existent section was targeted or enabled. "
                     "Nothing to do.")


def acquire_actions_and_apply(console_printer,
                              log_printer,
                              section,
                              file_diff_dict,
                              result,
                              file_dict,
                              cli_actions=None):
    """
    Acquires applicable actions and applies them.

    :param console_printer: Object to print messages on the console.
    :param log_printer:     Printer responsible for logging the messages.
    :param section:         Name of section to which the result belongs.
    :param file_diff_dict:  Dictionary containing filenames as keys and Diff
                            objects as values.
    :param result:          A derivative of Result.
    :param file_dict:       A dictionary containing all files with filename as
                            key.
    :param cli_actions:     The list of cli actions available.
    """
    cli_actions = CLI_ACTIONS if cli_actions is None else cli_actions
    failed_actions = set()
    while True:
        actions = []
        for action in cli_actions:
            if action.is_applicable(result, file_dict, file_diff_dict):
                actions.append(action)

        if actions == []:
            return

        action_dict = {}
        metadata_list = []
        for action in actions:
            metadata = action.get_metadata()
            action_dict[metadata.name] = action
            metadata_list.append(metadata)

        # User can always choose no action which is guaranteed to succeed
        if not ask_for_action_and_apply(log_printer,
                                        console_printer,
                                        section,
                                        metadata_list,
                                        action_dict,
                                        failed_actions,
                                        result,
                                        file_diff_dict,
                                        file_dict):
            break


def print_lines(console_printer,
                file_dict,
                section,
                sourcerange):
    """
    Prints the lines between the current and the result line. If needed
    they will be shortened.

    :param console_printer: Object to print messages on the console.
    :param file_dict:       A dictionary containing all files as values with
                            filenames as key.
    :param sourcerange:     The SourceRange object referring to the related
                            lines to print.
    """
    for i in range(sourcerange.start.line, sourcerange.end.line + 1):
        # Print affected file's line number in the sidebar.
        console_printer.print(format_lines(lines='', line_nr=i),
                              color=FILE_LINES_COLOR,
                              end='')

        line = file_dict[sourcerange.file][i - 1].rstrip("\n")
        try:
            lexer = get_lexer_for_filename(sourcerange.file)
        except ClassNotFound:
            lexer = TextLexer()
        lexer.add_filter(VisibleWhitespaceFilter(
            spaces="•", tabs=True,
            tabsize=SpacingHelper.DEFAULT_TAB_WIDTH))
        # highlight() combines lexer and formatter to output a ``str``
        # object.
        printed_chars = 0
        if i == sourcerange.start.line and sourcerange.start.column:
            console_printer.print(highlight_text(
                line[:sourcerange.start.column-1], lexer), end='')

            printed_chars = sourcerange.start.column-1

        if i == sourcerange.end.line and sourcerange.end.column:
            console_printer.print(highlight_text(
                line[printed_chars:sourcerange.end.column-1],
                lexer, BackgroundSourceRangeStyle), end='')

            console_printer.print(highlight_text(
                line[sourcerange.end.column-1:], lexer), end='')
            console_printer.print("")

        else:
            console_printer.print(highlight_text(
                line[printed_chars:], lexer), end='')
            console_printer.print("")


def print_result(console_printer,
                 log_printer,
                 section,
                 file_diff_dict,
                 result,
                 file_dict,
                 interactive=True):
    """
    Prints the result to console.

    :param console_printer: Object to print messages on the console.
    :param log_printer:     Printer responsible for logging the messages.
    :param section:         Name of section to which the result belongs.
    :param file_diff_dict:  Dictionary containing filenames as keys and Diff
                            objects as values.
    :param result:          A derivative of Result.
    :param file_dict:       A dictionary containing all files with filename as
                            key.
    :interactive:           Variable to check wether or not to
                            offer the user actions interactively.
    """
    if not isinstance(result, Result):
        log_printer.warn("One of the results can not be printed since it is "
                         "not a valid derivative of the coala result "
                         "class.")
        return

    console_printer.print(format_lines("[{sev}] {bear}:".format(
        sev=RESULT_SEVERITY.__str__(result.severity), bear=result.origin)),
        color=RESULT_SEVERITY_COLORS[result.severity])
    lexer = TextLexer()
    result.message = highlight_text(result.message, lexer,
                                    BackgroundMessageStyle)
    console_printer.print(format_lines(result.message))

    if interactive:
        cli_actions = CLI_ACTIONS
        show_patch_action = ShowPatchAction()
        if show_patch_action.is_applicable(result, file_dict, file_diff_dict):
            diff_size = sum(len(diff) for diff in result.diffs.values())
            if diff_size <= DIFF_EXCERPT_MAX_SIZE:
                show_patch_action.apply_from_section(result,
                                                     file_dict,
                                                     file_diff_dict,
                                                     section)
                cli_actions = tuple(action for action in cli_actions
                                    if not isinstance(action, ShowPatchAction))
            else:
                print_diffs_info(result.diffs, console_printer)
        acquire_actions_and_apply(console_printer,
                                  log_printer,
                                  section,
                                  file_diff_dict,
                                  result,
                                  file_dict,
                                  cli_actions)


def print_diffs_info(diffs, printer):
    for filename, diff in sorted(diffs.items()):
        additions, deletions = diff.stats()
        printer.print(
            format_lines("+{additions} -{deletions} in {file}".format(
                file=filename,
                additions=additions,
                deletions=deletions)),
            color='green')


def print_results_formatted(log_printer,
                            section,
                            result_list,
                            *args):
    format_str = str(section.get(
        "format_str",
        "id:{id}:origin:{origin}:file:{file}:line:{line}:column:"
        "{column}:end_line:{end_line}:end_column:{end_column}:severity:"
        "{severity}:severity_str:{severity_str}:message:{message}"))
    for result in result_list:
        severity_str = RESULT_SEVERITY.__str__(result.severity)
        try:
            if len(result.affected_code) == 0:
                print(format_str.format(file=None,
                                        line=None,
                                        end_line=None,
                                        column=None,
                                        end_column=None,
                                        severity_str=severity_str,
                                        **result.__dict__))
                continue

            for range in result.affected_code:
                print(format_str.format(file=range.start.file,
                                        line=range.start.line,
                                        end_line=range.end.line,
                                        column=range.start.column,
                                        end_column=range.end.column,
                                        severity_str=severity_str,
                                        **result.__dict__))
        except KeyError as exception:
            log_printer.log_exception(
                "Unable to print the result with the given format string.",
                exception)


def print_affected_files(console_printer,
                         log_printer,
                         section,
                         result,
                         file_dict,
                         color=True):
    """
    Prints all the affected files and affected lines within them.

    :param console_printer: Object to print messages on the console.
    :param log_printer:     Printer responsible for logging the messages.
    :param section:         The section to which the results belong to.
    :param result:          The result to print the context for.
    :param file_dict:       A dictionary containing all files with filename as
                            key.
    :param color:           Boolean variable to print the results in color or
                            not. Can be used for testing.
    """
    if len(result.affected_code) == 0:
        console_printer.print("\n" + STR_PROJECT_WIDE,
                              color=FILE_NAME_COLOR)
    else:
        for sourcerange in result.affected_code:
            if (
                    sourcerange.file is not None and
                    sourcerange.file not in file_dict):
                log_printer.warn("The context for the result ({}) cannot "
                                 "be printed because it refers to a file "
                                 "that doesn't seem to exist ({})"
                                 ".".format(result, sourcerange.file))
            else:
                print_affected_lines(console_printer,
                                     file_dict,
                                     section,
                                     sourcerange)


def print_results_no_input(log_printer,
                           section,
                           result_list,
                           file_dict,
                           file_diff_dict,
                           color=True):
    """
    Prints all non interactive results in a section

    :param log_printer:    Printer responsible for logging the messages.
    :param section:        The section to which the results belong to.
    :param result_list:    List containing the results
    :param file_dict:      A dictionary containing all files with filename as
                           key.
    :param file_diff_dict: A dictionary that contains filenames as keys and
                           diff objects as values.
    :param color:          Boolean variable to print the results in color or
                           not. Can be used for testing.
    """
    console_printer = ConsolePrinter(print_colored=color)
    for result in result_list:

        print_affected_files(console_printer,
                             log_printer,
                             section,
                             result,
                             file_dict,
                             color=color)

        print_result(console_printer,
                     log_printer,
                     section,
                     file_diff_dict,
                     result,
                     file_dict,
                     interactive=False)


def print_results(log_printer,
                  section,
                  result_list,
                  file_dict,
                  file_diff_dict,
                  color=True):
    """
    Prints all the results in a section.

    :param log_printer:    Printer responsible for logging the messages.
    :param section:        The section to which the results belong to.
    :param result_list:    List containing the results
    :param file_dict:      A dictionary containing all files with filename as
                           key.
    :param file_diff_dict: A dictionary that contains filenames as keys and
                           diff objects as values.
    :param color:          Boolean variable to print the results in color or
                           not. Can be used for testing.
    """
    console_printer = ConsolePrinter(print_colored=color)

    for result in sorted(result_list):

        print_affected_files(console_printer,
                             log_printer,
                             section,
                             result,
                             file_dict,
                             color=color)

        print_result(console_printer,
                     log_printer,
                     section,
                     file_diff_dict,
                     result,
                     file_dict)


def print_affected_lines(console_printer, file_dict, section, sourcerange):
    """
    Prints the lines affected by the bears.

    :param console_printer:    Object to print messages on the console.
    :param file_dict:          A dictionary containing all files with filename
                               as key.
    :param section:            The section to which the results belong to.
    :param sourcerange:        The SourceRange object referring to the related
                               lines to print.
    """
    console_printer.print("\n" + os.path.relpath(sourcerange.file),
                          color=FILE_NAME_COLOR)

    if sourcerange.start.line is not None:
        if len(file_dict[sourcerange.file]) < sourcerange.end.line:
            console_printer.print(format_lines(lines=STR_LINE_DOESNT_EXIST,
                                               line_nr=sourcerange.end.line))
        else:
            print_lines(console_printer,
                        file_dict,
                        section,
                        sourcerange)


def join_names(values):
    """
    Produces a string by concatenating the items in ``values`` with
    commas, except the last element, which is concatenated with an "and".

    >>> join_names(["apples", "bananas", "oranges"])
    'apples, bananas and oranges'
    >>> join_names(["apples", "bananas"])
    'apples and bananas'
    >>> join_names(["apples"])
    'apples'

    :param values:
        A list of strings.
    :return:
        The concatenated string.
    """
    if len(values) > 1:
        return ", ".join(values[:-1]) + " and " + values[-1]
    else:
        return values[0]


def require_setting(setting_name, arr):
    """
    This method is responsible for prompting a user about a missing setting and
    taking its value as input from the user.

    :param setting_name: Name of the setting missing
    :param arr:          A list containing a description in [0] and the name
                         of the bears who need this setting in [1] and
                         following.
    """
    needed = join_names(arr[1:])

    # Don't use input, it can't deal with escapes!
    print(colored(STR_GET_VAL_FOR_SETTING.format(setting_name, arr[0], needed),
                  REQUIRED_SETTINGS_COLOR))
    return input()


def acquire_settings(log_printer, settings_names_dict):
    """
    This method prompts the user for the given settings.

    :param log_printer:
        Printer responsible for logging the messages. This is needed to comply
        with the interface.
    :param settings_names_dict:
        A dictionary with the settings name as key and a list containing a
        description in [0] and the name of the bears who need this setting in
        [1] and following.

                        Example:

    ::

        {"UseTabs": ["describes whether tabs should be used instead of spaces",
                     "SpaceConsistencyBear",
                     "SomeOtherBear"]}

    :return:
        A dictionary with the settings name as key and the given value as
        value.
    """
    if not isinstance(settings_names_dict, dict):
        raise TypeError("The settings_names_dict parameter has to be a "
                        "dictionary.")

    result = {}
    for setting_name, arr in sorted(settings_names_dict.items(),
                                    key=lambda x: (join_names(x[1][1:]), x[0])):
        value = require_setting(setting_name, arr)
        result.update({setting_name: value} if value is not None else {})

    return result


def get_action_info(section, action, failed_actions):
    """
    Gets all the required Settings for an action. It updates the section with
    the Settings.

    :param section:         The section the action corresponds to.
    :param action:          The action to get the info for.
    :param failed_actions:  A set of all actions that have failed. A failed
                            action remains in the list until it is successfully
                            executed.
    :return:                Action name and the updated section.
    """
    params = action.non_optional_params

    for param_name in params:
        if param_name not in section or action.name in failed_actions:
            question = format_lines(
                "Please enter a value for the parameter '{}' ({}): "
                .format(param_name, params[param_name][0]))
            section.append(Setting(param_name, input(question)))

    return action.name, section


def choose_action(console_printer, actions):
    """
    Presents the actions available to the user and takes as input the action
    the user wants to choose.

    :param console_printer: Object to print messages on the console.
    :param actions:         Actions available to the user.
    :return:                Return choice of action of user.
    """
    while True:
        console_printer.print(format_lines("*0: " +
                                           "Do nothing"))
        for i, action in enumerate(actions, 1):
            console_printer.print(format_lines("{:>2}: {}".format(
                i,
                action.desc)))

        try:
            line = format_lines("Enter number (Ctrl-D to exit): ")

            choice = input(line)
            if not choice:
                return 0
            choice = int(choice)
            if 0 <= choice <= len(actions):
                return choice
        except ValueError:
            pass

        console_printer.print(format_lines("Please enter a valid number."))


def print_actions(console_printer, section, actions, failed_actions):
    """
    Prints the given actions and lets the user choose.

    :param console_printer: Object to print messages on the console.
    :param actions:         A list of FunctionMetadata objects.
    :param failed_actions:  A set of all actions that have failed. A failed
                            action remains in the list until it is
                            successfully executed.
    :return:                A tuple with the name member of the
                            FunctionMetadata object chosen by the user
                            and a Section containing at least all needed
                            values for the action. If the user did
                            choose to do nothing, return (None, None).
    """
    choice = choose_action(console_printer, actions)

    if choice == 0:
        return None, None

    return get_action_info(section, actions[choice - 1], failed_actions)


def ask_for_action_and_apply(log_printer,
                             console_printer,
                             section,
                             metadata_list,
                             action_dict,
                             failed_actions,
                             result,
                             file_diff_dict,
                             file_dict):
    """
    Asks the user for an action and applies it.

    :param log_printer:     Printer responsible for logging the messages.
    :param console_printer: Object to print messages on the console.
    :param section:         Currently active section.
    :param metadata_list:   Contains metadata for all the actions.
    :param action_dict:     Contains the action names as keys and their
                            references as values.
    :param failed_actions:  A set of all actions that have failed. A failed
                            action remains in the list until it is successfully
                            executed.
    :param result:          Result corresponding to the actions.
    :param file_diff_dict:  If it is an action which applies a patch, this
                            contains the diff of the patch to be applied to
                            the file with filename as keys.
    :param file_dict:       Dictionary with filename as keys and its contents
                            as values.
    :return:                Returns a boolean value. True will be returned, if
                            it makes sense that the user may choose to execute
                            another action, False otherwise.
    """
    action_name, section = print_actions(console_printer, section,
                                         metadata_list, failed_actions)
    if action_name is None:
        return False

    chosen_action = action_dict[action_name]
    try:
        chosen_action.apply_from_section(result,
                                         file_dict,
                                         file_diff_dict,
                                         section)
        console_printer.print(
            format_lines(chosen_action.SUCCESS_MESSAGE),
            color=SUCCESS_COLOR)
        failed_actions.discard(action_name)
    except Exception as exception:  # pylint: disable=broad-except
        log_printer.log_exception("Failed to execute the action "
                                  "{} with error: {}.".format(action_name,
                                                              exception),
                                  exception)
        failed_actions.add(action_name)
    return True


def show_enumeration(console_printer,
                     title,
                     items,
                     indentation,
                     no_items_text):
    """
    This function takes as input an iterable object (preferably a list or
    a dict) and prints it in a stylized format. If the iterable object is
    empty, it prints a specific statement given by the user. An e.g :

    <indentation>Title:
    <indentation> * Item 1
    <indentation> * Item 2

    :param console_printer: Object to print messages on the console.
    :param title:           Title of the text to be printed
    :param items:           The iterable object.
    :param indentation:     Number of spaces to indent every line by.
    :param no_items_text:   Text printed when iterable object is empty.
    """
    if not items:
        console_printer.print(indentation + no_items_text)
    else:
        console_printer.print(indentation + title)
        if isinstance(items, dict):
            for key, value in items.items():
                console_printer.print(indentation + " * " + key + ": " +
                                      value[0])
        else:
            for item in items:
                console_printer.print(indentation + " * " + item)
    console_printer.print()


def show_bear(bear,
              show_description,
              show_params,
              console_printer):
    """
    Displays all information about a bear.

    :param bear:             The bear to be displayed.
    :param show_description: True if the main description should be shown.
    :param show_params:      True if the details should be shown.
    :param console_printer:  Object to print messages on the console.
    """
    console_printer.print(bear.name, color="blue")

    if not show_description and not show_params:
        return

    metadata = bear.get_metadata()

    if show_description:
        console_printer.print(
            "  " + metadata.desc.replace("\n", "\n  "))
        console_printer.print()  # Add a newline

    if show_params:
        show_enumeration(
            console_printer, "Supported languages:",
            bear.LANGUAGES,
            "  ",
            "The bear does not provide information about which languages "
            "it can analyze.")
        show_enumeration(console_printer,
                         "Needed Settings:",
                         metadata.non_optional_params,
                         "  ",
                         "No needed settings.")
        show_enumeration(console_printer,
                         "Optional Settings:",
                         metadata.optional_params,
                         "  ",
                         "No optional settings.")
        show_enumeration(console_printer,
                         "Can detect:",
                         bear.can_detect,
                         "  ",
                         "This bear does not provide information about what "
                         "categories it can detect.")
        show_enumeration(console_printer,
                         "Can fix:",
                         bear.CAN_FIX,
                         "  ",
                         "This bear cannot fix issues or does not provide "
                         "information about what categories it can fix.")


def print_bears(bears,
                show_description,
                show_params,
                console_printer):
    """
    Presents all bears being used in a stylized manner.

    :param bears:            It's a dictionary with bears as keys and list of
                             sections containing those bears as values.
    :param show_description: True if the main description of the bears should
                             be shown.
    :param show_params:      True if the parameters and their description
                             should be shown.
    :param console_printer:  Object to print messages on the console.
    """
    if not bears:
        console_printer.print("No bears to show. Did you forget to install "
                              "the `coala-bears` package? Try `pip3 install "
                              "coala-bears`.")
        return

    for bear, sections in sorted(bears.items(),
                                 key=lambda bear_tuple: bear_tuple[0].name):
        show_bear(bear,
                  show_description,
                  show_params,
                  console_printer)


def show_bears(local_bears,
               global_bears,
               show_description,
               show_params,
               console_printer):
    """
    Extracts all the bears from each enabled section or the sections in the
    targets and passes a dictionary to the show_bears_callback method.

    :param local_bears:      Dictionary of local bears with section names
                             as keys and bear list as values.
    :param global_bears:     Dictionary of global bears with section
                             names as keys and bear list as values.
    :param show_description: True if the main description of the bears should
                             be shown.
    :param show_params:      True if the parameters and their description
                             should be shown.
    :param console_printer:  Object to print messages on the console.
    """
    bears = inverse_dicts(local_bears, global_bears)

    print_bears(bears, show_description, show_params, console_printer)


def show_language_bears_capabilities(language_bears_capabilities,
                                     console_printer):
    """
    Displays what the bears can detect and fix.

    :param language_bears_capabilities:
        Dictionary with languages as keys and their bears' capabilities as
        values. The capabilities are stored in a tuple of two elements where the
        first one represents what the bears can detect, and the second one what
        they can fix.
    :param console_printer:
        Object to print messages on the console.
    """
    if not language_bears_capabilities:
        console_printer.print("There is no bear available for this language")
    else:
        for language, capabilities in language_bears_capabilities.items():
            if capabilities[0]:
                console_printer.print('coala can do the following for ', end='')
                console_printer.print(language.upper(), color="blue")
                console_printer.print("    Can detect only: ", end='')
                console_printer.print(
                    ', '.join(sorted(capabilities[0])), color=CAPABILITY_COLOR)
                if capabilities[1]:
                    console_printer.print("    Can fix        : ", end='')
                    console_printer.print(
                        ', '.join(sorted(capabilities[1])),
                        color=CAPABILITY_COLOR)
            else:
                console_printer.print('coala does not support ', color='red',
                                      end='')
                console_printer.print(language, color='blue')
