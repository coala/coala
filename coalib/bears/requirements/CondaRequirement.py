from coalib.bears.requirements.PackageRequirement import PackageRequirement


class CondaRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``conda``, without using the manager name.
    """

    def __init__(self, package, version=""):
        """
        Constructs a new ``CondaRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = CondaRequirement('clang')
        >>> pr.manager
        'conda'
        >>> pr.package
        'clang'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'conda', package, version)
