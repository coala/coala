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


class DocumentationComment:
    class _ParseMode:
        DESCRIPTION = 0
        PARAM = 1
        RETVAL = 2

    def __init__(self, desc, param_dict, retval_desc):
        """
        Represents a documentation comment of a python class or function.
        """
        if not isinstance(desc, str):
            raise TypeError("desc should be a string")
        if not isinstance(param_dict, dict):
            raise TypeError("param_dict should be a dict")
        if not isinstance(retval_desc, str):
            raise TypeError("retval_desc should be a string")

        self.desc = desc
        self.param_dict = param_dict
        self.retval_desc = retval_desc

    @classmethod
    def from_docstring(cls, docstring):
        """
        Parses a python docstring. Usable attributes are:
        :param
        @param
        :return
        @return
        """
        if not isinstance(docstring, str):
            raise TypeError("Parameter docstring has to be a string.")

        lines = docstring.split("\n")

        parse_mode = cls._ParseMode.DESCRIPTION
        cur_param = ""

        desc = ""
        param_dict = {}
        retval_desc = ""
        for line in lines:
            line = line.strip()

            if line == "":
                parse_mode = cls._ParseMode.DESCRIPTION

                continue

            if line.startswith(":param ") or line.startswith("@param "):
                parse_mode = cls._ParseMode.PARAM
                splitted = line[7:].split(":", 1)
                cur_param = splitted[0]
                param_dict[cur_param] = splitted[1].strip()

                continue

            if line.startswith(":return: ") or line.startswith("@return: "):
                parse_mode = cls._ParseMode.RETVAL
                retval_desc = line[9:].strip()

                continue

            if parse_mode == cls._ParseMode.RETVAL:
                retval_desc += " " + line
            elif parse_mode == cls._ParseMode.PARAM:
                param_dict[cur_param] += " " + line
            else:
                desc += " " + line

        return cls(desc=desc.strip(), param_dict=param_dict, retval_desc=retval_desc.strip())
