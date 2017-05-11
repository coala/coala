import logging
import shlex
import subprocess
from os.path import exists
from os import environ

from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction
from coala_utils.decorators import enforce_signature


"""
Data about all text editors coala knows about. New editors
can just be added here.
For each editor the following info is stored:
{
    <name/comand>: {
        "file_arg_template":
            A string used to generate arguments to open a file.
            Must at least have the placeholder 'filename'
            and can optionally use 'line' and 'column'
            to open the file at the correct position.
            Some editors don't support opening files at
            a certain position if multiple files are
            to be opened, but we try to do so anyway.
        "args":
            General arguments added to the call, e.g. to
            force opening of a new window.
        "gui":
            Boolean. True if this is a gui editor.
            Optional, defaults to False.
    }
}
"""
KNOWN_EDITORS = {
    # non-gui editors
    'vim': {
        'file_arg_template': '{filename} +{line}',
        'gui': False
    },
    'nvim': {
        'file_arg_template': '{filename} +{line}',
        'gui': False
    },
    'nano': {
        'file_arg_template': '+{line},{column} {filename} ',
        'gui': False
    },
    'emacs': {
        'file_arg_template': '+{line}:{column} {filename}',
        'gui': False
    },
    'emacsclient': {
        'file_arg_template': '+{line}:{column} {filename}',
        'gui': False
    },

    # gui editors
    'atom': {
        'file_arg_template': '{filename}:{line}:{column}',
        'args': '--wait',
        'gui': True
    },
    'geany': {
        'file_arg_template': '{filename} -l {line} --column {column}',
        'args': '-s -i',
        'gui': True
    },
    'gedit': {
        'file_arg_template': '{filename} +{line}',
        'args': '-s',
        'gui': True
    },
    'gvim': {
        'file_arg_template': '{filename} +{line}',
        'gui': True
    },
    'kate': {
        'file_arg_template': '{filename} -l {line} -c {column}',
        'args': '--new',
        'gui': True
    },
    'subl': {
        'file_arg_template': '{filename}:{line}:{column}',
        'args': '--wait',
        'gui': True
    },
    'xed': {
        'file_arg_template': '{filename} +{line}',
        'args': '--new-window',
        'gui': True
    },
}


class OpenEditorAction(ResultAction):

    SUCCESS_MESSAGE = 'Changes saved successfully.'

    @staticmethod
    @enforce_signature
    def is_applicable(result: Result, original_file_dict, file_diff_dict):
        """
        For being applicable, the result has to point to a number of files
        that have to exist i.e. have not been previously deleted.
        """

        if not len(result.affected_code) > 0:
            return 'The result is not associated with any source code.'

        filenames = set(src.renamed_file(file_diff_dict)
                        for src in result.affected_code)
        if not all(exists(filename) for filename in filenames):
            return ("The result is associated with source code that doesn't "
                    'seem to exist.')
        return True

    def build_editor_call_args(self, editor, editor_info, filenames):
        """
        Create argument list which will then be used to open an editor for
        the given files at the correct positions, if applicable.

        :param editor:
            The editor to open the file with.
        :param editor_info:
            A dict containing the keys ``args`` and ``file_arg_template``,
            providing additional call arguments and a template to open
            files at a position for this editor.
        :param filenames:
            A dict holding one entry for each file to be opened.
            Keys must be ``filename``, ``line`` and ``column``.
        """
        call_args = [editor]

        # for some editors we define extra arguments
        if 'args' in editor_info:
            call_args += shlex.split(editor_info['args'])

        # add info for each file to be opened
        for file_info in filenames.values():
            file_arg = editor_info['file_arg_template'].format(
                filename=shlex.quote(file_info['filename']),
                line=file_info['line'], column=file_info['column']
            )
            call_args += shlex.split(file_arg)

        return call_args

    def apply(self, result, original_file_dict, file_diff_dict, editor: str):
        """
        Open file(s)

        :param editor: The editor to open the file with.
        """
        try:
            editor_info = KNOWN_EDITORS[editor.strip()]
        except KeyError:
            # If the editor is unknown fall back to just passing
            # the filenames and emit a warning
            logging.warning(
                'The editor "{editor}" is unknown to coala. Files won\'t be'
                ' opened at the correct positions and other quirks might'
                ' occur. Consider opening an issue at'
                ' https://github.com/coala/coala/issues so we'
                ' can add support for this editor.'
                ' Supported editors are: {supported}'.format(
                    editor=editor, supported=', '.join(
                        sorted(KNOWN_EDITORS.keys())
                    )
                )
            )
            editor_info = {
                'file_arg_template': '{filename}',
                'gui': False
            }

        # Use dict to remove duplicates
        filenames = {
            src.file: {
                'filename': src.renamed_file(file_diff_dict),
                'line': src.start.line or 1,
                'column': src.start.column or 1
            }
            for src in result.affected_code
        }

        call_args = self.build_editor_call_args(editor, editor_info, filenames)

        if editor_info.get('gui', True):
            subprocess.call(call_args, stdout=subprocess.PIPE)
        else:
            subprocess.call(call_args)

        for original_name, file_info in filenames.items():
            filename = file_info['filename']
            with open(filename, encoding='utf-8') as file:
                file_diff_dict[original_name] = Diff.from_string_arrays(
                    original_file_dict[original_name], file.readlines(),
                    rename=False if original_name == filename else filename)

        return file_diff_dict

    if 'EDITOR' in environ:
        apply.__defaults__ = (environ['EDITOR'],)
