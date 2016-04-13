import traceback

from pyprint.Printer import Printer

from coalib.misc.Decorators import enforce_signature
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.settings.FunctionMetadata import FunctionMetadata
from coalib.settings.Section import Section
from coalib.settings.ConfigurationGathering import get_config_directory


class Bear(Printer, LogPrinter):
    """
    A bear contains the actual subroutine that is responsible for checking
    source code for certain specifications. However it can actually do
    whatever it wants with the files it gets. If you are missing some Result
    type, feel free to contact us and/or help us extending the coalib.

    This is the base class for every bear. If you want to write an bear, you
    will probably want to look at the GlobalBear and LocalBear classes that
    inherit from this class. In any case you'll want to overwrite at least the
    run method. You can send debug/warning/error messages through the
    debug(), warn(), err() functions. These will send the
    appropriate messages so that they are outputted. Be aware that if you use
    err(), you are expected to also terminate the bear run-through
    immediately.

    If you need some setup or teardown for your bear, feel free to overwrite
    the set_up() and tear_down() functions. They will be invoked
    before/after every run invocation.

    Settings are available at all times through self.section.
    """

    @enforce_signature
    def __init__(self,
                 section: Section,
                 message_queue,
                 timeout=0):
        """
        Constructs a new bear.

        :param section:       The section object where bear settings are
                              contained.
        :param message_queue: The queue object for messages. Can be ``None``.
        :param timeout:       The time the bear is allowed to run. To set no
                              time limit, use 0.
        :raises TypeError:    Raised when ``message_queue`` is no queue.
        :raises RuntimeError: Raised when bear requirements are not fulfilled.
        """
        Printer.__init__(self)
        LogPrinter.__init__(self, self)

        if message_queue is not None and not hasattr(message_queue, "put"):
            raise TypeError("message_queue has to be a Queue or None.")

        self.section = section
        self.message_queue = message_queue
        self.timeout = timeout

        cp = type(self).check_prerequisites()
        if cp is not True:
            error_string = ("The bear " + type(self).__name__ +
                            " does not fulfill all requirements.")
            if cp is not False:
                error_string += " " + cp

            self.warn(error_string)
            raise RuntimeError(error_string)

    def _print(self, output, **kwargs):
        self.debug(output)

    def log_message(self, log_message, timestamp=None, **kwargs):
        if self.message_queue is not None:
            self.message_queue.put(log_message)

    def run(self, *args, dependency_results=None, **kwargs):
        raise NotImplementedError

    def run_bear_from_section(self, args, kwargs):
        try:
            kwargs.update(
                self.get_metadata().create_params_from_section(self.section))
        except ValueError as err:
            self.warn("The bear {} cannot be executed.".format(
                type(self).__name__), str(err))
            return

        return self.run(*args, **kwargs)

    def execute(self, *args, **kwargs):
        name = type(self).__name__
        try:
            self.debug("Running bear {}...".format(name))
            # If it's already a list it won't change it
            return list(self.run_bear_from_section(args, kwargs) or [])
        except:
            self.warn(
                "Bear {} failed to run. Take a look at debug messages for "
                "further information.".format(name))
            self.debug(
                "The bear {bear} raised an exception. If you are the writer "
                "of this bear, please make sure to catch all exceptions. If "
                "not and this error annoys you, you might want to get in "
                "contact with the writer of this bear.\n\nTraceback "
                "information is provided below:\n\n{traceback}"
                "\n".format(bear=name, traceback=traceback.format_exc()))

    @staticmethod
    def kind():
        """
        :return: The kind of the bear
        """
        raise NotImplementedError

    @classmethod
    def get_metadata(cls):
        """
        :return: Metadata for the run function. However parameters like
                 ``self`` or parameters implicitly used by coala (e.g.
                 filename for local bears) are already removed.
        """
        return FunctionMetadata.from_function(
            cls.run,
            omit={"self", "dependency_results"})

    @classmethod
    def missing_dependencies(cls, lst):
        """
        Checks if the given list contains all dependencies.

        :param lst: A list of all already resolved bear classes (not
                    instances).
        :return:    A list of missing dependencies.
        """
        dep_classes = cls.get_dependencies()

        for item in lst:
            if item in dep_classes:
                dep_classes.remove(item)

        return dep_classes

    @staticmethod
    def get_dependencies():
        """
        Retrieves bear classes that are to be executed before this bear gets
        executed. The results of these bears will then be passed to the
        run method as a dict via the dependency_results argument. The dict
        will have the name of the Bear as key and the list of its results as
        results.

        :return: A list of bear classes.
        """
        return []

    @classmethod
    def get_non_optional_settings(cls):
        """
        This method has to determine which settings are needed by this bear.
        The user will be prompted for needed settings that are not available
        in the settings file so don't include settings where a default value
        would do.

        :return: A dictionary of needed settings as keys and a tuple of help
                 text and annotation as values
        """
        return cls.get_metadata().non_optional_params

    @classmethod
    def check_prerequisites(cls):
        """
        Checks whether needed runtime prerequisites of the bear are satisfied.

        This function gets executed at construction and returns True by
        default.

        Section value requirements shall be checked inside the ``run`` method.

        :return: True if prerequisites are satisfied, else False or a string
                 that serves a more detailed description of what's missing.
        """
        return True

    def get_config_dir(self):
        """
        Gives the directory where the configuration file is

        :return: Directory of the config file
        """
        return get_config_directory(self.section)
