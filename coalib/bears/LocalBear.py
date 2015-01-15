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
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from coalib.bears.Bear import Bear
from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.settings.FunctionMetadata import FunctionMetadata


class LocalBear(Bear):
    """
    A LocalBear is a Bear that analyzes only one file at once. It therefore can not analyze semantical facts over
    multiple files or so.

    This has the advantage that it can be highly parrallelized. In addition the results from multiple bears for one
    file can be shown together for that file which is better to grasp for the user. coala takes care of all that.

    Examples for LocalBear's could be:
    - A SpaceConsistencyBear that checks every line for trailing whitespaces, tabs, ...
    - A VariableNameBear that checks variable names and constant names for certain conditions
    """

    def __init__(self,
                 section,
                 message_queue,
                 TIMEOUT=0):
        Bear.__init__(self, section, message_queue, TIMEOUT)

    @staticmethod
    def kind():
        return BEAR_KIND.LOCAL

    def run_bear(self, filename, file, *args):
        """
        Handles the given file.

        :param filename: The filename of the file
        :param file: The file contents as string array
        :return: A list of Result
        """
        raise NotImplementedError("This function has to be implemented for a runnable bear.")

    @classmethod
    def get_metadata(cls):
        metadata = FunctionMetadata.from_function(cls.run_bear)
        metadata.non_optional_params.pop("self", None)
        metadata.non_optional_params.pop("filename", None)
        metadata.non_optional_params.pop("file", None)

        return metadata
