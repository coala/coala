#!/usr/bin/env python3

from setuptools import setup

from coalib import assert_supported_version
from coalib.misc.i18n import compile_translations
from coalib.misc.StringConstants import StringConstants
from coalib.misc.BuildManPage import BuildManPage


assert_supported_version()


if __name__ == "__main__":
    authors = "Lasse Schuirmann, Fabian Neuschmidt, Mischa Kr\xfcger"
    author_mails = ('lasse.schuirmann@gmail.com, '
                    'fabian@neuschmidt.de, '
                    'makman@alice.de')
    data_files = compile_translations()

    setup(name='coala',
          version=StringConstants.VERSION,
          description='Code Analysis Application (coala)',
          author=authors,
          author_email=author_mails,
          maintainer=authors,
          maintainer_email=author_mails,
          url='http://coala.rtfd.org/',
          platforms='any',
          packages=['bears',
                    'bears.codeclone_detection',
                    'bears.linters',
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
          install_requires=["setuptools",
                            "munkres3",
                            "coverage",
                            "pylint",
                            "language-check"],
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
                  "coala-dbus = coalib.coala_dbus:main"]},
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

              'Programming Language :: Python :: 3.2',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',

              'Topic :: Scientific/Engineering :: Information Analysis',
              'Topic :: Software Development :: Quality Assurance',
              'Topic :: Text Processing :: Linguistic'],
          cmdclass={'build_manpage': BuildManPage})
