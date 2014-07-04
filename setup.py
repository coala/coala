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

from setuptools import setup


setup(name='Codec',
      version='0.1',
      description='Dynamic Code File Checker',
      maintainer='Lasse Schuirmann, Fabian Neuschmidt',
      maintainer_email='lasse.schuirmann@gmail.com, fabian@neuschmidt.de',
      url='www.schuirmann.eu',
      scripts=['codec'],
      packages=['codeclib',

                'codeclib.fillib',
                    'codeclib.fillib.filters',
                    'codeclib.fillib.misc',
                    'codeclib.fillib.results',
                    'codeclib.fillib.settings',

                'codeclib.filters',

                'codeclib.internal',
                    'codeclib.internal.filter_managing',
                    'codeclib.internal.misc',
                    'codeclib.internal.modifying',
                    'codeclib.internal.output',
                    'codeclib.internal.parsing',
                    'codeclib.internal.process_managing',
                ],
      license = "GPL v3"
      )
