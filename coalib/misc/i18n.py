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


def _(original):
    """
    Marks the input string for translation and returns the translated string.
    """
    return translation.gettext(original)


def N_(original):
    """
    Marks the input string for translation and returns the untranslated string.
    """
    return original
