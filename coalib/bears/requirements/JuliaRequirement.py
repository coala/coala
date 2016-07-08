import shlex

from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.misc.Shell import call_without_output

from coala_utils.string_processing import escape


class JuliaRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``julia``, without using the manager name.
    """

    def __init__(self, package, version=""):
        """
        Constructs a new ``JuliaRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = JuliaRequirement('Lint', '19.2')
        >>> pr.manager
        'julia'
        >>> pr.package
        'Lint'
        >>> pr.version
        '19.2'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'julia', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> JuliaRequirement('Lint').install_command()
        'julia -e \\'Pkg.add("Lint")\\''

        :return: A string with the installation command.
        """
        code = 'Pkg.add("{}")'.format(escape(self.package, '\\"'))
        args = ('julia', '-e', shlex.quote(code))
        return ' '.join(args)

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :return: ``True`` if dependency is installed, ``False`` otherwise.
        """
        # We need to check explicitly if `nothing` is returned, as this happens
        # when the package is *registered*, but *not installed*. If it's not
        # even registered, julia will throw an exception which lets julia exit
        # with an error code different from 0.
        code = 'Pkg.installed("{}")==nothing?exit(1):exit(0)'.format(
            escape(self.package, '\\"'))
        args = ('julia', '-e', code)
        return not call_without_output(args)
