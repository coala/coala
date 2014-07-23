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

import os
import gettext
import subprocess
import sys
import builtins


def compile_translations(verbose=True):  # pragma: no cover
    """
    This will be used only for setup.py and we dont have anything to compare the results with. For this reason this
    function is not unit tested.
    """
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
                dest = os.path.join(dest_path, "coala.mo")
                install_dir = os.path.join(trans_install_dir_prefix, lang, "LC_MESSAGES")

                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                else:
                    if os.path.exists(dest):
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
                except:
                    print("WARNING: Failed building translation for {}. "
                          "Please make sure msgfmt is installed and in PATH.".format(lang))
    return translations


def __untranslated(msg):
    return msg

builtins.__dict__['_'] = __untranslated
__langs = os.environ.get('LANG', '').split(':')
__langs += ['en_US']

__language = "en_US"
__mopath = os.path.join(sys.prefix, "share", "locale")
for __lang in __langs:
    __filename = os.path.join(__mopath, __lang[0:5], "LC_MESSAGES", "coala.mo")

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
