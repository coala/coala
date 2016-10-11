from collections import OrderedDict
from copy import copy
from inspect import getfullargspec, ismethod

from coala_utils.decorators import enforce_signature
from coalib.settings.DocstringMetadata import DocstringMetadata


class FunctionMetadata:
    str_nodesc = "No description given."
    str_optional = "Optional, defaults to '{}'."

    @enforce_signature
    def __init__(self,
                 name: str,
                 desc: str="",
                 retval_desc: str="",
                 non_optional_params: (dict, None)=None,
                 optional_params: (dict, None)=None,
                 omit: (set, tuple, list, frozenset)=frozenset(),
                 deprecated_params: (set, tuple, list, frozenset)=frozenset()):
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
        :param deprecared_params:   A list of params that are deprecated.
        """
        if non_optional_params is None:
            non_optional_params = OrderedDict()
        if optional_params is None:
            optional_params = OrderedDict()

        self.name = name
        self._desc = desc
        self.retval_desc = retval_desc
        self._non_optional_params = non_optional_params
        self._optional_params = optional_params
        self.omit = set(omit)
        self.deprecated_params = set(deprecated_params)

    @property
    def desc(self):
        """
        Returns description of the function.
        """
        return self._desc

    @desc.setter
    @enforce_signature
    def desc(self, new_desc: str):
        """
        Set's the description to the new_desc.
        """
        self._desc = new_desc

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

    def add_deprecated_param(self, original, alias):
        """
        Adds an alias for the original setting. The alias setting will have
        the same metadata as the original one. If the original setting is not
        optional, the alias will default to ``None``.

        :param original:  The name of the original setting.
        :param alias:     The name of the alias for the original.
        :raises KeyError: If the new setting doesn't exist in the metadata.
        """
        self.deprecated_params.add(alias)
        self._optional_params[alias] = (
            self._optional_params[original]
            if original in self._optional_params
            else self._non_optional_params[original] + (None, ))

    def create_params_from_section(self, section):
        """
        Create a params dictionary for this function that holds all values the
        function needs plus optional ones that are available.

        :param section:    The section to retrieve the values from.
        :return:           The params dictionary.
        """
        params = {}

        for param in self.non_optional_params:
            _, annotation = self.non_optional_params[param]
            params[param] = self._get_param(param, section, annotation)

        for param in self.optional_params:
            if param in section:
                _, annotation, _ = self.optional_params[param]
                params[param] = self._get_param(param, section, annotation)

        return params

    @staticmethod
    def _get_param(param, section, annotation):
        if annotation is None:
            annotation = lambda x: x

        try:
            return annotation(section[param])
        except (TypeError, ValueError):
            raise ValueError("Unable to convert parameter {!r} into type "
                             "{}.".format(param, annotation))

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

        doc = func.__doc__ or ""
        doc_comment = DocstringMetadata.from_docstring(doc)

        non_optional_params = OrderedDict()
        optional_params = OrderedDict()

        argspec = getfullargspec(func)
        args = () if argspec.args is None else argspec.args
        defaults = () if argspec.defaults is None else argspec.defaults
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
                    cls.str_optional.format(
                        defaults[i-num_non_defaults]) + ")",
                    argspec.annotations.get(arg, None),
                    defaults[i-num_non_defaults])

        return cls(name=func.__name__,
                   desc=doc_comment.desc,
                   retval_desc=doc_comment.retval_desc,
                   non_optional_params=non_optional_params,
                   optional_params=optional_params,
                   omit=omit)

    def filter_parameters(self, dct):
        """
        Filters the given dict for keys that are declared as parameters inside
        this metadata (either optional or non-optional).

        You can use this function to safely pass parameters from a given
        dictionary:

        >>> def multiply(a, b=2, c=0):
        ...     return a * b + c
        >>> metadata = FunctionMetadata.from_function(multiply)
        >>> args = metadata.filter_parameters({'a': 10, 'b': 20, 'd': 30})

        You can safely pass the arguments to the function now:

        >>> multiply(**args)  # 10 * 20
        200

        :param dct:
            The dict to filter.
        :return:
            A new dict containing the filtered items.
        """
        return {key: dct[key]
                for key in (self.non_optional_params.keys() |
                            self.optional_params.keys())
                if key in dct}

    @classmethod
    def merge(cls, *metadatas):
        """
        Merges signatures of ``FunctionMetadata`` objects.

        Parameter (either optional or non-optional) and non-parameter
        descriptions are merged from left to right, meaning the right hand
        metadata overrides the left hand one.

        >>> def a(x, y):
        ...     '''
        ...     desc of *a*
        ...     :param x: x of a
        ...     :param y: y of a
        ...     :return:  5*x*y
        ...     '''
        ...     return 5 * x * y
        >>> def b(x):
        ...     '''
        ...     desc of *b*
        ...     :param x: x of b
        ...     :return:  100*x
        ...     '''
        ...     return 100 * x
        >>> metadata1 = FunctionMetadata.from_function(a)
        >>> metadata2 = FunctionMetadata.from_function(b)
        >>> merged = FunctionMetadata.merge(metadata1, metadata2)
        >>> merged.name
        "<Merged signature of 'a', 'b'>"
        >>> merged.desc
        'desc of *b*'
        >>> merged.retval_desc
        '100*x'
        >>> merged.non_optional_params['x'][0]
        'x of b'
        >>> merged.non_optional_params['y'][0]
        'y of a'

        :param metadatas:
            The sequence of metadatas to merge.
        :return:
            A ``FunctionMetadata`` object containing the merged signature of
            all given metadatas.
        """
        # Collect the metadatas, as we operate on them more often and we want
        # to support arbitrary sequences.
        metadatas = tuple(metadatas)

        merged_name = ("<Merged signature of " +
                       ", ".join(repr(metadata.name)
                                 for metadata in metadatas) +
                       ">")

        merged_desc = next((m.desc for m in reversed(metadatas) if m.desc), "")
        merged_retval_desc = next(
            (m.retval_desc for m in reversed(metadatas) if m.retval_desc), "")
        merged_non_optional_params = {}
        merged_optional_params = {}

        for metadata in metadatas:
            # Use the fields and not the properties to get also omitted
            # parameters.
            merged_non_optional_params.update(metadata._non_optional_params)
            merged_optional_params.update(metadata._optional_params)

        merged_omit = set.union(*(metadata.omit for metadata in metadatas))
        merged_deprecated_params = set.union(*(
            metadata.deprecated_params for metadata in metadatas))

        return cls(merged_name,
                   merged_desc,
                   merged_retval_desc,
                   merged_non_optional_params,
                   merged_optional_params,
                   merged_omit,
                   merged_deprecated_params)
