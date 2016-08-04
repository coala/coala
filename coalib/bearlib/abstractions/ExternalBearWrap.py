import json
import inspect
from functools import partial
from collections import OrderedDict

from coalib.bears.LocalBear import LocalBear
from coala_utils.decorators import enforce_signature
from coalib.misc.Shell import run_shell_command
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.FunctionMetadata import FunctionMetadata


def _prepare_options(options):
    """
    Checks for illegal options and raises ValueError.

    :param options:
        The options dict that contains user/developer inputs.
    :raises ValueError:
        Raised when illegal options are specified.
    """
    allowed_options = {"executable",
                       "settings"}

    # Check for illegal superfluous options.
    superfluous_options = options.keys() - allowed_options
    if superfluous_options:
        raise ValueError(
            "Invalid keyword arguments provided: " +
            ", ".join(repr(s) for s in sorted(superfluous_options)))

    if not 'settings' in options:
        options['settings'] = {}


def _create_wrapper(klass, options):
    NoDefaultValue = object()

    class ExternalBearWrapBase(LocalBear):

        @staticmethod
        def create_arguments():
            """
            This method has to be implemented by the class that uses
            the decorator in order to create the arguments needed for
            the executable.
            """
            return ()

        @classmethod
        def get_executable(cls):
            """
            Returns the executable of this class.

            :return:
                The executable name.
            """
            return options["executable"]

        @staticmethod
        def _normalize_desc(description, setting_type,
                            default_value=NoDefaultValue):
            """
            Normalizes the description of the parameters only if there
            is none provided.

            :param description:
                The parameter description to be modified in case it is empty.
            :param setting_type:
                The type of the setting. It is needed to create the final
                tuple.
            :param default_value:
                The default value of the setting.
            :return:
                A value for the OrderedDict in the ``FunctionMetadata`` object.
            """
            if description == "":
                description = FunctionMetadata.str_nodesc

            if default_value is NoDefaultValue:
                return (description, setting_type)
            else:
                return (description + " " +
                        FunctionMetadata.str_optional.format(default_value),
                        setting_type, default_value)

        @classmethod
        def get_non_optional_params(cls):
            """
            Fetches the non_optional_params from ``options['settings']``
            and also normalizes their descriptions.

            :return:
                An OrderedDict that is used to create a
                ``FunctionMetadata`` object.
            """
            non_optional_params = {}
            for setting_name, description in options['settings'].items():
                if len(description) == 2:
                    non_optional_params[
                        setting_name] = cls._normalize_desc(description[0],
                                                            description[1])
            return OrderedDict(non_optional_params)

        @classmethod
        def get_optional_params(cls):
            """
            Fetches the optional_params from ``options['settings']``
            and also normalizes their descriptions.

            :return:
                An OrderedDict that is used to create a
                ``FunctionMetadata`` object.
            """
            optional_params = {}
            for setting_name, description in options['settings'].items():
                if len(description) == 3:
                    optional_params[
                        setting_name] = cls._normalize_desc(description[0],
                                                            description[1],
                                                            description[2])
            return OrderedDict(optional_params)

        @classmethod
        def get_metadata(cls):
            metadata = FunctionMetadata(
                'run',
                optional_params=cls.get_optional_params(),
                non_optional_params=cls.get_non_optional_params())
            metadata.desc = inspect.getdoc(cls)
            return metadata

        @classmethod
        def _prepare_settings(cls, settings):
            """
            Adds the optional settings to the settings dict in-place.

            :param settings:
                The settings dict.
            """
            opt_params = cls.get_optional_params()
            for setting_name, description in opt_params.items():
                if setting_name not in settings:
                    settings[setting_name] = description[2]

        def parse_output(self, out, filename):
            """
            Parses the output JSON into Result objects.

            :param out:
                Raw output from the given executable (should be JSON).
            :param filename:
                The filename of the analyzed file. Needed to
                create the Result objects.
            :return:
                An iterator yielding ``Result`` objects.
            """
            output = json.loads(out)

            for result in output['results']:
                affected_code = tuple(
                    SourceRange.from_values(
                        code_range['file'],
                        code_range['start']['line'],
                        code_range['start'].get('column'),
                        code_range.get('end', {}).get('line'),
                        code_range.get('end', {}).get('column'))
                    for code_range in result['affected_code'])
                yield Result(
                    origin=result['origin'],
                    message=result['message'],
                    affected_code=affected_code,
                    severity=result.get('severity', 1),
                    debug_msg=result.get('debug_msg', ""),
                    additional_info=result.get('additional_info', ""))

        def run(self, filename, file, **settings):
            self._prepare_settings(settings)
            json_string = json.dumps({'filename': filename,
                                      'file': file,
                                      'settings': settings})

            args = self.create_arguments()
            try:
                args = tuple(args)
            except TypeError:
                self.err("The given arguments "
                         "{!r} are not iterable.".format(args))
                return

            shell_command = (self.get_executable(),) + args
            out, err = run_shell_command(shell_command, json_string)

            return self.parse_output(out, filename)

    result_klass = type(klass.__name__, (klass, ExternalBearWrapBase), {})
    result_klass.__doc__ = klass.__doc__ or ""
    return result_klass


@enforce_signature
def external_bear_wrap(executable: str, **options):

    options["executable"] = executable
    _prepare_options(options)

    return partial(_create_wrapper, options=options)
