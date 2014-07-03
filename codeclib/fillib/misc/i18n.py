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
import locale
import gettext

APP_NAME = "Codec"
LOCALE_DIR = os.path.join(os.path.curdir, 'i18n')

DEFAULT_LANGUAGES = os.environ.get('LANG', '').split(':')
DEFAULT_LANGUAGES += ['en_US']

languages = []
lc, encoding = locale.getdefaultlocale()
if lc:
    languages.append(lc)

languages += DEFAULT_LANGUAGES

gettext.install(True, localedir=None)

gettext.find(APP_NAME, LOCALE_DIR)

gettext.textdomain(APP_NAME)

gettext.bind_textdomain_codeset(APP_NAME, "UTF-8")

language = gettext.translation(APP_NAME, LOCALE_DIR, languages=languages, fallback=True)