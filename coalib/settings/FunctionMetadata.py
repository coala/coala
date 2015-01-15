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
from inspect import isfunction, ismethod, getfullargspec
from coalib.settings.DocumentationComment import DocumentationComment
from coalib.misc.i18n import _


class FunctionMetadata:
    str_nodesc = _("No description given.")
    str_optional = _("Optional, defaults to '{}'.")

    def __init__(self, name, desc="", retval_desc="", non_optional_params={}, optional_params={}):
        """
        Creates the FunctionMetadata object.

        :param name: The name of the function.
        :param desc: The description of the function.
        :param retval_desc: The retval description of the function.
        :param non_optional_params: A dict containing the name of non optional parameters as the key and
        a tuple of a description and the python annotation.
        :param optional_params: A dict containing the name of optional parameters as the key and a tuple
        of a description, the python annotation and the default value.
        """
        if not isinstance(name, str):
            raise TypeError("name should be a string")
        if not isinstance(desc, str):
            raise TypeError("desc should be a string")
        if not isinstance(retval_desc, str):
            raise TypeError("retval_desc should be a string")
        if not isinstance(non_optional_params, dict):
            raise TypeError("non_optional_params should be a dict")
        if not isinstance(optional_params, dict):
            raise TypeError("optional_params should be a dict")

        self.name = name
        self.desc = desc
        self.retval_desc = retval_desc
        self.non_optional_params = non_optional_params
        self.optional_params = optional_params

    @classmethod
    def from_function(cls, func):
        """
        Creates a FunctionMetadata object from a function. Please note that any variable argument lists are not
        supported. If you do not want the self argument to appear please pass the method of an actual INSTANCE of a
        class; passing the method of the class isn't enough.

        :param func: The function.
        :return: The FunctionMetadata object corresponding to the given function.
        """
        if not isfunction(func) and not ismethod(func):
            raise TypeError("function has to be a function")

        doc = func.__doc__
        if doc is None:
            doc = ""
        doc_comment = DocumentationComment.from_docstring(doc)

        non_optional_params = {}
        optional_params = {}

        argspec = getfullargspec(func)
        args = argspec.args if argspec.args is not None else ()
        defaults = argspec.defaults if argspec.defaults is not None else ()
        num_non_defaults = len(args) - len(defaults)
        for i, arg in enumerate(args):
            if i < 1 and ismethod(func):  # Implicit self argument
                continue

            if i < num_non_defaults:
                non_optional_params[arg] = (doc_comment.param_dict.get(arg, cls.str_nodesc),
                                            argspec.annotations.get(arg, None))
            else:
                optional_params[arg] = (doc_comment.param_dict.get(arg, cls.str_nodesc) + \
                                        " (" + cls.str_optional.format(str(defaults[i-num_non_defaults])) + ")",
                                        argspec.annotations.get(arg, None),
                                        defaults[i-num_non_defaults])

        return cls(name=func.__name__,
                   desc=doc_comment.desc,
                   retval_desc=doc_comment.retval_desc,
                   non_optional_params=non_optional_params,
                   optional_params=optional_params)
