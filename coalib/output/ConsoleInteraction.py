try:
    # This import has side effects and is needed to make input() behave nicely
    import readline  # pylint: disable=unused-import
except ImportError:  # pragma: no cover
    pass
import os.path

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.misc.DictUtilities import inverse_dicts
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
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

STR_GET_VAL_FOR_SETTING = ("Please enter a value for the setting \"{}\" ({}) "
                           "needed by {}: ")
STR_LINE_DOESNT_EXIST = ("The line belonging to the following result "
                         "cannot be printed because it refers to a line "
                         "that doesn't seem to exist in the given file.")
STR_PROJECT_WIDE = "Project wide:"
FILE_NAME_COLOR = "blue"
FILE_LINES_COLOR = "blue"
HIGHLIGHTED_CODE_COLOR = 'red'
SUCCESS_COLOR = 'green'
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
    cli_actions = cli_actions or CLI_ACTIONS
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


def print_spaces_tabs_in_unicode(console_printer, line, tab_dict,
                                 color, index=0):
    """
    Prints the lines with tabs and spaces replaced by unicode symbols.

    :param console_printer: The ``Printer`` object to print to.
    :param line:            The line-text to print to ``console_printer``.
    :param tab_dict:        A dictionary containing the indices of tabs inside
                            ``line`` as keys and the tab-length as values.
    :param color:           The color to print the line with (except for spaces
                            and tabs.
    :param index:           The index from where to start the printing.
    """
    for char in line:
        if char == " ":
            try:
                console_printer.print("•", color='cyan', end='')
            except UnicodeEncodeError:
                console_printer.print(".", color='cyan', end='')
        elif char == '\t' and tab_dict:
            tab_count = tab_dict[index]
            console_printer.print(
                '-'*(tab_count-1) + '>', color='cyan', end='')
        else:
            console_printer.print(char, color=color, end='')
        index += 1


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
        console_printer.print(format_lines(lines='', line_nr=i),
                              color=FILE_LINES_COLOR,
                              end='')
        line = file_dict[sourcerange.file][i - 1].rstrip("\n")
        tab_width = int(section.get('tab_width', 4))
        s = SpacingHelper(tab_width)
        tab_dict = dict(s.yield_tab_lengths(line))
        printed_chars = 0
        if i == sourcerange.start.line and sourcerange.start.column:
            print_spaces_tabs_in_unicode(
                console_printer, line[:sourcerange.start.column-1],
                tab_dict, FILE_LINES_COLOR)

            printed_chars = sourcerange.start.column-1

        if i == sourcerange.end.line and sourcerange.end.column:
            print_spaces_tabs_in_unicode(
                console_printer, line[printed_chars:sourcerange.end.column-1],
                tab_dict, HIGHLIGHTED_CODE_COLOR, printed_chars)

            print_spaces_tabs_in_unicode(
                console_printer, line[sourcerange.end.column-1:],
                tab_dict, FILE_LINES_COLOR, sourcerange.end.column)
            console_printer.print("")
        else:
            print_spaces_tabs_in_unicode(
                console_printer, line[printed_chars:], tab_dict,
                HIGHLIGHTED_CODE_COLOR, printed_chars)
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
    console_printer.print(format_lines(result.message), delimiter="\n")

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
    Print all the afected files and affected lines within them.

    :param console_printer: Object to print messages on the console.
    :param log_printer:     Printer responsible for logging the messages.
    :param section:         The section to which the results belong to.
    :param result_list:     List containing the results
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
                                 ".".format(str(result), sourcerange.file))
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
    Print all non interactive results in a section

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
    Print all the results in a section.

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
    console_printer.print("\n" + os.path.relpath(sourcerange.file),
                          color=FILE_NAME_COLOR)

    if sourcerange.start.line is not None:
        if len(file_dict[sourcerange.file]) < sourcerange.end.line:
            console_printer.print(format_lines(lines=STR_LINE_DOESNT_EXIST))
        else:
            print_lines(console_printer,
                        file_dict,
                        section,
                        sourcerange)


