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


import os
import gettext
import builtins


def untranslated(msg):
    return msg

builtins.__dict__['_'] = untranslated
langs = os.environ.get('LANG', '').split(':')
langs += ['en_US']

for lang in langs:
    filename = "i18n/{}.mo".format(lang[0:5])
    try:
        # overwrite our _ definition
        gettext.GNUTranslations(open(filename, "rb")).install()
        break
    except IOError:
        continue
