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


setup(name='coala',
      version='0.1',
      description='Code Analysis Application',
      maintainer='Lasse Schuirmann, Fabian Neuschmidt',
      maintainer_email='lasse.schuirmann@gmail.com, fabian@neuschmidt.de',
      url='www.schuirmann.eu',
      scripts=['coala'],
      packages=['coalib',

                'coalib.fillib',
                    'coalib.fillib.filters',
                    'coalib.fillib.misc',
                    'coalib.fillib.results',
                    'coalib.fillib.settings',

                'coalib.filters',

                'coalib.internal',
                    'coalib.internal.filter_managing',
                    'coalib.internal.misc',
                    'coalib.internal.modifying',
                    'coalib.internal.output',
                    'coalib.internal.parsing',
                    'coalib.internal.process_managing',
                ],
      license = "GPL v3"
      )
