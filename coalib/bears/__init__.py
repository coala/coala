"""
Contains useful stuff for bears all in one file!
"""

# Start ignoring PyImportSortBear
from coalib.bears.Bear import Bear
from coalib.bears.LocalBear import LocalBear
from coalib.bears.GlobalBear import GlobalBear

from coalib.bearlib.abstractions.Linter import linter

from coalib.results.Result import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.results.HiddenResult import HiddenResult
from coalib.results.Diff import Diff
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
# Stop ignoring
