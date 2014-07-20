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
import subprocess


def __untranslated(msg):
    return msg

builtins.__dict__['_'] = __untranslated
__langs = os.environ.get('LANG', '').split(':')
__langs += ['en_US']

__language = "en_US"
# FIXME this will not work with installed versions later
for __lang in __langs:
    __pofile = os.path.abspath("locale/{}.po".format(__lang[0:5]))
    __filename = os.path.abspath("locale/{}.mo".format(__lang[0:5]))
    # try generating mo file if possible
    if (not os.path.exists(__filename)) and os.path.exists(__pofile):
        try:
            subprocess.call(["msgfmt", __pofile, "--output-file", __filename])
        except:
            # we can't do anything about this here
            pass

    if os.path.exists(__filename):
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
