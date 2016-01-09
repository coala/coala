#!/usr/bin/env python3

from setuptools import setup, find_packages
import setuptools.command.build_py

from coalib import assert_supported_version
assert_supported_version()
from coalib.misc.BuildManPage import BuildManPage
from coalib.output.dbus.BuildDbusService import BuildDbusService
from coalib.misc import Constants


class BuildPyCommand(setuptools.command.build_py.build_py):

    def run(self):
        self.run_command('build_manpage')
        self.run_command('build_dbus')
        setuptools.command.build_py.build_py.run(self)


with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()


if __name__ == "__main__":
    maintainers = "Lasse Schuirmann, Fabian Neuschmidt, Mischa Kr\xfcger"
    maintainer_mails = ('lasse.schuirmann@gmail.com, '
                        'fabian@neuschmidt.de, '
                        'makman@alice.de')
    data_files = [('.', ['coala.1']), ('.', [Constants.BUS_NAME + '.service'])]

    setup(name='coala',
          version=Constants.VERSION,
          description='Code Analysis Application (coala)',
          author="The coala developers",
          maintainer=maintainers,
          maintainer_email=maintainer_mails,
          url='http://coala.rtfd.org/',
          platforms='any',
          packages=find_packages(exclude=["build.*", "*.tests.*", "*.tests"]),
          install_requires=required,
          package_data={'coalib': ['default_coafile', "VERSION"]},
          license="AGPL v3",
          data_files=data_files,
          long_description="coala is a simple COde AnaLysis Application. Its "
                           "goal is to make static code analysis easy while "
                           "remaining completely modular and therefore "
                           "extendable and language independent. Code analysis"
                           " happens in python scripts while coala manages "
                           "these, tries to provide helpful libraries and "
                           "provides a user interface. Please visit "
                           "http://coala.rtfd.org/ for more information or our"
                           "development repository on "
                           "https://github.com/coala-analyzer/coala/.",
          entry_points={
              "console_scripts": [
                  "coala = coalib.coala:main",
                  "coala-ci = coalib.coala_ci:main",
                  "coala-dbus = coalib.coala_dbus:main",
                  "coala-json = coalib.coala_json:main",
                  "coala-format = coalib.coala_format:main"]},
          # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=[
              'Development Status :: 3 - Alpha',

              'Environment :: Console',
              'Environment :: MacOS X',
              'Environment :: Win32 (MS Windows)',
              'Environment :: X11 Applications :: Gnome',

              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',

              'License :: OSI Approved :: GNU Affero General Public License '
              'v3 or later (AGPLv3+)',

              'Operating System :: OS Independent',

              'Programming Language :: Python :: Implementation :: CPython',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3 :: Only',

              'Topic :: Scientific/Engineering :: Information Analysis',
              'Topic :: Software Development :: Quality Assurance',
              'Topic :: Text Processing :: Linguistic'],
          cmdclass={'build_manpage': BuildManPage,
                    'build_dbus': BuildDbusService,
                    'build_py': BuildPyCommand})
