try:
    # This import has side effects and is needed to make input() behave nicely
    import readline  # pylint: disable=unused-import
except ImportError:  # pragma: no cover
    pass

from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.results.RESULT_SEVERITY import (
    RESULT_SEVERITY,
    RESULT_SEVERITY_COLORS)
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.misc.i18n import _
from coalib.settings.Setting import Setting
from coalib.results.Result import Result
from coalib.misc.DictUtilities import inverse_dicts
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.result_actions.PrintDebugMessageAction import (
    PrintDebugMessageAction)
from coalib.results.result_actions.ShowPatchAction import ShowPatchAction


STR_GET_VAL_FOR_SETTING = _("Please enter a value for the setting \"{}\" ({}) "
                            "needed by {}: ")
STR_LINE_DOESNT_EXIST = _("The line belonging to the following result "
                          "cannot be printed because it refers to a line "
                          "that doesn't seem to exist in the given file.")
STR_PROJECT_WIDE = _("Project wide:")
FILE_NAME_COLOR = "blue"
FILE_LINES_COLOR = "blue"
CLI_ACTIONS = [OpenEditorAction(),
               ApplyPatchAction(),
               PrintDebugMessageAction(),
               ShowPatchAction()]


def format_line(line, real_nr="", sign="|", mod_nr="", symbol="", ):
    return "|{:>4}{}{:>4}|{:1}{}".format(real_nr,
                                         sign,
                                         mod_nr,
                                         symbol,
                                         line.rstrip("\n"))


def print_section_beginning(console_printer, section):
    """
    Will be called after initialization current_section in
    begin_section()

    :param console_printer: Object to print messages on the console.
    :param section:         The section that will get executed now.
    """
    console_printer.print(_("Executing section {name}...").format(
        name=section.name))


def nothing_done(console_printer):
    """
    Will be called after processing a coafile when nothing had to be done,
    i.e. no section was enabled/targeted.
    """
    console_printer.print(_("No existent section was targeted or enabled. "
                            "Nothing to do."))


def print_lines(console_printer,
                pre_padding,
                file_dict,
                current_line,
                result_line,
                result_file):
    """
    Prints the lines between the current and the result line. If needed
    they will be shortened.

    :param console_printer: Object to print messages on the console.
    :param file_dict      : A dictionary containing all files with filename as
                            key.
    :param current_line   : The current line printed by the console_printer.
    :param result_line    : The line to which the result belongs to.
    :param result_file    : The file to which the result belongs to.
    """
    line_delta = result_line - current_line

    if line_delta > pre_padding:
        print_segregation(console_printer)

        for i in range(max(result_line - pre_padding, 1),
                       result_line + 1):
            console_printer.print(
                format_line(line=file_dict[result_file][i - 1],
                            real_nr=i,
                            mod_nr=i),
                color=FILE_LINES_COLOR)
    else:
        for i in range(1, line_delta + 1):
            console_printer.print(
                format_line(
                    line=file_dict[result_file][current_line + i - 1],
                    real_nr=current_line + i,
                    mod_nr=current_line + i),
                color=FILE_LINES_COLOR)


def print_result(console_printer,
                 log_printer,
                 section,
                 file_diff_dict,
                 result,
                 file_dict):
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
    """
    if not isinstance(result, Result):
        log_printer.warn(_("One of the results can not be printed since it is "
                           "not a valid derivative of the coala result "
                           "class."))
        return

    console_printer.print(format_line("[{sev}] {bear}:".format(
        sev=RESULT_SEVERITY.__str__(result.severity), bear=result.origin)),
        color=RESULT_SEVERITY_COLORS[result.severity])
    console_printer.print(
        *[format_line(line) for line in result.message.split("\n")],
        delimiter="\n")

    actions = []
    for action in CLI_ACTIONS:
        if action.is_applicable(result):
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
    while apply_action(log_printer,
                       console_printer,
                       section,
                       metadata_list,
                       action_dict,
                       result,
                       file_diff_dict,
                       file_dict):
        pass


def print_results_formatted(log_printer,
                            section,
                            result_list,
                            *args):
    format_str = str(section.get(
        "format_str",
        "origin:{origin}:file:{file}:line_nr:{line_nr}:severity:"
        "{severity}:msg:{message}"))
    for result in result_list:
        try:
            print(format_str.format(**result.__dict__))
        except KeyError as exception:
            log_printer.log_exception(
                _("Unable to print the result with the given format string."),
                exception)


def print_results(log_printer,
                  section,
                  result_list,
                  file_dict,
                  file_diff_dict,
                  color=True,
                  pre_padding=3):
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
                           not.
    :param pre_padding:    No of lines of file to print before the result line.
                           Default value is 3.
    """
    if not isinstance(result_list, list):
        raise TypeError("result_list should be of type list")
    if not isinstance(file_dict, dict):
        raise TypeError("file_dict should be of type dict")
    if not isinstance(file_diff_dict, dict):
        raise TypeError("file_diff_dict should be of type dict")

    # We can't use None since we need line 109 be executed if file of first
    # result is None
    console_printer = ConsolePrinter(print_colored=color)
    current_file = False
    current_line = 0

    for result in sorted(result_list):
        if result.file != current_file:
            if result.file in file_dict or result.file is None:
                current_file = result.file
                current_line = 0
                console_printer.print("\n\n{}".format(current_file
                                                      if current_file is not
                                                      None
                                                      else STR_PROJECT_WIDE),
                                      color=FILE_NAME_COLOR)
            else:
                log_printer.warn(_("A result ({}) cannot be printed "
                                   "because it refers to a file that "
                                   "doesn't seem to "
                                   "exist.").format(str(result)))
                continue

        if result.line_nr is not None:
            if current_file is None:
                raise AssertionError("A result with a line_nr should also "
                                     "have a file.")
            if result.line_nr < current_line:  # pragma: no cover
                raise AssertionError("The sorting of the results doesn't "
                                     "work correctly.")
            if len(file_dict[result.file]) < result.line_nr - 1:
                console_printer.print(format_line(line=STR_LINE_DOESNT_EXIST))
            else:
                print_lines(console_printer,
                            pre_padding,
                            file_dict,
                            current_line,
                            result.line_nr,
                            result.file)
                current_line = result.line_nr

        print_result(console_printer,
                     log_printer,
                     section,
                     file_diff_dict,
                     result,
                     file_dict)


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
                        _("One of the given settings ({}) is not properly "
                          "described.").format(str(setting_name)))

        return None

    if len(arr) == 2:
        needed = arr[1]
    else:
        needed = ", ".join(arr[1:-1]) + _(" and ") + arr[-1]

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


