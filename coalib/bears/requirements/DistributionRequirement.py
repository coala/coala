import platform

from coalib.bears.requirements.Requirement import Requirement


class DistributionRequirement(Requirement):
    """
    This class is a subclass of ``Requirement``. It specifies the
    proper type automatically.
    """

    def __init__(self, **manager_commands):
        """
        Constructs a new ``DistributionRequirement``, using the
        ``Requirement`` constructor.

        >>> dr = DistributionRequirement(apt_get='libclang', dnf='libclangg')
        >>> dr.package['apt_get']
        'libclang'
        >>> dr.package['dnf']
        'libclangg'

        :param manager_commands: comma separated (type='package') pairs.
        """
        self.package = manager_commands
