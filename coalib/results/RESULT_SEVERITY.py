from coalib.misc.Enum import enum

RESULT_SEVERITY = enum("INFO", "NORMAL", "MAJOR")
RESULT_SEVERITY.__str__ = lambda x: RESULT_SEVERITY.reverse.get(x, "NORMAL")
RESULT_SEVERITY_COLORS = {RESULT_SEVERITY.INFO: "green",
                          RESULT_SEVERITY.NORMAL: "yellow",
                          RESULT_SEVERITY.MAJOR: "red"}
