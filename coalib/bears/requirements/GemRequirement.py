from coalib.bears.requirements.Requirement import Requirement
from coalib.misc.Shell import call_without_output
import platform


class GemRequirement(Requirement):
    """
    This class is a subclass of ``Requirement``. It specifies the
    proper type for ``ruby`` packages automatically and provides a function to
    check for the requirement.
    """

    def __init__(self, package, version="", require=""):
        """
        Constructs a new ``GemRequirement``, using the ``Requirement``
        constructor.

        >>> pr = GemRequirement('setuptools', '19.2', 'flag')
        >>> pr.type
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
        Requirement.__init__(self, 'gem', package, version)
        self.require = require

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        cmd = ['gem', 'list', '-i', self.package]
        if platform.system() == 'Windows':  # pragma: no cover
            cmd = ['cmd', '/c'] + cmd
        return not call_without_output(cmd)
