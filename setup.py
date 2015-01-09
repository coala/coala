#! /bin/python3

"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
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
                    'bears.spacing',
                    'coalib',
                    'coalib.bearlib',
                    'coalib.bearlib.abstractions',
                    'coalib.bearlib.spacing',
                    'coalib.bears',
                    'coalib.bears.results',
                    'coalib.collecting',
                    'coalib.misc',
                    'coalib.output',
                    'coalib.parsing',
                    'coalib.processes',
                    'coalib.processes.communication',
                    'coalib.settings',
          ],
          license="GPL v3",
          data_files=data_files
    )
