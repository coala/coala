#!/usr/bin/env python3

import datetime
import locale
import os
import platform
import sys
from os import getenv
from subprocess import call

import pip
import setuptools.command.build_py
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

from coalib import assert_supported_version, get_version
from coalib.misc.BuildManPage import BuildManPage

try:
    lc = locale.getlocale()
    pf = platform.system()
    if pf != 'Windows' and lc == (None, None):
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
except (ValueError, UnicodeError, locale.Error):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

VERSION = '0.12.0.dev99999999999999'
DESCRIPTION = (
    'Linting and Fixing Code for All Languages'
)
DEPENDENCY_LINKS = []

KEYWORDS = [
    'code-analysis',
    'lint',
]


# from http://pypi.python.org/pypi?%3Aaction=list_classifiers

CLASSIFIERS = [
    'Development Status :: 4 - Beta',

    'Environment :: Console',
    'Environment :: MacOS X',
    'Environment :: Win32 (MS Windows)',

    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',

    'License :: OSI Approved :: GNU Affero General Public License '
    'v3 or later (AGPLv3+)',
    'Operating System :: OS Independent',

    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3 :: Only',

    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Text Processing :: Linguistic',

]

SETUP_COMMANDS = {}

assert_supported_version()


class BuildPyCommand(setuptools.command.build_py.build_py):

    def run(self):
        if platform.system() != 'Windows':
            self.run_command('build_manpage')
        setuptools.command.build_py.build_py.run(self)


def set_python_path(path):
    if 'PYTHONPATH' in os.environ:
        user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
        user_paths.insert(0, path)
        os.environ['PYTHONPATH'] = os.pathsep.join(user_paths)
    else:
        os.environ['PYTHONPATH'] = path


class PyTestCommand(TestCommand):
    """
    From https://pytest.org/latest/goodpractices.html
    """
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


SETUP_COMMANDS['test'] = PyTestCommand


class BuildDocsCommand(setuptools.command.build_py.build_py):

    def initialize_options(self):
        setup_dir = os.path.join(os.getcwd(), __dir__)
        docs_dir = os.path.join(setup_dir, 'docs')
        source_docs_dir = os.path.join(docs_dir,
                                       './')

        set_python_path(setup_dir)

        self.apidoc_commands = list()

        self.apidoc_commands.append((
            'sphinx-apidoc', '-f', '-o', source_docs_dir,
            '--no-toc',
            os.path.join(setup_dir, 'coalib')
        ))

        self.make_command = (
            'make', '-C',
            docs_dir,
            'html', 'SPHINXOPTS=-W',
        )

        # build_lib & optimize is set to these as a
        # work around for "AttributeError"
        self.build_lib = ''
        self.optimize = 2

    def run(self):
        for command in self.apidoc_commands:
            err_no = call(command)
            if err_no:
                sys.exit(err_no)
        err_no = call(self.make_command)
        sys.exit(err_no)

__dir__ = os.path.dirname(__file__)

SETUP_COMMANDS['docs'] = BuildDocsCommand

# Generate API documentation only if we are running on readthedocs.io
on_rtd = getenv('READTHEDOCS', None) is not None
if on_rtd:
    build = BuildDocsCommand()
    build.initialize_options()
    build.run()
    if 'dev' in '0.12.0.dev99999999999999':
        current_version = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        call(['python3', '.misc/adjust_version_number.py', 'coalib/VERSION',
              '-b {}'.format(current_version)])
        VERSION = get_version()


from distutils.version import LooseVersion  # noqa (late-import)


