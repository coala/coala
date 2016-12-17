from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.misc.Shell import call_without_output


class CabalRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequiment``, It specifies the proper
    type for ``cabal`` packages automatically and provide a function to check
    for the requirment.
    """

    def __init__(self, package, version=''):
        """
        Constructs a new ``CabalRequirment``, using the ``PackageRequirment``
        constructor.

        >>> cr = CabalRequirement('setuptools', '19.2')
        >>> cr.type
        'cabal'
        >>> cr.package
        'setuptools'
        >>> cr.version
        '19.2'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'cabal', package, version)

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        return not call_without_output(('cabal', 'info', self.package))
