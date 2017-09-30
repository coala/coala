import locale
import platform


try:
    lc = locale.getlocale()
    ps = platform.system()
    if ps != 'Windows' and lc == (None, None):
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
except (ValueError, UnicodeError):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
