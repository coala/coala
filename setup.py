#!/usr/bin/env python3

from distutils.core import setup
from distutils.sysconfig import get_python_lib
import os

from coalib.misc.i18n import compile_translations


if __name__ == "__main__":
    data_files = compile_translations()

    setup(name='coala',
          version='0.2',
          description='Code Analysis Application (coala)',
          maintainer='Lasse Schuirmann, Fabian Neuschmidt',
          maintainer_email='lasse.schuirmann@gmail.com, fabian@neuschmidt.de',
          url='http://www.coala.schuirmann.net/',
          scripts=['coala'],
          packages=['bears',
                    'bears.misc',
                    'bears.spacing',
                    'coalib',
                    'coalib.bearlib',
                    'coalib.bearlib.abstractions',
                    'coalib.bearlib.parsing',
                    'coalib.bearlib.spacing',
                    'coalib.bears',
                    'coalib.collecting',
                    'coalib.misc',
                    'coalib.output',
                    'coalib.output.printers',
                    'coalib.parsing',
                    'coalib.processes',
                    'coalib.processes.communication',
                    'coalib.results',
                    'coalib.results.result_actions',
                    'coalib.settings'],
          package_data={'coalib': ['default_coafile']},
          license="AGPL v3",
          data_files=data_files
    )
