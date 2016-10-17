import traceback
from functools import partial
from os import makedirs
from os.path import join, abspath, exists
from shutil import copyfileobj
from urllib.request import urlopen

from appdirs import user_data_dir

from pyprint.Printer import Printer

from coala_utils.decorators import (enforce_signature, classproperty,
                                    get_public_members)

from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.output.printers.LogPrinter import LogPrinterMixin
from coalib.results.Result import Result
from coalib.settings.FunctionMetadata import FunctionMetadata
from coalib.settings.Section import Section
from coalib.settings.ConfigurationGathering import get_config_directory


class Bear(Printer, LogPrinterMixin):
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

    To indicate which languages your bear supports, just give it the
    ``LANGUAGES`` value which should be a set of string(s):

    >>> class SomeBear(Bear):
    ...     LANGUAGES = {'C', 'CPP','C#', 'D'}

    To indicate the requirements of the bear, assign ``REQUIREMENTS`` a set
    with instances of ``PackageRequirements``.

    >>> class SomeBear(Bear):
    ...     REQUIREMENTS = {
    ...         PackageRequirement('pip', 'coala_decorators', '0.2.1')}

    If your bear uses requirements from a manager we have a subclass from,
    you can use the subclass, such as ``PipRequirement``, without specifying
    manager:

    >>> class SomeBear(Bear):
    ...     REQUIREMENTS = {PipRequirement('coala_decorators', '0.2.1')}

    To specify multiple requirements using ``pip``, you can use the multiple
    method. This can receive both tuples of strings, in case you want a specific
    version, or a simple string, in case you want the latest version to be
    specified.

    >>> class SomeBear(Bear):
    ...     REQUIREMENTS = PipRequirement.multiple(
    ...         ('colorama', '0.1'), 'coala_decorators')

    To specify additional attributes to your bear, use the following:

    >>> class SomeBear(Bear):
    ...     AUTHORS = {'Jon Snow'}
    ...     AUTHORS_EMAILS = {'jon_snow@gmail.com'}
    ...     MAINTAINERS = {'Catelyn Stark'}
    ...     MAINTAINERS_EMAILS = {'catelyn_stark@gmail.com'}
    ...     LICENSE = 'AGPL-3.0'
    ...     ASCIINEMA_URL = 'https://asciinema.org/a/80761'

    If the maintainers are the same as the authors, they can be omitted:

    >>> class SomeBear(Bear):
    ...     AUTHORS = {'Jon Snow'}
    ...     AUTHORS_EMAILS = {'jon_snow@gmail.com'}
    >>> SomeBear.maintainers
    {'Jon Snow'}
    >>> SomeBear.maintainers_emails
    {'jon_snow@gmail.com'}

    If your bear needs to include local files, then specify it giving strings
    containing relative file paths to the INCLUDE_LOCAL_FILES set:

    >>> class SomeBear(Bear):
    ...     INCLUDE_LOCAL_FILES = {'checkstyle.jar', 'google_checks.xml'}

    To keep track easier of what a bear can do, simply tell it to the CAN_FIX
    and the CAN_DETECT sets. Possible values:

    >>> CAN_DETECT = {'Syntax', 'Formatting', 'Security', 'Complexity', 'Smell',
    ... 'Unused Code', 'Redundancy', 'Variable Misuse', 'Spelling',
    ... 'Memory Leak', 'Documentation', 'Duplication', 'Commented Code',
    ... 'Grammar', 'Missing Import', 'Unreachable Code', 'Undefined Element',
    ... 'Code Simplification'}
    >>> CAN_FIX = {'Syntax', ...}

    Specifying something to CAN_FIX makes it obvious that it can be detected
    too, so it may be omitted:

    >>> class SomeBear(Bear):
    ...     CAN_DETECT = {'Syntax', 'Security'}
    ...     CAN_FIX = {'Redundancy'}
    >>> list(sorted(SomeBear.can_detect))
    ['Redundancy', 'Security', 'Syntax']

    Every bear has a data directory which is unique to that particular bear:

    >>> class SomeBear(Bear): pass
    >>> class SomeOtherBear(Bear): pass
    >>> SomeBear.data_dir == SomeOtherBear.data_dir
    False

    BEAR_DEPS contains bear classes that are to be executed before this bear
    gets executed. The results of these bears will then be passed to the
    run method as a dict via the dependency_results argument. The dict
    will have the name of the Bear as key and the list of its results as
    results:

    >>> class SomeBear(Bear): pass
    >>> class SomeOtherBear(Bear):
    ...     BEAR_DEPS = {SomeBear}
    >>> SomeOtherBear.BEAR_DEPS
    {<class 'coalib.bears.Bear.SomeBear'>}
    """

    LANGUAGES = set()
    REQUIREMENTS = set()
    AUTHORS = set()
    AUTHORS_EMAILS = set()
    MAINTAINERS = set()
    MAINTAINERS_EMAILS = set()
    PLATFORMS = {'any'}
    LICENSE = ''
    INCLUDE_LOCAL_FILES = set()
    CAN_DETECT = set()
    CAN_FIX = set()
    ASCIINEMA_URL = ''
    BEAR_DEPS = set()

    @classproperty
    def name(cls):
        """
        :return: The name of the bear
        """
        return cls.__name__

    @classproperty
    def can_detect(cls):
        """
        :return: A set that contains everything a bear can detect, gathering
                 information from what it can fix too.
        """
        return cls.CAN_DETECT | cls.CAN_FIX

    @classproperty
    def maintainers(cls):
        """
        :return: A set containing ``MAINTAINERS`` if specified, else takes
                 ``AUTHORS`` by default.
        """
        return cls.AUTHORS if cls.MAINTAINERS == set() else cls.MAINTAINERS

    @classproperty
    def maintainers_emails(cls):
        """
        :return: A set containing ``MAINTAINERS_EMAILS`` if specified, else
                 takes ``AUTHORS_EMAILS`` by default.
        """
        return (cls.AUTHORS_EMAILS if cls.MAINTAINERS_EMAILS == set()
                else cls.MAINTAINERS)

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

        if message_queue is not None and not hasattr(message_queue, "put"):
            raise TypeError("message_queue has to be a Queue or None.")

        self.section = section
        self.message_queue = message_queue
        self.timeout = timeout

        self.setup_dependencies()
        cp = type(self).check_prerequisites()
        if cp is not True:
            error_string = ("The bear " + self.name +
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
                self.name), str(err))
            return

        return self.run(*args, **kwargs)

    def execute(self, *args, **kwargs):
        name = self.name
        try:
            self.debug("Running bear {}...".format(name))
            # If it's already a list it won't change it
            result = self.run_bear_from_section(args, kwargs)
            return [] if result is None else list(result)
        except:
            self.warn("Bear {} failed to run. Take a look at debug messages"
                      " (`-V`) for further information.".format(name))
            self.debug(
                "The bear {bear} raised an exception. If you are the author "
                "of this bear, please make sure to catch all exceptions. If "
                "not and this error annoys you, you might want to get in "
                "contact with the author of this bear.\n\nTraceback "
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
    def __json__(cls):
        """
        Override JSON export of ``Bear`` object.
        """
        # json cannot serialize properties, so drop them
        _dict = {key: value for key, value in get_public_members(cls).items()
                 if not isinstance(value, property)}
        metadata = cls.get_metadata()
        non_optional_params = metadata.non_optional_params
        optional_params = metadata.optional_params
        _dict["metadata"] = {
            "desc": metadata.desc,
            "non_optional_params": ({param: non_optional_params[param][0]}
                                    for param in non_optional_params),
            "optional_params": ({param: optional_params[param][0]}
                                for param in optional_params)}
        return _dict

    @classmethod
    def missing_dependencies(cls, lst):
        """
        Checks if the given list contains all dependencies.

        :param lst: A list of all already resolved bear classes (not
                    instances).
        :return:    A set of missing dependencies.
        """
        return set(cls.BEAR_DEPS) - set(lst)

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

    @staticmethod
    def setup_dependencies():
        """
        This is a user defined function that can download and set up
        dependencies (via download_cached_file or arbitrary other means) in an
        OS independent way.
        """

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

    def download_cached_file(self, url, filename):
        """
        Downloads the file if needed and caches it for the next time. If a
        download happens, the user will be informed.

        Take a sane simple bear:

        >>> from queue import Queue
        >>> bear = Bear(Section("a section"), Queue())

        We can now carelessly query for a neat file that doesn't exist yet:

        >>> from os import remove
        >>> if exists(join(bear.data_dir, "a_file")):
        ...     remove(join(bear.data_dir, "a_file"))
        >>> file = bear.download_cached_file("http://gitmate.com/", "a_file")

        If we download it again, it'll be much faster as no download occurs:

        >>> newfile = bear.download_cached_file("http://gitmate.com/", "a_file")
        >>> newfile == file
        True

        :param url:      The URL to download the file from.
        :param filename: The filename it should get, e.g. "test.txt".
        :return:         A full path to the file ready for you to use!
        """
        filename = join(self.data_dir, filename)
        if exists(filename):
            return filename

        self.info("Downloading {filename!r} for bear {bearname} from {url}."
                  .format(filename=filename, bearname=self.name, url=url))

        with urlopen(url) as response, open(filename, 'wb') as out_file:
            copyfileobj(response, out_file)
        return filename

    @classproperty
    def data_dir(cls):
        """
        Returns a directory that may be used by the bear to store stuff. Every
        bear has an own directory dependent on their name.
        """
        data_dir = abspath(join(user_data_dir('coala-bears'), cls.name))

        makedirs(data_dir, exist_ok=True)
        return data_dir

    @property
    def new_result(self):
        """
        Returns a partial for creating a result with this bear already bound.
        """
        return partial(Result.from_values, self)
