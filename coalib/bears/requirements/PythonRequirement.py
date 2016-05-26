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