def get_action_info(section, action):
    """
    Get all the required Settings for an action. It updates the section with
    the Settings.

    :param section: The section the action corresponds to.
    :param action:  The action to get the info for.
    :return:        Action name and the updated section.
    """
    params = action.non_optional_params

    if section is None:
        raise ValueError("section has to be intializied.")

    for param_name in params:
        if param_name not in section:
            question = format_line(
                _("Please enter a value for the parameter '{}' ({}): ")
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
    console_printer.print(format_line(
        _("The following actions are applicable to this result:")))

    while True:
        console_printer.print(format_line(" 0: " +
                                          _("Apply no further actions.")))
        for i, action in enumerate(actions):
            console_printer.print(format_line("{:>2}: {}".format(i + 1,
                                                                 action.desc)))

        try:
            line = format_line(_("Please enter the number of the action "
                                 "you want to execute. "))
            choice = int(input(line))
            if 0 <= choice <= len(actions):
                return choice
        except ValueError:
            pass

        console_printer.print(format_line(_("Please enter a valid number.")))


def print_actions(console_printer, section, actions):
    """
    Prints the given actions and lets the user choose.

    :param actions: A list of FunctionMetadata objects.
    :return:        A touple with the name member of the FunctionMetadata
                    object chosen by the user and a Section containing at
                    least all needed values for the action. If the user did
                    choose to do nothing, return (None, None).
    """
    choice = choose_action(console_printer, actions)

    if choice == 0:
        return None, None

    return get_action_info(section, actions[choice - 1])


def print_action_failed(log_printer, action_name, exception):
    """
    Prints out the information that the chosen action failed.

    :param log_printer: Printer responsible for logging the messages.
    :param action_name: The name of the action that failed.
    :param exception:   The exception with which it failed.
    """
    log_printer.log_exception("Failed to execute the action {}.".
                              format(action_name), exception)


def apply_action(log_printer,
                 console_printer,
                 section,
                 metadata_list,
                 action_dict,
                 result,
                 file_diff_dict,
                 file_dict):
    """
    Applies the action selected by the user.

    :param log_printer:     Printer responsible for logging the messages.
    :param console_printer: Object to print messages on the console.
    :param section:         Currently active section.
    :param metadata_list:   Contains metadata for all the actions.
    :param action_dict:     Contains the action names as keys and their
                            references as values.
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
    action_name, section = print_actions(console_printer,
                                         section,
                                         metadata_list)
    if action_name is None:
        return False

    chosen_action = action_dict[action_name]
    try:
        chosen_action.apply_from_section(result,
                                         file_dict,
                                         file_diff_dict,
                                         section)
    except Exception as exception:  # pylint: disable=broad-except
        print_action_failed(log_printer, action_name, exception)

    return True


def print_segregation(console_printer):
    console_printer.print(format_line(line="",
                                      real_nr="...",
                                      sign="|",
                                      mod_nr="..."),
                          color=FILE_LINES_COLOR)


def show_enumeration(console_printer, title, items, indentation, no_items_text):
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
    console_printer.print("{bear}:".format(bear=bear.__name__))
    console_printer.print("  " + metadata.desc + "\n")

    show_enumeration(console_printer,
                     _("Used in:"),
                     sections,
                     "  ",
                     _("No sections."))
    show_enumeration(console_printer,
                     _("Needed Settings:"),
                     metadata.non_optional_params,
                     "  ",
                     _("No needed settings."))
    show_enumeration(console_printer,
                     _("Optional Settings:"),
                     metadata.optional_params,
                     "  ",
                     _("No optional settings."))


def print_bears(console_printer, bears):
    """
    Presents all bears being used in a stylized manner.

    :param console_printer: Object to print messages on the console.
    :param bears:           Its a dictionary with bears as keys and list of
                            sections containing those bears as values.
    """
    if not bears:
        console_printer.print(_("No bears to show."))
    else:
        for bear in sorted(bears.keys(),
                           key=lambda bear: bear.__name__):
            show_bear(console_printer,
                      bear,
                      bears[bear],
                      bear.get_metadata())


def show_bears(local_bears, global_bears, console_printer):
    """
    Extracts all the bears from each enabled section or the sections in the
    targets and passes a dictionary to the show_bears_callback method.

    :param local_bears:         Dictionary of local bears with section names
                                as keys and bear list as values.
    :param global_bears:        Dictionary of global bears with section
                                names as keys and bear list as values.
    :param show_bears_callback: The callback that is used to print these
                                bears. It will get one parameter holding
                                bears as key and the list of section names
                                where it's used as values.
    """
    bears = inverse_dicts(local_bears, global_bears)

    print_bears(console_printer, bears)
