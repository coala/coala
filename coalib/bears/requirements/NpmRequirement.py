from coalib.bears.requirements.PackageRequirement import PackageRequirement


class NpmRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``npm``, without using the manager name.
    """

    def __init__(self, package, version=""):
        """
        Constructs a new ``NpmRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = NpmRequirement('ramllint', '6.2')
        >>> pr.manager
        'npm'
        >>> pr.package
        'ramllint'
        >>> pr.version
        '6.2'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'npm', package, version)
