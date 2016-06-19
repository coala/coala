from coalib.bears.requirements.PackageRequirement import PackageRequirement


class GemRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``gem``, without using the manager name.
    """

    def __init__(self, package, version="", require=""):
        """
        Constructs a new ``GemRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = GemRequirement('setuptools', '19.2', 'flag')
        >>> pr.manager
        'gem'
        >>> pr.package
        'setuptools'
        >>> pr.version
        '19.2'
        >>> pr.require
        'flag'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        :param require: A string that specifies any additional flags, that
                        would be used with ``require``.
        """
        PackageRequirement.__init__(self, 'gem', package, version)
        self.require = require
