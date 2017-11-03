import copy
import logging
import platform
import os

from termcolor import colored

try:
    # This import has side effects and is needed to make input() behave nicely
    import readline  # pylint: disable=unused-import
except ImportError:  # pragma: no cover
    pass

from coalib.misc.DictUtilities import inverse_dicts
from coalib.misc.Exceptions import log_exception
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.results.Result import Result
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction
from coalib.results.result_actions.IgnoreResultAction import IgnoreResultAction
from coalib.results.result_actions.DoNothingAction import DoNothingAction
from coalib.results.result_actions.GeneratePatchesAction import (
    GeneratePatchesAction)
from coalib.results.result_actions.ShowAppliedPatchesAction import (
    ShowAppliedPatchesAction)
from coalib.results.result_actions.PrintDebugMessageAction import (
    PrintDebugMessageAction)
from coalib.results.result_actions.PrintMoreInfoAction import (
    PrintMoreInfoAction)
from coalib.results.result_actions.ShowPatchAction import ShowPatchAction
from coalib.results.RESULT_SEVERITY import (
    RESULT_SEVERITY, RESULT_SEVERITY_COLORS)
from coalib.settings.Setting import Setting
from coala_utils.string_processing.Core import join_names

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


class NoColorStyle(Style):
    styles = {
        Token: 'noinherit'
    }


def highlight_text(no_color, text, style, lexer=TextLexer()):
    formatter = TerminalTrueColorFormatter(style=style)
    if no_color:
        formatter = TerminalTrueColorFormatter(style=NoColorStyle)
    return highlight(text, lexer, formatter)[:-1]


STR_GET_VAL_FOR_SETTING = ('Please enter a value for the setting \"{}\" ({}) '
                           'needed by {} for section \"{}\": ')
STR_LINE_DOESNT_EXIST = ('The line belonging to the following result '
                         'cannot be printed because it refers to a line '
                         "that doesn't seem to exist in the given file.")
STR_PROJECT_WIDE = 'Project wide:'
STR_ENTER_NUMBER = 'Enter number (Ctrl-{} to exit): '.format(
    'Z' if platform.system() == 'Windows' else 'D')
FILE_NAME_COLOR = 'blue'
FILE_LINES_COLOR = 'blue'
CAPABILITY_COLOR = 'green'
HIGHLIGHTED_CODE_COLOR = 'red'
SUCCESS_COLOR = 'green'
REQUIRED_SETTINGS_COLOR = 'green'
CLI_ACTIONS = (OpenEditorAction(),
               ApplyPatchAction(),
               PrintDebugMessageAction(),
               PrintMoreInfoAction(),
               ShowPatchAction(),
               IgnoreResultAction(),
               ShowAppliedPatchesAction(),
               GeneratePatchesAction())
DIFF_EXCERPT_MAX_SIZE = 4


def color_letter(console_printer, line):
    x = -1
    y = -1
    letter = ''
    for i, l in enumerate(line, 0):
        if line[i] == '(':
            x = i
        if line[i] == ')':
            y = i
        if l.isupper() and x != -1:
            letter = l
    first_part = line[:x+1]
    second_part = line[y:]

    console_printer.print(first_part, end='')
    console_printer.print(letter, color='blue', end='')
    console_printer.print(second_part)


def format_lines(lines, symbol='', line_nr=''):
    def sym(x): return ']' if x is '[' else x
    return '\n'.join('{}{:>4}{} {}'.format(symbol, line_nr, sym(symbol), line)
                     for line in lines.rstrip('\n').split('\n'))


def print_section_beginning(console_printer, section):
    """
    Will be called after initialization current_section in
    begin_section()

    :param console_printer: Object to print messages on the console.
    :param section:         The section that will get executed now.
    """
    console_printer.print('Executing section {name}...'.format(
        name=section.name))


def nothing_done(log_printer=None):
    """
    Will be called after processing a coafile when nothing had to be done,
    i.e. no section was enabled/targeted.

    :param log_printer: A LogPrinter object.
    """
    logging.warning('No existent section was targeted or enabled. Nothing to '
                    'do.')