class PEP440Version(LooseVersion):
    """
    Basic PEP440 version with a few features.

    Uses the same version semantics as LooseVersion,
    with the addition that a ``v`` prefix is allowed
    in the version as required by PEP 440.

    vstring may be a list, tuple or string.

    v_prefix indicates whether output of the version
    should include a v prefix.

    v_prefix is auto-detected by default.
    Set to False to remove if present, or True to add if missing.
    """

    def __init__(self, vstring=None, v_prefix=None):
        self._v_prefix = v_prefix

        if isinstance(vstring, (list, tuple)):
            type_ = type(vstring)
            vstring = '.'.join(str(i) for i in vstring)
        else:
            type_ = list

        vstring = vstring.strip()

        if vstring.startswith('v'):
            vstring = vstring[1:]
            if vstring.startswith('!'):
                raise ValueError('Invalid use of epoch')
            if v_prefix is not False:
                self._v_prefix = True

        # Can not use super(..) on Python 2.7
        LooseVersion.__init__(self, vstring)
        if self._v_prefix:
            self.vstring = 'v' + self.vstring
        if len(self.version) > 1 and self.version[1] == '!':
            self._epoch = self.version[0]
            if not isinstance(self._epoch, int) or len(self.version) < 3:
                raise ValueError('Invalid use of epoch')

        # Normalise to lower case
        self.version = [
            x if isinstance(x, int) else x.lower() for x in self.version
            if x not in ('-', '_')]

        if self.version[-1] != '*' and not isinstance(self.version[-1], int):
            self.version += (0, )

        if type_ is tuple:
            self.version = tuple(self.version)

        self._final = None
        self._previous = None

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, str(self))

    @property
    def is_dev(self):
        return any(part == 'dev' for part in self.version)

    @property
    def has_epoch(self):
        return any(part == '!' for part in self.version)

    @property
    def final(self):
        """
        Provide only the final component of the version.

        A new instance is return if this instance is not final.
        """
        if self.has_epoch:
            raise NotImplementedError

        if self._final is not None:
            return self._final

        for i, part in enumerate(self.version):
            if not isinstance(part, int):
                final = self.version[:i]
                break
        else:
            self._final = self
            return self

        self._final = PEP440Version(final, self._v_prefix)

        return self._final

    @property
    def is_final(self):
        return self.final == self

    @property
    def is_zero(self):
        return all(part == 0 for part in self.version)

    _zero_message = 'version prior to 0.0 can not exist'

    def _estimate_previous(self):
        """
        Return a new version calculated to be the previous version.

        Currently only handles when the current instance is a final version.

        To really get the previous for 1.0.0, we need to consult PyPi,
        git tags, or some other source of all released versions,
        to find the highest patch release in the prior minor release, or
        highest minor releases if there were no patch releases in the
        last minor release, etc.

        As a result, currently this assumes that release x.(x-1).0 exists
        in that instance.
        """
        if self._previous:
            return self._previous

        assert self.is_final, '%r is not final' % self

        if self.is_zero:
            raise ValueError(self._zero_message)

        previous = self._decrement(self.version)
        self._previous = PEP440Version(previous, self._v_prefix)
        return self._previous

    @staticmethod
    def _decrement(version):
        pos = len(version) - 1

        # Look for non-zero int part
        while pos != 0 and not (isinstance(version[pos], int) and version[pos]):
            pos -= 1

        previous = []
        if pos:
            previous = version[:pos]

        previous += (version[pos] - 1, )

        if len(previous) == len(version):
            return previous

        remaining = version[pos + 1:-1]

        previous += tuple(
            0 if isinstance(i, int) else i for i in remaining)

        previous += ('*', )

        return previous


# This is an unfortunately needed comment

