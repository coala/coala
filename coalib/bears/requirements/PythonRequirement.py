from coalib.bears.requirements.PackageRequirement import PackageRequirement


class PythonRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``pip``, without using the manager name.
    """

    def __init__(self, package, version=""):
        """
        Constructs a new ``PythonRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = PythonRequirement('setuptools', '19.2')
        >>> pr.manager
        'pip'
        >>> pr.package
        'setuptools'
        >>> pr.version
        '19.2'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'pip', package, version)

    @classmethod
    def multiple(cls, *args):
        """
        Creates a tuple of multiple ``PythonRequirements``.

        You should use the ``multiple`` method if you have more
        requirements from the same manager. This can receive both tuples of
        strings, in case you want a specific version, or a simple string, in
        case you want the latest version to be specified.

        This is the case where you would provide strings only, to specify the
        latest version automatically:

        >>> REQUIREMENTS = PythonRequirement.multiple(
        ...     'coala_decorators', 'setuptools')

        And if you choose to mix them, specifying version for some and for some
        not:

        >>> REQUIREMENTS = PythonRequirement.multiple(
        ...     'coala_decorators', ('setuptools', '19.2'))

        In case you provide too many arguments into the tuple, an error will be
        raised:

        >>> REQUIREMENTS = PythonRequirement.multiple(
        ...     'coala_decorators', ('setuptools', '19.2', 'colorama'))
        Traceback (most recent call last):
        ...
        TypeError: The tuple must have 2 elements.

        The same would happen in case you provide something different than a
        string or a tuple:

        >>> x = [1, 2, 3, 4]
        >>> REQUIREMENTS = PythonRequirement.multiple(x)
        Traceback (most recent call last):
        ...
        TypeError: The arguments need to be tuples or strings.

        :param args:       Should be tuples of strings: ``('packageName',
                           'version')`` or strings: ``'packageName'`` if latest
                           version is wanted.
        :return:           A tuple containing ``PythonRequirements``.
        :raises TypeError: In case the tuples contain more or less than two
                           elements. Also raised when arguments are neither
                           tuples nor strings.
        """
        reqs = []
        for requirement in args:
            if isinstance(requirement, str):
                reqs.append(cls(requirement),)
            elif isinstance(requirement, tuple):
                try:
                    name, version = requirement
                    reqs.append(cls(name, version),)
                except ValueError:
                    raise TypeError('The tuple must have 2 elements.')
            else:
                raise TypeError('The arguments need to be tuples or strings.')
        return tuple(reqs)