def acquire_actions_and_apply(console_printer,
                              section,
                              file_diff_dict,
                              result,
                              file_dict,
                              cli_actions=None,
                              apply_single=False):
    """
    Acquires applicable actions and applies them.

    :param console_printer: Object to print messages on the console.
    :param section:         Name of section to which the result belongs.
    :param file_diff_dict:  Dictionary containing filenames as keys and Diff
                            objects as values.
    :param result:          A derivative of Result.
    :param file_dict:       A dictionary containing all files with filename as
                            key.
    :param apply_single:    The action that should be applied for all results.
                            If it's not selected, has a value of False.
    :param cli_actions:     The list of cli actions available.
    """
    cli_actions = CLI_ACTIONS if cli_actions is None else cli_actions
    failed_actions = set()
    applied_actions = {}
    while True:
        actions = []
        for action in cli_actions:
            if action.is_applicable(result, file_dict, file_diff_dict) is True:
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
        if apply_single:
            ask_for_action_and_apply(console_printer,
                                     section,
                                     metadata_list,
                                     action_dict,
                                     failed_actions,
                                     result,
                                     file_diff_dict,
                                     file_dict,
                                     applied_actions,
                                     apply_single=apply_single)
            break
        elif not ask_for_action_and_apply(console_printer,
                                          section,
                                          metadata_list,
                                          action_dict,
                                          failed_actions,
                                          result,
                                          file_diff_dict,
                                          file_dict,
                                          applied_actions,
                                          apply_single=apply_single):
            break


def print_lines(console_printer,
                file_dict,
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
    no_color = not console_printer.print_colored
    for i in range(sourcerange.start.line, sourcerange.end.line + 1):
        # Print affected file's line number in the sidebar.
        console_printer.print(format_lines(lines='', line_nr=i, symbol='['),
                              color=FILE_LINES_COLOR,
                              end='')

        line = file_dict[sourcerange.file][i - 1].rstrip('\n')
        try:
            lexer = get_lexer_for_filename(sourcerange.file)
        except ClassNotFound:
            lexer = TextLexer()
        lexer.add_filter(VisibleWhitespaceFilter(
            spaces=True, tabs=True,
            tabsize=SpacingHelper.DEFAULT_TAB_WIDTH))
        # highlight() combines lexer and formatter to output a ``str``
        # object.
        printed_chars = 0
        if i == sourcerange.start.line and sourcerange.start.column:
            console_printer.print(highlight_text(
                no_color, line[:sourcerange.start.column - 1],
                BackgroundMessageStyle, lexer), end='')

            printed_chars = sourcerange.start.column - 1

        if i == sourcerange.end.line and sourcerange.end.column:
            console_printer.print(highlight_text(
                no_color, line[printed_chars:sourcerange.end.column - 1],
                BackgroundSourceRangeStyle, lexer), end='')

            console_printer.print(highlight_text(
               no_color, line[sourcerange.end.column - 1:],
               BackgroundSourceRangeStyle, lexer), end='')
            console_printer.print('')
        else:
            console_printer.print(highlight_text(
                no_color, line[printed_chars:], BackgroundMessageStyle, lexer),
                                  end='')
            console_printer.print('')


def print_result(console_printer,
                 section,
                 file_diff_dict,
                 result,
                 file_dict,
                 interactive=True,
                 apply_single=False):
    """
    Prints the result to console.

    :param console_printer: Object to print messages on the console.
    :param section:         Name of section to which the result belongs.
    :param file_diff_dict:  Dictionary containing filenames as keys and Diff
                            objects as values.
    :param result:          A derivative of Result.
    :param file_dict:       A dictionary containing all files with filename as
                            key.
    :param apply_single:    The action that should be applied for all results.
                            If it's not selected, has a value of False.
    :param interactive:     Variable to check whether or not to
                            offer the user actions interactively.
    """
    no_color = not console_printer.print_colored
    if not isinstance(result, Result):
        logging.warning('One of the results can not be printed since it is '
                        'not a valid derivative of the coala result '
                        'class.')
        return

    if hasattr(section, 'name'):
        console_printer.print('**** {bear} [Section: {section} | Severity: '
                              '{severity}] ****'
                              .format(bear=result.origin,
                                      section=section.name,
                                      severity=RESULT_SEVERITY.__str__(
                                          result.severity)),
                              color=RESULT_SEVERITY_COLORS[result.severity])
    else:
        console_printer.print('**** {bear} [Section {section} | Severity '
                              '{severity}] ****'
                              .format(bear=result.origin, section='<empty>',
                                      severity=RESULT_SEVERITY.__str__(
                                          result.severity)),
                              color=RESULT_SEVERITY_COLORS[result.severity])
    lexer = TextLexer()
    result.message = highlight_text(no_color, result.message,
                                    BackgroundMessageStyle, lexer)
    console_printer.print(format_lines(result.message, symbol='!'))

    if interactive:
        cli_actions = CLI_ACTIONS
        show_patch_action = ShowPatchAction()
        if show_patch_action.is_applicable(
                result, file_dict, file_diff_dict) is True:
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
                                  section,
                                  file_diff_dict,
                                  result,
                                  file_dict,
                                  cli_actions,
                                  apply_single=apply_single)


