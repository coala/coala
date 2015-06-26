#!/usr/bin/env python3

from setuptools import setup

from coalib.misc.i18n import compile_translations
from coalib import version_str


if __name__ == "__main__":
    data_files = compile_translations()

    setup(name='coala',
          version=version_str,
          description='Code Analysis Application (coala)',
          maintainer='Lasse Schuirmann, Fabian Neuschmidt, Mischa Krüger',
          maintainer_email='lasse.schuirmann@gmail.com, '
                           'fabian@neuschmidt.de, '
                           'makman@alice.de',
          url='http://coala.schuirmann.net/',
          packages=['bears',
                    'bears.codeclone_detection',
                    'bears.misc',
                    'bears.spacing',
                    'coalib',
                    'coalib.bearlib',
                    'coalib.bearlib.abstractions',
                    'coalib.bearlib.parsing',
                    'coalib.bearlib.parsing.clang',
                    'coalib.bearlib.spacing',
                    'coalib.bears',
                    'coalib.collecting',
                    'coalib.misc',
                    'coalib.output',
                    'coalib.output.printers',
                    'coalib.output.dbus',
                    'coalib.parsing',
                    'coalib.processes',
                    'coalib.processes.communication',
                    'coalib.results',
                    'coalib.results.result_actions',
                    'coalib.settings'],
          package_data={'coalib': ['default_coafile']},
          license="AGPL v3",
          data_files=data_files,
          long_description="coala is a simple COde AnaLysis Application. Its "
                           "goal is to make static code analysis easy while "
                           "remaining completely modular and therefore "
                           "extendable and language independent. Code analysis"
                           " happens in python scripts while coala manages "
                           "these, tries to provide helpful libraries and "
                           "provides a user interface.",
          entry_points={
              "console_scripts": [
                  "coala = coalib.coala:main",
                  "coala-ci = coalib.coala_ci:main",
                  "coala-dbus = coalib.coala_dbus:main"]})
