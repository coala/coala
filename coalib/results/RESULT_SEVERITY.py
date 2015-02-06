from coalib.misc.Enum import enum
from coalib.misc.i18n import _, N_


RESULT_SEVERITY = enum(N_("INFO"), N_("NORMAL"), N_("MAJOR"))
RESULT_SEVERITY.__str__ = lambda x: _(RESULT_SEVERITY.reverse.get(x, "NORMAL"))