def egg_name_to_requirement(name):
    name = name.strip()
    parts = name.split('-')

    # The first part may be v or v0, which would be considered a version
    # if processed in the following loop.
    name_parts = [parts[0]]
    # Pre-releases may contain a '-' and be alpha only, so we must
    # parse from the second part to find the first version-like part.
    for part in parts[1:]:
        version = PEP440Version(part)
        if isinstance(version.version[0], int):
            break
        name_parts.append(part)

    version_parts = parts[len(name_parts):]

    if not version_parts:
        return name

    name = '-'.join(name_parts)

    version = PEP440Version('-'.join(version_parts))

    # Assume that alpha, beta, pre, post & final releases
    # are in PyPi so setuptools can find it.
    if not version.is_dev:
        return name + '==' + str(version)

    # setuptools fails if a version is given with any specifier such as
    # `==`, `=~`, `>`, if the version is not in PyPi.

    # For development releases, which will not usually be PyPi,
    # setuptools will typically fail.

    # So we estimate a previous release that should exist in PyPi,
    # by decrementing the lowest final version part, and use version
    # specifier `>` so that the installed package from VCS will have a
    # version acceptable to the requirement.

    # With major and minor releases, the previous version must be guessed.
    # If the version was `2.1.0`, the previous_version will be literally
    # `2.0.*` as it assumes that a prior minor release occurred and used
    # the same versioning convention.
    previous_version = version.final._estimate_previous()

    if previous_version.is_zero:
        raise ValueError(
            'Version %s could not be decremented' % version)

    return name + '>' + str(previous_version)


def read_requirements(filename):
    """
    Parse a requirements file.

    Accepts vcs+ links, and places the URL into
    `DEPENDENCY_LINKS`.

    :return: list of str for each package
    """
    data = []
    filename = os.path.join(__dir__, filename)
    with open(filename) as requirements:
        required = requirements.read().splitlines()
        for line in required:
            if not line or line.startswith('#'):
                continue

            if '+' in line[:4]:
                repo_link, egg_name = line.split('#egg=')
                if not egg_name:
                    raise ValueError('Unknown requirement: {0}'
                                     .format(line))

                DEPENDENCY_LINKS.append(line)

                line = egg_name_to_requirement(egg_name)

            data.append(line)

    return data


required = read_requirements('requirements.txt')

test_required = read_requirements('test-requirements.txt')

filename = os.path.join(__dir__, 'README.rst')
with open(filename) as readme:
    long_description = readme.read()

extras_require = None
EXTRAS_REQUIRE = {}
data_files = None
if __name__ == '__main__':
    if platform.system() != 'Windows':
        data_files = [('man/man1', ['coala.1'])]
    else:
        data_files = None

if extras_require:
    EXTRAS_REQUIRE = extras_require
SETUP_COMMANDS.update({
                    'build_manpage': BuildManPage,
                    'build_py': BuildPyCommand,
})

if __name__ == '__main__':
    pip_version = LooseVersion(pip.__version__)
    if pip_version < LooseVersion('9.0.1'):
        raise RuntimeError('Version of pip is less than 9.0.1. '
                           'Consider upgrading pip to pip~=9.0.1')
    setup(name='coala',
          version=VERSION,
          description=DESCRIPTION,
          author='The coala developers',
          author_email='coala.analyzer@gmail.com',
          maintainer='Lasse Schuirmann, Fabian Neuschmidt, Mischa Kr\xfcger'
                     if not on_rtd else 'L.S., F.N., M.K.',
          maintainer_email=('lasse.schuirmann@gmail.com, '
                            'fabian@neuschmidt.de, '
                            'makman@alice.de'),
          url='http://coala.io/',
          platforms='any',
          packages=find_packages(exclude=('build.*', 'tests', 'tests.*')),
          install_requires=required,
          extras_require=EXTRAS_REQUIRE,
          tests_require=test_required,
          dependency_links=DEPENDENCY_LINKS,
          package_data={'coalib': ['system_coafile', 'VERSION',
                                   'bearlib/languages/documentation/*.coalang']
                        },
          license='AGPL-3.0',
          keywords=KEYWORDS,
          data_files=data_files,
          long_description=long_description,
          entry_points={
              'console_scripts': [
                  'coala = coalib.coala:main',
                  'coala-ci = coalib.coala_ci:main',
                  'coala-json = coalib.coala_json:main',
                  'coala-format = coalib.coala_format:main',
                  'coala-delete-orig = coalib.coala_delete_orig:main',
              ],
          },
          classifiers=CLASSIFIERS,
          cmdclass=SETUP_COMMANDS,
          )
