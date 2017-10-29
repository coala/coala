from collections import defaultdict
from functools import partial
import inspect
import logging
from os import makedirs
from os.path import join, abspath, exists

from appdirs import user_data_dir

from coala_utils.decorators import (enforce_signature, classproperty,
                                    get_public_members)

import requests

from coalib.results.Result import Result
from coalib.settings.ConfigurationGathering import get_config_directory
from coalib.settings.FunctionMetadata import FunctionMetadata
from coalib.settings.Section import Section


class Bear:
    """
    A bear contains the actual subroutine that is responsible for checking
    source code for certain specifications. However, it can actually do
    whatever it wants with the files it gets.

    This is the base class for every bear. If you want to write a bear, you
    will probably want to look at the ``ProjectBear`` and ``FileBear`` classes
    that inherit from this class.

    To indicate which languages your bear supports, just give it the
    ``LANGUAGES`` value which should be a set of string(s):

    >>> class SomeBear(Bear):
    ...     LANGUAGES = {'C', 'CPP', 'C#', 'D'}

    To indicate the requirements of the bear, assign ``REQUIREMENTS`` a set
    with instances of ``PackageRequirements``.

    >>> from dependency_management.requirements.PackageRequirement import (
    ...     PackageRequirement)
    >>> class SomeBear(Bear):
    ...     REQUIREMENTS = {
    ...         PackageRequirement('pip', 'coala_decorators', '0.2.1')}

    If your bear uses requirements from a manager we have a subclass from,
    you can use the subclass, such as ``PipRequirement``, without specifying
    manager:

    >>> from dependency_management.requirements.PipRequirement import (
    ...     PipRequirement)
    >>> class SomeBear(Bear):
    ...     REQUIREMENTS = {PipRequirement('coala_decorators', '0.2.1')}

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

    To keep track easier of what a bear can do, simply tell it to the
    ``CAN_FIX`` and the ``CAN_DETECT`` sets. Possible values are:

    >>> CAN_DETECT = {'Syntax', 'Formatting', 'Security', 'Complexity',
    ... 'Smell', 'Unused Code', 'Redundancy', 'Variable Misuse', 'Spelling',
    ... 'Memory Leak', 'Documentation', 'Duplication', 'Commented Code',
    ... 'Grammar', 'Missing Import', 'Unreachable Code', 'Undefined Element',
    ... 'Code Simplification'}
    >>> CAN_FIX = {'Syntax', ...}

    Specifying something to ``CAN_FIX`` makes it obvious that it can be
    detected too, so it may be omitted:

    >>> class SomeBear(Bear):
    ...     CAN_DETECT = {'Syntax', 'Security'}
    ...     CAN_FIX = {'Redundancy'}
    >>> sorted(SomeBear.can_detect)
    ['Redundancy', 'Security', 'Syntax']

    Every bear has a data directory which is unique to that particular bear:

    >>> class SomeBear(Bear): pass
    >>> class SomeOtherBear(Bear): pass
    >>> SomeBear.data_dir == SomeOtherBear.data_dir
    False

    A bear can be dependent from other bears. ``BEAR_DEPS`` contains bear
    classes that are to be executed before this bear gets executed. The results
    of these bears will then be passed inside ``self.dependency_results`` as a
    dict. The dict will have the name of the bear as key and a list of its
    results as values:

    >>> class SomeBear(Bear): pass
    >>> class SomeOtherBear(Bear):
    ...     BEAR_DEPS = {SomeBear}
    >>> SomeOtherBear.BEAR_DEPS
    {<class 'coalib.core.Bear.SomeBear'>}
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
        :return:
            The name of the bear.
        """
        return cls.__name__

    @classproperty
    def can_detect(cls):
        """
        :return:
            A set that contains everything a bear can detect, including
            information from what it can fix too.
        """
        return cls.CAN_DETECT | cls.CAN_FIX

    @classproperty
    def source_location(cls):
        """
        Returns the directory this bear is inside.

        >>> class SomeBear(Bear): pass
        >>> SomeBear.source_location
        '...Bear.py'
        """
        return inspect.getfile(cls)

    @classproperty
    def maintainers(cls):
        """
        :return:
            A set containing ``MAINTAINERS`` if specified, else takes
            ``AUTHORS`` by default.
        """
        return cls.AUTHORS if cls.MAINTAINERS == set() else cls.MAINTAINERS

    @classproperty
    def maintainers_emails(cls):
        """
        :return:
            A set containing ``MAINTAINERS_EMAILS`` if specified, else takes
            ``AUTHORS_EMAILS`` by default.
        """
        return (cls.AUTHORS_EMAILS
                if cls.MAINTAINERS_EMAILS == set() else
                cls.MAINTAINERS_EMAILS)

    @enforce_signature
    def __init__(self, section: Section, file_dict: dict):
        """
        Constructs a new bear.

        :param section:
            The section object where bear settings are contained.
        :param file_dict:
            The file-dictionary containing a mapping of filenames to the
            according file contents.
        :raises RuntimeError:
            Raised when bear requirements are not fulfilled.
        """
        self.section = section
        self.file_dict = file_dict

        self._dependency_results = defaultdict(list)

        self.setup_dependencies()
        cp = type(self).check_prerequisites()
        if cp is not True:
            error_string = ('The bear ' + self.name +
                            ' does not fulfill all requirements.')
            if cp is not False:
                error_string += ' ' + cp

            raise RuntimeError(error_string)

    @property
    def dependency_results(self):
        """
        Contains all dependency results.

        This variable gets set during bear execution from the core and can be
        used from ``analyze``.

        Modifications to the returned dictionary while the core is running
        leads to undefined behaviour.

        >>> section = Section('my-section')
        >>> file_dict = {'file1.txt': ['']}
        >>> bear = Bear(section, file_dict)
        >>> bear.dependency_results
        defaultdict(<class 'list'>, {})
        >>> dependency_bear = Bear(section, file_dict)
        >>> bear.dependency_results[type(dependency_bear)] += [1, 2]
        >>> bear.dependency_results
        defaultdict(<class 'list'>, {<class 'coalib.core.Bear.Bear'>: [1, 2]})

        :return:
            A dictionary with bear-types as keys and their results received.
        """
        return self._dependency_results

    @classmethod
    def get_metadata(cls):
        """
        :return:
            Metadata for the ``analyze`` function extracted from its signature.
            Excludes parameter ``self``.
        """
        return FunctionMetadata.from_function(
            cls.analyze,
            omit={'self'})

    # FIXME Make this a @classproperty.
    @classmethod
    def get_non_optional_settings(cls):
        """
        This method has to determine which settings are needed by this bear.
        The user will be prompted for needed settings that are not available
        in the settings file so don't include settings where a default value
        would do.

        Note: This function also queries settings from bear dependencies in
        recursive manner. Though circular dependency chains are a challenge to
        achieve, this function would never return on them!

        :return: A dictionary of needed settings as keys and a tuple of help
                 text and annotation as values
        """
        non_optional_settings = {}

        for dependency in cls.BEAR_DEPS:
            non_optional_settings.update(
                dependency.get_non_optional_settings())

        non_optional_settings.update(cls.get_metadata().non_optional_params)

        return non_optional_settings

    @classmethod
    def __json__(cls):
        """
        Override JSON export of ``Bear`` class.
        """
        # Those members get duplicated if they aren't excluded because they
        # exist also as fields.
        excluded_members = {'can_detect', 'maintainers', 'maintainers_emails'}

        # json cannot serialize properties, so drop them
        data = {
            key: value
            for key, value in get_public_members(cls).items()
            if not isinstance(value, property) and key not in excluded_members}

        metadata = cls.get_metadata()
        non_optional_params = metadata.non_optional_params
        optional_params = metadata.optional_params
        data['metadata'] = {
            'desc': metadata.desc,
            'non_optional_params': {param: non_optional_params[param][0]
                                    for param in non_optional_params},
            'optional_params': {param: optional_params[param][0]
                                for param in optional_params}}

        return data

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

        This function gets executed at construction.

        Section value requirements shall be checked inside the ``run`` method.

        >>> from dependency_management.requirements.PipRequirement import (
        ...     PipRequirement)
        >>> class SomeBear(Bear):
        ...     REQUIREMENTS = {PipRequirement('pip')}

        >>> SomeBear.check_prerequisites()
        True

        >>> class SomeOtherBear(Bear):
        ...     REQUIREMENTS = {PipRequirement('really_bad_package')}

        >>> SomeOtherBear.check_prerequisites()
        'Following requirements are not installed: really_bad_package (...)'

        :return: True if prerequisites are satisfied, else False or a string
                 that serves a more detailed description of what's missing.
        """
        not_installed_requirements = [requirement
                                      for requirement in cls.REQUIREMENTS
                                      if not requirement.is_installed()]

        if not_installed_requirements:
            return 'Following requirements are not installed: ' + ', '.join(
                '{} (installable via `{}`)'.format(
                    requirement.package,
                    ' '.join(requirement.install_command()))
                for requirement in not_installed_requirements)
        else:
            return True

    def get_config_dir(self):
        """
        Gives the directory where the configuration file resides.

        :return:
            Directory of the config file.
        """
        return get_config_directory(self.section)

    @classmethod
    def download_cached_file(cls, url, filename):
        """
        Downloads the file if needed and caches it for the next time. If a
        download happens, the user will be informed.

        Take a sane simple bear:

        >>> section = Section('my-section')
        >>> file_dict = {'file1.txt': ['']}
        >>> bear = Bear(section, file_dict)

        We can now carelessly query for a neat file that doesn't exist yet:

        >>> from os import remove
        >>> if exists(join(bear.data_dir, 'a_file')):
        ...     remove(join(bear.data_dir, 'a_file'))
        >>> file = bear.download_cached_file('https://github.com/', 'a_file')

        If we download it again, it'll be much faster as no download occurs:

        >>> newfile = bear.download_cached_file(
        ...     'https://github.com/', 'a_file')
        >>> newfile == file
        True

        :param url:
            The URL to download the file from.
        :param filename:
            The filename it should get, e.g. "test.txt".
        :return:
            A full path to the file ready for you to use!
        """
        filename = join(cls.data_dir, filename)
        if exists(filename):
            return filename

        logging.info('{}: Downloading {} into {!r}.'
                     .format(cls.name, url, filename))

        response = requests.get(url, stream=True, timeout=20)
        response.raise_for_status()

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(125):
                file.write(chunk)
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

    def execute_task(self, args, kwargs):
        """
        Executes a task.

        By default returns a list of results collected from this bear.

        This function has to return something that is picklable to make bears
        work in multi-process environments.

        :param args:
            The arguments of a task.
        :param kwargs:
            The keyword-arguments of a task.
        :return:
            A list of results from the bear.
        """
        return list(self.analyze(*args, **kwargs))

    def analyze(self, *args, **kwargs):
        """
        Performs the code analysis.

        :return:
            An iterable of results.
        """
        raise NotImplementedError('This function has to be implemented for a '
                                  'runnable bear.')

    def generate_tasks(self):
        """
        This method is responsible for providing the job arguments ``analyze``
        gets called with.

        :return:
            An iterable containing the positional and keyword arguments
            organized in pairs: ``(args-tuple, kwargs-dict)``
        """
        raise NotImplementedError('This function has to be implemented for a '
                                  'runnable bear.')
