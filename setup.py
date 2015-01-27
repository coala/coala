#! /bin/python3

from distutils.core import setup
from distutils.sysconfig import get_python_lib
import os

from coalib.misc.i18n import compile_translations


if __name__ == "__main__":
    data_files = compile_translations()
    data_files.append((os.path.join(get_python_lib(), "coalib"), ["coalib/default_coafile"]))

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
                    'coalib.settings',
          ],
          license="AGPL v3",
          data_files=data_files
    )
