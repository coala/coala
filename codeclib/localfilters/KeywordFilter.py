"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from codeclib.fillib.results import LineResult
from codeclib.fillib.util.settings import Settings
from codeclib.fillib import LocalFilter


class KeywordFilter(LocalFilter.LocalFilter):

    def run(self, filename, file):
        results = []
        assert isinstance(self.settings, Settings)

        keywords = self.settings["keywords"].value

        for i in range(len(file)):
            for keyword in keywords:
                if file[i].find(keyword) > 0:
                    msg = "Keyword '" + keyword + "' found."
                    results.append(LineResult.LineResult(filename, "KeywordFilter", msg, i+1, file[i]))
        return results

    @staticmethod
    def get_needed_settings():
        """
        This method has to determine which settings are needed by this filter. The user will be prompted for needed
        settings that are not available in the settings file so don't include settings where a default value would do.

        :return: a dictionary of needed settings as keys and help texts as values
        """
        return {"Keywords": "Keywords to raise warnings for in files"}