def print_diffs_info(diffs, printer):
    """
    Prints diffs information (number of additions and deletions) to the console.

    :param diffs:    List of Diff objects containing corresponding diff info.
    :param printer:  Object responsible for printing diffs on console.
    """
    for filename, diff in sorted(diffs.items()):
        additions, deletions = diff.stats()
        printer.print(
            format_lines('+{additions} -{deletions} in {file}'.format(
                file=filename,
                additions=additions,
                deletions=deletions), '!'),
            color='green')


def print_results_formatted(log_printer,
                            section,
                            result_list,
                            file_dict,
                            *args):
    """
    Prints results through the format string from the format setting done by
    user.

    :param log_printer:    Printer responsible for logging the messages.
    :param section:        The section to which the results belong.
    :param result_list:    List of Result objects containing the corresponding
                           results.
    """
    default_format = ('id:{id}:origin:{origin}:file:{file}:line:{line}:'
                      'column:{column}:end_line:{end_line}:end_column:'
                      '{end_column}:severity:{severity}:severity_str:'
                      '{severity_str}:message:{message}')
    format_str = str(section.get('format', default_format))

    if format_str == 'True':
        format_str = default_format

    for result in result_list:
        severity_str = RESULT_SEVERITY.__str__(result.severity)
        format_args = vars(result)
        try:
            if len(result.affected_code) == 0:
                format_args['affected_code'] = None
                print(format_str.format(file=None,
                                        line=None,
                                        end_line=None,
                                        column=None,
                                        end_column=None,
                                        severity_str=severity_str,
                                        message=result.message,
                                        **format_args))
                continue

            for range in result.affected_code:
                format_args['affected_code'] = range
                format_args['source_lines'] = range.affected_source(file_dict)
                print(format_str.format(file=range.start.file,
                                        line=range.start.line,
                                        end_line=range.end.line,
                                        column=range.start.column,
                                        end_column=range.end.column,
                                        severity_str=severity_str,
                                        message=result.message,
                                        **format_args))
        except KeyError as exception:
            log_exception(
                'Unable to print the result with the given format string.',
                exception)


def print_bears_formatted(bears, format=None):
    format_str = format or ('name:{name}:can_detect:{can_detect}:'
                            'can_fix:{can_fix}:description:{description}')
    print('\n\n'.join(format_str.format(name=bear.name,
                                        can_detect=bear.CAN_DETECT,
                                        can_fix=bear.CAN_FIX,
                                        description=bear.get_metadata().desc)
                      for bear in bears))


def print_affected_files(console_printer,
                         log_printer,
                         result,
                         file_dict):
    """
    Prints all the affected files and affected lines within them.

    :param console_printer: Object to print messages on the console.
    :param log_printer:     Printer responsible for logging the messages.
    :param result:          The result to print the context for.
    :param file_dict:       A dictionary containing all files with filename as
                            key.
    """
    if len(result.affected_code) == 0:
        console_printer.print('\n' + STR_PROJECT_WIDE,
                              color=FILE_NAME_COLOR)
    else:
        for sourcerange in result.affected_code:
            if (
                    sourcerange.file is not None and
                    sourcerange.file not in file_dict):
                logging.warning('The context for the result ({}) cannot '
                                'be printed because it refers to a file '
                                "that doesn't seem to exist ({})"
                                '.'.format(result, sourcerange.file))
            else:
                print_affected_lines(console_printer,
                                     file_dict,
                                     sourcerange)


