from inspect import ismethod, getfullargspec
from collections import OrderedDict
from copy import copy

from coalib.settings.DocumentationComment import DocumentationComment
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.misc.i18n import _


class FunctionMetadata:
    str_nodesc = _("No description given.")
    str_optional = _("Optional, defaults to '{}'.")

    def __init__(self,
                 name,
                 desc="",
                 retval_desc="",
                 non_optional_params=None,
                 optional_params=None,
                 omit=frozenset()):
        """
        Creates the FunctionMetadata object.

        :param name:                The name of the function.
        :param desc:                The description of the function.
        :param retval_desc:         The retval description of the function.
        :param non_optional_params: A dict containing the name of non optional
                                    parameters as the key and a tuple of a
                                    description and the python annotation. To
                                    preserve the order, use OrderedDict.
        :param optional_params:     A dict containing the name of optional
                                    parameters as the key and a tuple
                                    of a description, the python annotation and
                                    the default value. To preserve the order,
                                    use OrderedDict.
        :param omit:                A set of parameters to omit.
        """
        if non_optional_params is None:
            non_optional_params = OrderedDict()
        if optional_params is None:
            optional_params = OrderedDict()

        self.name = name
        self.desc = desc
        self.retval_desc = retval_desc
        self._non_optional_params = non_optional_params
        self._optional_params = optional_params
        self.omit = set(omit)

    def _filter_out_omitted(self, params):
        """
        Filters out parameters that are to omit. This is a helper method for
        the param related properties.

        :param params: The parameter dictionary to filter.
        :return:       The filtered dictionary.
        """
        return OrderedDict(filter(lambda p: p[0] not in self.omit,
                                  tuple(params.items())))

    @property
    def non_optional_params(self):
        """
        Retrieves a dict containing the name of non optional parameters as the
        key and a tuple of a description and the python annotation. Values that
        are present in self.omit will be omitted.
        """
        return self._filter_out_omitted(self._non_optional_params)

    @property
    def optional_params(self):
        """
        Retrieves a dict containing the name of optional parameters as the key
        and a tuple of a description, the python annotation and the default
        value. Values that are present in self.omit will be omitted.
        """
        return self._filter_out_omitted(self._optional_params)

    def create_params_from_section(self,
                                   section,
                                   log_printer=LogPrinter(ConsolePrinter())):
        """
        Create a params dictionary for this function that holds all values the
        function needs plus optional ones that are available.

        :param section: The section to retrieve the values from.
        :return:        A dictionary. Unfold it with ** to pass it to the
                        function.
        """
        # Import Section only as needed to avoid circular dependency
        from coalib.settings.Section import Section

        if not isinstance(section, Section):
            raise TypeError("The 'section' parameter should be a "
                            "coalib.settings.Section instance.")

        params = {}

        for param in self.non_optional_params:
            dummy, annotation = self.non_optional_params[param]
            params[param] = self._get_param(param,
                                            section,
                                            annotation,
                                            log_printer)

        for param in self.optional_params:
            if param in section:
                dummy, annotation, dummy = self.optional_params[param]
                params[param] = self._get_param(param,
                                                section,
                                                annotation,
                                                log_printer)

        return params

    @staticmethod
    def _get_param(param, section, annotation, log_printer):
        if annotation is None:
            annotation = lambda x: x
        try:
            return annotation(section[param])
        except:
            log_printer.warn(_("Unable to convert {param} to the desired "
                               "data type.").format(param=param))
            return section[param]

    @classmethod
    def from_function(cls, func, omit=frozenset()):
        """
        Creates a FunctionMetadata object from a function. Please note that any
        variable argument lists are not supported. If you do not want the
        first (usual named 'self') argument to appear please pass the method of
        an actual INSTANCE of a class; passing the method of the class isn't
        enough. Alternatively you can add "self" to the omit set.

        :param func: The function. If __metadata__ of the unbound function is
                     present it will be copied and used, otherwise it will be
                     generated.
        :param omit: A set of parameter names that are to be ignored.
        :return:     The FunctionMetadata object corresponding to the given
                     function.
        """
        if hasattr(func, "__metadata__"):
            metadata = copy(func.__metadata__)
            metadata.omit = omit
            return metadata

        doc = func.__doc__
        if doc is None:
            doc = ""
        doc_comment = DocumentationComment.from_docstring(doc)

        non_optional_params = OrderedDict()
        optional_params = OrderedDict()

        argspec = getfullargspec(func)
        args = argspec.args if argspec.args is not None else ()
        defaults = argspec.defaults if argspec.defaults is not None else ()
        num_non_defaults = len(args) - len(defaults)
        for i, arg in enumerate(args):
            # Implicit self argument or omitted explicitly
            if i < 1 and ismethod(func):
                continue

            if i < num_non_defaults:
                non_optional_params[arg] = (
                    doc_comment.param_dict.get(arg, cls.str_nodesc),
                    argspec.annotations.get(arg, None))
            else:
                optional_params[arg] = (
                    doc_comment.param_dict.get(arg, cls.str_nodesc) + " (" +
                    cls.str_optional.format(str(defaults[i-num_non_defaults]))
                    + ")",
                    argspec.annotations.get(arg, None),
                    defaults[i-num_non_defaults])

        return cls(name=func.__name__,
                   desc=doc_comment.desc,
                   retval_desc=doc_comment.retval_desc,
                   non_optional_params=non_optional_params,
                   optional_params=optional_params,
                   omit=omit)
