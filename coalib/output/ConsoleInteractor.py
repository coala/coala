import shutil
try:
    # This import has side effects and is needed to make input() behave nicely
    import readline  # pylint: disable=unused-import
except ImportError: # pragma: no cover
    pass

from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.results.RESULT_SEVERITY import (
    RESULT_SEVERITY,
    RESULT_SEVERITY_COLORS)
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.misc.i18n import _
from coalib.settings.Setting import Setting
from coalib.results.Result import Result


STR_GET_VAL_FOR_SETTING = _("Please enter a value for the setting \"{}\" ({}) "
                            "needed by {}: ")


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


def finalize(file_diff_dict, file_dict):
    """
    To be called after all results are given to the interactor.

    :param file_diff_dict: A dictionary containing filenames as keys and diff
                           objects as values.
    :param file_dict:      A dictionary containing all files with filename as
                           key.
    """
    for filename in file_diff_dict:
        diff = file_diff_dict[filename]
        file_dict[filename] = diff.apply(file_dict[filename])

        # Backup original file, override old backup if needed
        shutil.copy2(filename, filename + ".orig")

        # Write new contents
        with open(filename, mode='w') as file:
            file.writelines(file_dict[filename])


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


class ConsoleInteractor(ConsolePrinter):
    STR_LINE_DOESNT_EXIST = _("The line belonging to the following result "
                              "cannot be printed because it refers to a line "
                              "that doesn't seem to exist in the given file.")
    STR_PROJECT_WIDE = _("Project wide:")
    FILE_NAME_COLOR = "blue"
    FILE_LINES_COLOR = "blue"

    def __init__(self,
                 log_printer,
                 pre_padding: int=3,
                 print_colored=True):
        """
        A ConsoleInteractor uses the Console to interact with the user.

        :param log_printer: The LogPrinter to use for logging.
        :param pre_padding: Number of code lines to show before a result as
                            context.
        """
        ConsolePrinter.__init__(self, print_colored=print_colored)

        self.pre_padding = pre_padding
        self.log_printer = log_printer
        self.file_diff_dict = {}
        self.current_section = None

    def apply_action(self,
                     metadata_list,
                     action_dict,
                     result,
                     file_dict):
        """
        Applies action selected by user specific to a result.

        :param metadata_list: A list of FunctionMetadata objects.
        :param action_dict:   Dictionary containing action names as keys and
                              actions as values.
        :param result:        Result depending on which action is chosen.
        :param file_dict:     A dictionary containing all files with filename
                              as key.
        :return:              True if action is applied successfully.
                              Else False.
        """
        action_name, section = self._print_actions(metadata_list)
        if action_name is None:
            return True

        chosen_action = action_dict[action_name]
        try:
            chosen_action.apply_from_section(result,
                                             file_dict,
                                             self.file_diff_dict,
                                             section)
        except Exception as exception:  # pylint: disable=broad-except
            self._print_action_failed(action_name, exception)
            return False

        return True

    def _print_result(self, result):
        """
        Prints the result.
        """
        self.print(format_line("[{sev}] {bear}:".format(
            sev=RESULT_SEVERITY.__str__(result.severity), bear=result.origin)),
            color=RESULT_SEVERITY_COLORS[result.severity])
        self.print(*[format_line(line) for line in result.message.split("\n")],
                   delimiter="\n")

    def _print_actions(self, actions):
        """
        Prints the given actions and lets the user choose.

        :param actions: A list of FunctionMetadata objects.
        :return:        A touple with the name member of the FunctionMetadata
                        object chosen by the user and a Section containing at
                        least all needed values for the action. If the user did
                        choose to do nothing, return (None, None).
        """
        choice = self._choose_action(actions)

        if choice == 0:
            return None, None

        return get_action_info(self.current_section, actions[choice - 1])

    def _choose_action(self, actions):
        self.print(format_line(
            _("The following options are applicable to this result:")))

        while True:
            self.print(format_line(" 0: " + _("Do nothing.")))
            for i, action in enumerate(actions):
                self.print(format_line("{:>2}: {}".format(i + 1, action.desc)))

            try:
                line = format_line(_("Please enter the number of the action "
                                     "you want to execute. "))
                choice = int(input(line))
                if 0 <= choice <= len(actions):
                    return choice
            except ValueError:
                pass

            self.print(format_line(_("Please enter a valid number.")))

    def _print_action_failed(self, action_name, exception):
        """
        Prints out the information that the chosen action failed.

        :param action_name: The name of the action that failed.
        :param exception:   The exception with which it failed.
        """
        self.log_printer.log_exception("Failed to execute the action "
                                       "{}.".format(action_name),
                                       exception)

    def _print_segregation(self):
        self.print(format_line(line="", real_nr="...", sign="|", mod_nr="..."),
                   color=self.FILE_LINES_COLOR)

    def _print_lines(self, file_dict, current_line, result_line, result_file):
        """
        Prints the lines between the current and the result line. If needed
        they will be shortened.
        """
        line_delta = result_line - current_line

        if line_delta > self.pre_padding:
            self._print_segregation()

            for i in range(max(result_line - self.pre_padding, 1),
                           result_line + 1):
                self.print(
                    format_line(line=file_dict[result_file][i - 1],
                                real_nr=i,
                                mod_nr=i),
                    color=self.FILE_LINES_COLOR)
        else:
            for i in range(1, line_delta + 1):
                self.print(
                    format_line(
                        line=file_dict[result_file][current_line + i - 1],
                        real_nr=current_line + i,
                        mod_nr=current_line + i),
                    color=self.FILE_LINES_COLOR)

    def print_result(self, result, file_dict):
        """
        Prints the result to the console.

        :param result:    A derivative of Result.
        :param file_dict: A dictionary containing all files with filename as
                          key.
        """
        if not isinstance(result, Result):
            self.log_printer.warn(_("One of the results can not be printed "
                                    "since it is not a valid derivative of "
                                    "the coala result class."))
            return

        self._print_result(result)

        actions = result.get_actions()
        if actions == []:
            return

        action_dict = {}
        metadata_list = []
        for action in actions:
            metadata = action.get_metadata()
            action_dict[metadata.name] = action
            metadata_list.append(metadata)

        # User can always choose no action which is guaranteed to succeed
        while not self.apply_action(metadata_list,
                                    action_dict,
                                    result,
                                    file_dict):
            pass

    def print_results(self, result_list, file_dict):
        if not isinstance(result_list, list):
            raise TypeError("result_list should be of type list")
        if not isinstance(file_dict, dict):
            raise TypeError("file_dict should be of type dict")

        # We can't use None since we need line 109 be executed if file of first
        # result is None
        current_file = False
        current_line = 0

        for result in sorted(result_list):
            if result.file != current_file:
                if result.file in file_dict or result.file is None:
                    current_file = result.file
                    current_line = 0
                    self.print("\n\n{}".format(current_file
                                               if current_file is not None
                                               else self.STR_PROJECT_WIDE),
                               color=self.FILE_NAME_COLOR)
                else:
                    self.log_printer.warn(_("A result ({}) cannot be printed "
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
                    self.print(format_line(line=self.STR_LINE_DOESNT_EXIST))
                else:
                    self._print_lines(file_dict,
                                      current_line,
                                      result.line_nr,
                                      result.file)
                    current_line = result.line_nr

            self.print_result(result, file_dict)

    def begin_section(self, section):
        """
        Will be called before the results for a section come in (via
        print_results).

        :param section: The section that will get executed now.
        """
        self.file_diff_dict = {}
        self.current_section = section
        print_section_beginning(self, section)