def print_results_no_input(log_printer,
                           section,
                           result_list,
                           file_dict,
                           file_diff_dict,
                           console_printer,
                           apply_single=False):
    """
    Prints all non interactive results in a section

    :param log_printer:    Printer responsible for logging the messages.
    :param section:        The section to which the results belong to.
    :param result_list:    List containing the results
    :param file_dict:      A dictionary containing all files with filename as
                           key.
    :param file_diff_dict: A dictionary that contains filenames as keys and
                           diff objects as values.
    :param apply_single:   The action that should be applied for all results.
                           If it's not selected, has a value of False.
    :param console_printer: Object to print messages on the console.
    """
    for result in result_list:

        print_affected_files(console_printer,
                             None,
                             result,
                             file_dict)

        print_result(console_printer,
                     section,
                     file_diff_dict,
                     result,
                     file_dict,
                     interactive=False,
                     apply_single=apply_single)


def print_results(log_printer,
                  section,
                  result_list,
                  file_dict,
                  file_diff_dict,
                  console_printer,
                  apply_single=False):
    """
    Prints all the results in a section.

    :param log_printer:    Printer responsible for logging the messages.
    :param section:        The section to which the results belong to.
    :param result_list:    List containing the results
    :param file_dict:      A dictionary containing all files with filename as
                           key.
    :param file_diff_dict: A dictionary that contains filenames as keys and
                           diff objects as values.
    :param apply_single:   The action that should be applied for all results.
                           If it's not selected, has a value of False.
    :param console_printer: Object to print messages on the console.
    """
    for result in sorted(result_list):

        print_affected_files(console_printer,
                             None,
                             result,
                             file_dict)

        print_result(console_printer,
                     section,
                     file_diff_dict,
                     result,
                     file_dict,
                     apply_single=apply_single)


def print_affected_lines(console_printer, file_dict, sourcerange):
    """
    Prints the lines affected by the bears.

    :param console_printer:    Object to print messages on the console.
    :param file_dict:          A dictionary containing all files with filename
                               as key.
    :param sourcerange:        The SourceRange object referring to the related
                               lines to print.
    """
    console_printer.print('\n' + os.path.relpath(sourcerange.file),
                          color=FILE_NAME_COLOR)

    if sourcerange.start.line is not None:
        if len(file_dict[sourcerange.file]) < sourcerange.end.line:
            console_printer.print(format_lines(lines=STR_LINE_DOESNT_EXIST,
                                               line_nr=sourcerange.end.line,
                                               symbol='!'))
        else:
            print_lines(console_printer,
                        file_dict,
                        sourcerange)


def require_setting(setting_name, arr, section):
    """
    This method is responsible for prompting a user about a missing setting and
    taking its value as input from the user.

    :param setting_name: Name of the setting missing
    :param arr:          A list containing a description in [0] and the name
                         of the bears who need this setting in [1] and
                         following.
    :param section:      The section the action corresponds to.
    """
    needed = join_names(arr[1:])

    # Don't use input, it can't deal with escapes!

    print(colored(STR_GET_VAL_FOR_SETTING.format(setting_name, arr[0], needed,
                                                 section.name),
                  REQUIRED_SETTINGS_COLOR))
    return input()


