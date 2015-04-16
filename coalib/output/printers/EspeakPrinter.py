import subprocess

from coalib.misc.StringConstants import StringConstants
from coalib.output.printers.Printer import Printer
from coalib.output.ClosableObject import ClosableObject
from coalib.misc.i18n import _


class EspeakPrinter(Printer, ClosableObject):
    def __init__(self):
        """
        Raises EnvironmentError if VoiceOutput is impossible.
        """
        Printer.__init__(self)
        ClosableObject.__init__(self)
        # TODO retrieve language from get_locale and select appropriate voice

        try:
            self.espeak = subprocess.Popen(['espeak'], stdin=subprocess.PIPE)
        except OSError:  # pragma: no cover
            print(_("eSpeak doesn't seem to be installed. You cannot use the "
                    "voice output feature without eSpeak. It can be downloaded"
                    " from http://espeak.sourceforge.net/ or installed via "
                    "your usual package repositories."))
            raise EnvironmentError
        except:  # pragma: no cover
            print(_("Failed to execute eSpeak. An unknown error occurred."),
                  StringConstants.THIS_IS_A_BUG)
            raise EnvironmentError

    def _close(self):
        self.espeak.stdin.close()

    def _print(self, output, **kwargs):
        self.espeak.stdin.write(output.encode())
        self.espeak.stdin.flush()
