from coalib.misc.Enum import enum
from coalib.misc.i18n import N_

LOG_LEVEL = enum(N_("DEBUG"), N_("INFO"), N_("WARNING"), N_("ERROR"))
LOG_LEVEL_COLORS = {LOG_LEVEL.ERROR: "red",
                    LOG_LEVEL.WARNING: "yellow",
                    LOG_LEVEL.INFO: "blue",
                    LOG_LEVEL.DEBUG: "green"}
