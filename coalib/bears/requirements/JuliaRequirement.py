from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.misc.Shell import call_without_output


class JuliaRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``julia``, without using the manager name.
    """

    def __init__(self, package, version="", flag=""):
        """
        Constructs a new ``JuliaRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = JuliaRequirement('"Pkg.add(\"Lint\")"', '19.2', '-e')
        >>> pr.manager
        'julia'
        >>> pr.package
        '"Pkg.add(\"Lint\")"'
        >>> pr.version
        '19.2'
        >>> pr.flag
        '-e'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        :param flag:    A string that specifies any additional flags, that
                        are passed to the manager.
        """
        PackageRequirement.__init__(self, 'julia', package, version)
        self.flag = flag

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> JuliaRequirement("Lint").install_command()
        'julia -e "Pkg.add(\"Lint\")'

        :param return: A string with the installation command.
        """
        return 'julia {} "Pkg.add(\"{}\")'.format(self.flag, self.package)

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """

        return not call_without_output(
         ('julia', '-e', '"Pkg.installed(\"' + self.package + '\")"'))
