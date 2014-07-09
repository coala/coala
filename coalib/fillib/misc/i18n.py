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


def __untranslated(msg):
    return msg

builtins.__dict__['_'] = __untranslated
__langs = os.environ.get('LANG', '').split(':')
__langs += ['en_US']

__language = "en_US"
for __lang in __langs:
    __filename = "i18n/{}.mo".format(__lang[0:5])
    try:
        # overwrite our _ definition
        gettext.GNUTranslations(open(__filename, "rb")).install()
        __language = __lang[0:5]
        break
    except IOError:
        continue

__gettext = builtins.__dict__['_']


def get_locale():
    return __language


def _(s):
    return __gettext(s)
