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

import locale
import os
import gettext
import subprocess
import sys


COALA_DOMAIN = 'coala'


def compile_translations(verbose=True):
    if verbose:
        print("Compiling translations...")
    translations = []
    trans_install_dir_prefix = os.path.join(sys.prefix, "share", "locale")
    for (path, dirnames, filenames) in os.walk("locale"):
        for filename in filenames:
            if filename.endswith(".po"):
                lang = filename[:-3]
                src = os.path.join(path, filename)
                dest_path = os.path.join("build", "locale", lang, "LC_MESSAGES")
                dest = os.path.join(dest_path, COALA_DOMAIN + ".mo")
                install_dir = os.path.join(trans_install_dir_prefix, lang, "LC_MESSAGES")

                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                elif os.path.exists(dest):
                    src_mtime = os.stat(src)[8]
                    dest_mtime = os.stat(dest)[8]
                    if src_mtime <= dest_mtime:
                        translations.append((install_dir, [dest]))
                        continue

                try:
                    if verbose:
                        print("Compiling {}...".format(lang))
                    subprocess.call(["msgfmt", src, "--output-file", dest])
                    translations.append((install_dir, [dest]))
                except:  # pragma: no cover
                    print("WARNING: Failed building translation for {}. "
                          "Please make sure msgfmt is installed and in PATH.".format(lang))
    return translations


def _get_locale():  # pragma: no cover
    """
    This function will only be used if environment variables are unavailable. Therefore testing it while we cannot
    reconstruct these conditions does not make sense.

    :return: The current locale code. (The POSIX way.)
    """
    try:
        language, encoding = locale.getdefaultlocale()
    except ValueError:
        language = None
        encoding = None

    if language is None:
        language = 'C'
    if encoding is None:
        return language
    else:
        return language + '.' + encoding


if os.getenv('LANGUAGE') is None \
   and os.getenv('LC_ALL') is None \
   and os.getenv('LC_MESSAGES') is None \
   and os.getenv('LANG') is None:  # pragma: no cover
    # This will succeed e.g. for windows, gettext only searches those four environment vars
    # we run coverage on linux so we won't get this covered.
    os.environ['LANG'] = _get_locale()


translation = gettext.translation(COALA_DOMAIN, fallback=True)


def _(s):
    return translation.gettext(s)
