from coala_utils.decorators import generate_eq, generate_repr


@generate_eq("type", "package", "version")
@generate_repr()
class PackageRequirement:
    """
    This class helps keeping track of bear requirements. It should simply
    be appended to the REQUIREMENTS tuple inside the Bear class.

    Two ``PackageRequirements`` should always be equal if they have the same
    type, package and version:

    >>> pr1 = PackageRequirement('pip', 'coala_decorators', '0.1.0')
    >>> pr2 = PackageRequirement('pip', 'coala_decorators', '0.1.0')
    >>> pr1 == pr2
    True
    """

    def __init__(self, type: str, package: str, version=""):
        """
        Constructs a new ``PackageRequirement``.

        >>> pr = PackageRequirement('pip', 'colorama', '0.1.0')
        >>> pr.type
        'pip'
        >>> pr.package
        'colorama'
        >>> pr.version
        '0.1.0'

        :param type:    A string with the name of the manager (pip, npm, etc).
        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        self.type = type
        self.package = package
        self.version = version

    def is_installed(self):
        """
        Check if the requirement is satisfied.

        >>> PackageRequirement('pip', \
                               'coala_decorators', \
                               '0.2.1').is_installed()
        Traceback (most recent call last):
        ...
        NotImplementedError

        :return: Returns True if satisfied, False if not.
        """
        raise NotImplementedError