def require_setting(log_printer, setting_name, arr):
    """
    This method is responsible for prompting a user about a missing setting and
    taking its value as input from the user.

    :param log_printer:  Printer responsible for logging the messages.
    :param setting_name: Name od the setting missing
    :param arr:          a list containing a description in [0] and the name
                         of the bears who need this setting in [1] and
                         following.
    """
    if not isinstance(arr, list) or len(arr) < 2:
        log_printer.log(LOG_LEVEL.WARNING,
                        "One of the given settings ({}) is not properly "
                        "described.".format(str(setting_name)))

        return None

    if len(arr) == 2:
        needed = arr[1]
    else:
        needed = ", ".join(arr[1:-1]) + " and " + arr[-1]

    return input(STR_GET_VAL_FOR_SETTING.format(str(setting_name),
                                                str(arr[0]),
                                                needed))


def acquire_settings(log_printer, settings_names_dict):
    """
    This method prompts the user for the given settings.

    :param log_printer: Printer responsible for logging the messages.
    :param settings:    a dictionary with the settings name as key and a list
                        containing a description in [0] and the name of the
                        bears who need this setting in [1] and following.

                        Example:

    ::

        {"UseTabs": ["describes whether tabs should be used instead of spaces",
                     "SpaceConsistencyBear",
                     "SomeOtherBear"]}

    :return:            a dictionary with the settings name as key and the
                        given value as value.
    """
    if not isinstance(settings_names_dict, dict):
        raise TypeError("The settings_names_dict parameter has to be a "
                        "dictionary.")

    result = {}
    for setting_name, arr in settings_names_dict.items():
        value = require_setting(log_printer, setting_name, arr)
        if value is not None:
            result[setting_name] = value

    return result


def get_action_info(section, action, failed_actions):
    """
    Get all the required Settings for an action. It updates the section with
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
    console_printer.print(format_lines(
        "The following actions are applicable to this result:"))

    while True:
        console_printer.print(format_lines(" 0: " +
                                           "Apply no further actions."))
        for i, action in enumerate(actions, 1):
            console_printer.print(format_lines("{:>2}: {}".format(
                i,
                action.desc)))

        try:
            line = format_lines("Please enter the number of the action "
                                "you want to execute (Ctrl-D to exit). ")
            choice = int(input(line))
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
    :return:                A touple with the name member of the
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
    :param file_diff_dict:  If its an action which applies a patch, this
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
            format_lines(chosen_action.success_message),
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
    a dict). And prints in a stylized format. If the iterable object is
    empty, it prints a specific statement give by the user. An e.g :

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


def show_bear(console_printer, bear, sections, metadata):
    """
    Display all information about a bear.

    :param console_printer: Object to print messages on the console.
    :param bear:            The bear to be displayed.
    :param sections:        The sections to which the bear belongs.
    :param metadata:        Metadata about the bear.
    """
    console_printer.print("{bear}:".format(bear=bear.name))
    console_printer.print("  " + metadata.desc + "\n")

    show_enumeration(
        console_printer, "Supported languages:",
        bear.supported_languages,
        "  ",
        "The bear does not provide information about which languages "
        "it can analyze.")
    show_enumeration(console_printer,
                     "Used in:",
                     sections,
                     "  ",
                     "No sections.")

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


def print_bears(console_printer, bears, compress):
    """
    Presents all bears being used in a stylized manner.

    :param console_printer: Object to print messages on the console.
    :param bears:           Its a dictionary with bears as keys and list of
                            sections containing those bears as values.
    :param compress:            If set to true, output will be compressed (just
                                show bear names as a list)
    """
    if not bears:
        console_printer.print("No bears to show.")
    elif compress:
        bear_list = sorted(bears.keys(), key=lambda bear: bear.name)
        for bear in bear_list:
            console_printer.print(bear.name)
            console_printer.print("=" * len(bear.name))

            console_printer.print(bear.get_metadata().desc + "\n")
    else:
        for bear in sorted(bears.keys(),
                           key=lambda bear: bear.name):
            show_bear(console_printer,
                      bear,
                      bears[bear],
                      bear.get_metadata())


def show_bears(local_bears, global_bears, compress, console_printer):
    """
    Extracts all the bears from each enabled section or the sections in the
    targets and passes a dictionary to the show_bears_callback method.

    :param local_bears:         Dictionary of local bears with section names
                                as keys and bear list as values.
    :param global_bears:        Dictionary of global bears with section
                                names as keys and bear list as values.
    :param compress:            If set to true, output will be compressed (just
                                show bear names as a list)
    :param show_bears_callback: The callback that is used to print these
                                bears. It will get one parameter holding
                                bears as key and the list of section names
                                where it's used as values.
    """
    bears = inverse_dicts(local_bears, global_bears)

    print_bears(console_printer, bears, compress)