def acquire_settings(log_printer, settings_names_dict, section):
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


    :param section:
        The section the action corresponds to.
    :return:
        A dictionary with the settings name as key and the given value as
        value.
    """
    if not isinstance(settings_names_dict, dict):
        raise TypeError('The settings_names_dict parameter has to be a '
                        'dictionary.')

    result = {}
    for setting_name, arr in sorted(settings_names_dict.items(),
                                    key=lambda x: (join_names(x[1][1:]), x[0])):
        value = require_setting(setting_name, arr, section)
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
                .format(param_name, params[param_name][0]), symbol='!')
            section.append(Setting(param_name, input(question)))

    return action.name, section


def choose_action(console_printer, actions, apply_single=False):
    """
    Presents the actions available to the user and takes as input the action
    the user wants to choose.

    :param console_printer: Object to print messages on the console.
    :param actions:         Actions available to the user.
    :param apply_single:    The action that should be applied for all results.
                            If it's not selected, has a value of False.
    :return:                Return a tuple of lists, a list with the names of
                            actions that needs to be applied and a list with
                            with the description of the actions.
    """
    actions.insert(0, DoNothingAction().get_metadata())
    actions_desc = []
    actions_name = []
    if apply_single:
        for i, action in enumerate(actions, 0):
            if apply_single == action.desc:
                return ([action.desc], [action.name])
        return (['Do (N)othing'], ['Do (N)othing'])
    else:
        while True:
            for i, action in enumerate(actions, 0):
                output = '{:>2}. {}' if i != 0 else '*{}. {}'
                color_letter(console_printer, format_lines(output.format(
                    i, action.desc), symbol='['))

            line = format_lines(STR_ENTER_NUMBER, symbol='[')

            choice = input(line)
            choice = str(choice)

            for c in choice:
                c = str(c)
                actions_desc_len = len(actions_desc)
                if c.isnumeric():
                    for i, action in enumerate(actions, 0):
                        c = int(c)
                        if i == c:
                            actions_desc.append(action.desc)
                            actions_name.append(action.name)
                            break
                elif c.isalpha():
                    c = c.upper()
                    c = '(' + c + ')'
                    for i, action in enumerate(actions, 1):
                        if c in action.desc:
                            actions_desc.append(action.desc)
                            actions_name.append(action.name)
                            break
                if actions_desc_len == len(actions_desc):
                    console_printer.print(format_lines(
                        'Please enter a valid letter.', symbol='['))

            if not choice:
                actions_desc.append(DoNothingAction().get_metadata().desc)
                actions_name.append(DoNothingAction().get_metadata().name)
            return (actions_desc, actions_name)


def try_to_apply_action(action_name,
                        chosen_action,
                        console_printer,
                        section,
                        metadata_list,
                        action_dict,
                        failed_actions,
                        result,
                        file_diff_dict,
                        file_dict,
                        applied_actions):
    """
    Try to apply the given action.

    :param action_name:     The name of the action.
    :param choose_action:   The action object that will be applied.
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
    :param applied_actions: A dictionary that contains the result, file_dict,
                            file_diff_dict and the section for an action.
    :param file_dict:       Dictionary with filename as keys and its contents
                            as values.
    """
    try:
        chosen_action.apply_from_section(result,
                                         file_dict,
                                         file_diff_dict,
                                         section)
        console_printer.print(
            format_lines(chosen_action.SUCCESS_MESSAGE, symbol='['),
            color=SUCCESS_COLOR)
        applied_actions[action_name] = [copy.copy(result), copy.copy(
            file_dict),
                                    copy.copy(file_diff_dict),
                                    copy.copy(section)]
        result.set_applied_actions(applied_actions)
        failed_actions.discard(action_name)
    except Exception as exception:  # pylint: disable=broad-except
        logging.error('Failed to execute the action {} with error: {}.'
                      .format(action_name, exception))
        failed_actions.add(action_name)


def ask_for_action_and_apply(console_printer,
                             section,
                             metadata_list,
                             action_dict,
                             failed_actions,
                             result,
                             file_diff_dict,
                             file_dict,
                             applied_actions,
                             apply_single=False):
    """
    Asks the user for an action and applies it.

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
    :param apply_single:    The action that should be applied for all results.
                            If it's not selected, has a value of False.
    :param applied_actions: A dictionary that contains the result, file_dict,
                            file_diff_dict and the section for an action.
    :return:                Returns a boolean value. True will be returned, if
                            it makes sense that the user may choose to execute
                            another action, False otherwise.
    """
    actions_desc, actions_name = choose_action(console_printer, metadata_list,
                                               apply_single)

    if apply_single:
        if apply_single == 'Do (N)othing':
            return False
        for index, action_details in enumerate(metadata_list, 1):
            if apply_single == action_details.desc:
                action_name, section = get_action_info(
                    section, metadata_list[index - 1], failed_actions)
                chosen_action = action_dict[action_details.name]
                try_to_apply_action(action_name,
                                    chosen_action,
                                    console_printer,
                                    section,
                                    metadata_list,
                                    action_dict,
                                    failed_actions,
                                    result,
                                    file_diff_dict,
                                    file_dict,
                                    applied_actions)
    else:
        for action_choice, action_choice_name in zip(actions_desc,
                                                     actions_name):
            if action_choice == 'Do (N)othing':
                return False
            chosen_action = action_dict[action_choice_name]
            action_choice_made = action_choice
            for index, action_details in enumerate(metadata_list, 1):
                if action_choice_made in action_details.desc:
                    action_name, section = get_action_info(
                        section, metadata_list[index-1], failed_actions)
                    try_to_apply_action(action_name,
                                        chosen_action,
                                        console_printer,
                                        section,
                                        metadata_list,
                                        action_dict,
                                        failed_actions,
                                        result,
                                        file_diff_dict,
                                        file_dict,
                                        applied_actions)

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
                console_printer.print(indentation + ' * ' + key + ': ' +
                                      value[0])
        else:
            for item in items:
                console_printer.print(indentation + ' * ' + item)
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
    console_printer.print(bear.name, color='blue')

    if not show_description and not show_params:
        return

    metadata = bear.get_metadata()

    if show_description:
        console_printer.print(
            '  ' + metadata.desc.replace('\n', '\n  '))
        console_printer.print()  # Add a newline

    if show_params:
        show_enumeration(
            console_printer, 'Supported languages:',
            bear.LANGUAGES,
            '  ',
            'The bear does not provide information about which languages '
            'it can analyze.')
        show_enumeration(console_printer,
                         'Needed Settings:',
                         metadata.non_optional_params,
                         '  ',
                         'No needed settings.')
        show_enumeration(console_printer,
                         'Optional Settings:',
                         metadata.optional_params,
                         '  ',
                         'No optional settings.')
        show_enumeration(console_printer,
                         'Can detect:',
                         bear.can_detect,
                         '  ',
                         'This bear does not provide information about what '
                         'categories it can detect.')
        show_enumeration(console_printer,
                         'Can fix:',
                         bear.CAN_FIX,
                         '  ',
                         'This bear cannot fix issues or does not provide '
                         'information about what categories it can fix.')
        console_printer.print(
            '  Path:\n' + '   ' + repr(bear.source_location) + '\n')


def print_bears(bears,
                show_description,
                show_params,
                console_printer,
                args=None):
    """
    Presents all bears being used in a stylized manner.

    :param bears:            It's a dictionary with bears as keys and list of
                             sections containing those bears as values.
    :param show_description: True if the main description of the bears should
                             be shown.
    :param show_params:      True if the parameters and their description
                             should be shown.
    :param console_printer:  Object to print messages on the console.
    :param args:             Args passed to coala command.
    """
    if not bears:
        console_printer.print('No bears to show. Did you forget to install '
                              'the `coala-bears` package? Try `pip3 install '
                              'coala-bears`.')
        return

    results = [bear for bear, _ in sorted(bears.items(),
                                          key=lambda bear_tuple:
                                          bear_tuple[0].name.lower())]
    if args and args.json:
        from coalib.output.JSONEncoder import create_json_encoder
        JSONEncoder = create_json_encoder(use_relpath=args.relpath)
        json_output = {'bears': results}
        import json
        json_formatted_output = json.dumps(json_output,
                                           cls=JSONEncoder,
                                           sort_keys=True,
                                           indent=2,
                                           separators=(',', ': '))
        if args.output:
            filename = args.output[0]
            with open(filename, 'w') as fp:
                fp.write(json_formatted_output)
        else:
            print(json_formatted_output)
    elif args and args.format:
        print_bears_formatted(results)
    else:
        for bear in results:
            show_bear(bear,
                      show_description,
                      show_params,
                      console_printer)


def show_bears(local_bears,
               global_bears,
               show_description,
               show_params,
               console_printer,
               args=None):
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
    :param args:             Args passed to coala command.
    """
    bears = inverse_dicts(local_bears, global_bears)

    print_bears(bears, show_description, show_params, console_printer, args)


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
        console_printer.print('There is no bear available for this language')
    else:
        for language, capabilities in language_bears_capabilities.items():
            if capabilities[0]:
                console_printer.print(
                    'coala can do the following for ', end='')
                console_printer.print(language.upper(), color='blue')
                console_printer.print('    Can detect only: ', end='')
                console_printer.print(
                    ', '.join(sorted(capabilities[0])), color=CAPABILITY_COLOR)
                if capabilities[1]:
                    console_printer.print('    Can fix        : ', end='')
                    console_printer.print(
                        ', '.join(sorted(capabilities[1])),
                        color=CAPABILITY_COLOR)
            else:
                console_printer.print('coala does not support ', color='red',
                                      end='')
                console_printer.print(language, color='blue')
