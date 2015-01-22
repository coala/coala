from coalib.misc.i18n import _


class RESULT_SEVERITY:
    INFO = 0
    NORMAL = 1
    MAJOR = 2

    @staticmethod
    def __str__(severity):
        return {0: _("INFO"),
                1: _("NORMAL"),
                2: _("MAJOR")}.get(severity, _("NORMAL"))
