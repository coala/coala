import inspect
from collections import OrderedDict

from coalib.misc.i18n import _
from coalib.misc.Enum import enum


class DocumentationComment:
    _ParseMode = enum("DESCRIPTION", "PARAM", "RETVAL")

    def __init__(self, desc, param_dict, retval_desc):
        """
        Represents a documentation comment of a python class or function.

        :param desc:        A description as string.
        :param param_dict:  A dictionary containing parameter names as key and
                            their description as value.
        :param retval_desc: A string describing the return value.
        """
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
        lines = _(inspect.cleandoc(docstring)).split("\n")

        parse_mode = cls._ParseMode.DESCRIPTION
        cur_param = ""

        desc = ""
        param_dict = OrderedDict()
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

        return (cls(desc=desc.strip(),
                    param_dict=param_dict,
                    retval_desc=retval_desc.strip()))
