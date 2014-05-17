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
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Setuptools are used in case of distutils, because setuptools features a 'test' command.
# Therefore, unittests can now be run by simply calling "python setup.py test".
# Because setuptools is not part of the python standard library, it is included in this package as
# ez_setup.py. It should only be used though, if the library is otherwise unavailable on the system.
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


setup(name='codec',
      version='0.0',
      description='Dynamic Text File Checker',
      maintainer='Fabian Neuschmidt',
      maintainer_email='fabian@neuschmidt.de',
      url='www.test.url',
      scripts=['codec'],
      packages=['codeclib',
                'codeclib.fillib','codeclib.fillib.util',
                'codeclib.globalfilters',
                'codeclib.internal', 'codeclib.internal.util',
                'codeclib.localfilters'],
      test_suite='tests'
      )
