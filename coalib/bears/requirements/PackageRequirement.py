from coala_utils.decorators import generate_eq, generate_repr


@generate_eq("manager", "package", "version")
@generate_repr()
class PackageRequirement:
    """
    This class helps keeping track of bear requirements. It should simply
    be appended to the REQUIREMENTS tuple inside the Bear class.

    Two ``PackageRequirements`` should always be equal if they have the same
    manager, package and version:

    >>> pr1 = PackageRequirement('pip', 'coala_decorators', '0.1.0')
    >>> pr2 = PackageRequirement('pip', 'coala_decorators', '0.1.0')
    >>> pr1 == pr2
    True
    """

    def __init__(self, manager: str, package: str, version=""):
        """
        Constructs a new ``PackageRequirement``.

        >>> pr = PackageRequirement('pip', 'colorama', '0.1.0')
        >>> pr.manager
        'pip'
        >>> pr.package
        'colorama'
        >>> pr.version
        '0.1.0'

        :param manager: A string with the name of the manager (pip, npm, etc).
        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        self.manager = manager
        self.package = package
        self.version = version

    def check(self):
        """
        Check if the requirement is satisfied.

        >>> PackageRequirement('pip', 'coala_decorators', '0.2.1').check()
        Traceback (most recent call last):
        ...
        NotImplementedError

        :return: Returns True if satisfied, False if not.
        """
        raise NotImplementedError

    @classmethod
    def multiple(cls, *args):
        """
        Creates a set of multiple instances of a class.

        Should not be instances of ``PackageRequirement``, as this is an
        abstract class:

        >>> PackageRequirement.multiple(('pip', 'coala_decorators', '0.1.0'),)
        Traceback (most recent call last):
        ...
        NotImplementedError

        It can only be used for requirements of the same manager. For example,
        consider a manager ``XYZRequirement`` that inherits from
        PackageRequirement. This subclass will have the manager set to XYZ:

        >>> class XYZRequirement(PackageRequirement):
        ...     manager = 'xyz'
        ...     def __init__(self, package, version=""):
        ...         PackageRequirement.__init__(self, package, version)

        This is the case where you would provide strings only, to specify the
        latest version automatically:

        >>> REQUIREMENTS = XYZRequirement.multiple(
        ...     "package1", "package2")

        And if you choose to mix them, specifying version for some and for some
        not:

        >>> REQUIREMENTS = XYZRequirement.multiple(
        ...     'package1', ('package2', '2.0'))

        Lists are also valid arguments:

        >>> REQUIREMENTS = XYZRequirement.multiple(
        ...     ['package1', '1.0'],)

        In case you provide too many arguments into the tuple, an error will be
        raised:

        >>> REQUIREMENTS = XYZRequirement.multiple(
        ...     'package1', ('package2', '2.0', 'package3'))
        Traceback (most recent call last):
        ...
        TypeError: Too many elements provided.

        :param args:       In the subclasses, the ``manager`` is already
                           specified, so they hould be iterables with two
                           elements: ``('packageName', 'version')`` or strings:
                           ``'packageName'`` if latest version is wanted.
        :return:           A tuple containing instances of the subclass.
        :raises TypeError: In case the iterables contain more than two
                           elements.
        """
        if cls == PackageRequirement:
            raise NotImplementedError
        else:
            reqs = []
            for requirement in args:
                if isinstance(requirement, str):
                    reqs.append(cls(requirement))
                elif len(requirement) == 2:
                    name, version = requirement
                    reqs.append(cls(name, version))
                else:
                    raise TypeError('Too many elements provided.')
            return set(reqs)
