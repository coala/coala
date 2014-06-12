__author__ = 'fabian'

from codeclib.fillib.results import LineResult
from codeclib.fillib.util.settings import Settings
from codeclib.fillib import LocalFilter
import os

class LineLengthFilter(LocalFilter.LocalFilter):

    def run(self, filename, file):

        assert isinstance(self.settings, Settings)
        results = []
        line_continuations = {
            '.f': '&',  # Fortran
            '.for': '&',  # Fortran
            '.f77': '&',  # Fortran
            '.f90': '&',  # Fortran
            '.f95': '&',  # Fortran
            '.fpp': '&',  # Fortran
            '.sh': '\\',  # Bash / other unix shells
            '.ftd': '\\',  # Falcon
            '.fal': '\\',  # Falcon
            '.fam': '\\',  # Falcon
            '.py': '\\',  # Python
            '.pyc': '\\',  # Python
            '.pyw': '\\',  # Python
            '.pyo': '\\',  # Python
            '.pyd': '\\',  # Python
            '.rb': '\\',  # ruby
            '.rbw': '\\',  # ruby
            '.ps1': '`',  # Windows Power Shell
            '.psd1': '`',  # Windows Power Shell
            '.psm1': '`',  # Windows Power Shell
            '.ps1xml': '`',  # Windows Power Shell
            '.clixml': '`',  # Windows Power Shell
            '.psc1': '`',  # Windows Power Shell
            '.pssc': '`',  # Windows Power Shell
            '.cobra': '_',  # Cobra
            '.vb': '_',  # Visual Basic
            '.m': '...',  # Matlab
            '.tex': '%',  # TeX
            }

        line_cont_char = ''
        for key, value in line_continuations.items():
            if key == os.path.splitext(filename)[1]:
                line_cont_char = line_continuations[key]

        max_line_length = self.settings["maxlinelength"].to_int(0)

        for i in range(len(file)):
            if len(file[i]) > max_line_length:
                msg = "Line length exceeds {} characters".format(max_line_length)
                results.append(LineResult.LineResult(filename, "LineLengthFilter", msg, i+1, file[i], LineLengthFilter.abbreviate(file[i], max_line_length, line_cont_char)))
        return results

    @staticmethod
    def get_needed_settings():
        """
        This method has to determine which settings are needed by this filter. The user will be prompted for needed
        settings that are not available in the settings file so don't include settings where a default value would do.

        :return: a dictionary of needed settings as keys and help texts as values
        """
        return {"MaxLineLength": "Line Length in chars that should not be exceeded"}

    @staticmethod
    def abbreviate(str, max_line_length, line_cont_char = ''):
        if len(str) <= max_line_length:
            return str
        else:
            if line_cont_char:
                assert(max_line_length > 2)
                last_space_index = str.rfind(' ',0,max_line_length-2)
                if last_space_index > 0:
                    str = str[:last_space_index+2-len(line_cont_char)]+line_cont_char+'\n'+LineLengthFilter.abbreviate(str[last_space_index+2-len(line_cont_char):],max_line_length, line_cont_char)
                else:
                    str = str[:max_line_length-1-len(line_cont_char)]+line_cont_char+'\n'+LineLengthFilter.abbreviate(str[max_line_length-1-len(line_cont_char):],max_line_length, line_cont_char)
            else:
                assert(max_line_length > 1)
                last_space_index = str.rfind(' ',0,max_line_length-1)
                if last_space_index > 0:
                    str = str[:last_space_index]+'\n'+LineLengthFilter.abbreviate(str[last_space_index+1:],max_line_length)
                else:
                    str = str[:max_line_length-1]+'\n'+LineLengthFilter.abbreviate(str[max_line_length-1:],max_line_length)
            return str