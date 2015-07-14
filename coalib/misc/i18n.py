import locale
import os
import gettext
import subprocess
import sys


COALA_DOMAIN = 'coala'


def file_needs_update(source, generated):
    """
    Checks if the generated file is nonexistent or older than the source file
    and to be regenerated.
    """
    if os.path.exists(generated):
        src_mtime = os.stat(source)[8]
        gen_mtime = os.stat(generated)[8]
        return src_mtime > gen_mtime
    else:
        return True


def compile_translations(build_dir="build"):
    translations = []
    trans_install_dir_prefix = os.path.join(sys.prefix, "share", "locale")
    for (path, dummy, filenames) in os.walk("locale"):
        for filename in filter(lambda name: name.endswith(".po"), filenames):
            lang = filename[:-3]
            src = os.path.join(path, filename)
            dest_path = os.path.join(build_dir,
                                     "locale",
                                     lang,
                                     "LC_MESSAGES")
            os.makedirs(dest_path, exist_ok=True)
            dest = os.path.join(dest_path, COALA_DOMAIN + ".mo")
            install_dir = os.path.join(trans_install_dir_prefix,
                                       lang,
                                       "LC_MESSAGES")


            try:
                if file_needs_update(src, dest):
                    subprocess.call(["msgfmt", src, "--output-file", dest])

                translations.append((install_dir, [dest]))
            except:  # pragma: no cover
                print("WARNING: Failed building translation for {}."
                      "Please make sure msgfmt (usually provided"
                      "with the gettext package) are installed"
                      "and in PATH.".format(lang))
    return translations


def _get_locale():  # pragma: no cover
    """
    This function will only be used if environment variables are unavailable.
    Therefore testing it while we cannot reconstruct these conditions does
    not make sense.

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


if (os.getenv('LANGUAGE') is None
    and os.getenv('LC_ALL') is None
    and os.getenv('LC_MESSAGES') is None
    and os.getenv('LANG') is None):  # pragma: no cover
    # This will succeed e.g. for windows, gettext only searches those four
    # environment vars we run coverage on linux so we won't get this covered.
    os.environ['LANG'] = _get_locale()


translation = gettext.translation(COALA_DOMAIN, fallback=True)


def _(original):
    """
    Marks the input string for translation and returns the translated string.
    """
    # According to
    # http://www.gnu.org/software/gettext/manual/gettext.html#MO-Files
    # gettext returns some "system information" for empty strings. We don't
    # want that for our usual translations (e.g. if we translate empty
    # documentation comments or whatever).
    if original == "":
        return original

    return translation.gettext(original)


def N_(original):
    """
    Marks the input string for translation and returns the untranslated string.
    """
    return original
