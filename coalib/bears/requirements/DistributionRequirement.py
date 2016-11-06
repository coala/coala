from coalib.bears.requirements.PackageRequirement import PackageRequirement


class DistributionRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifices the
    proper type automatically.
    """

    def __init__(self, **manager_commands):
        """
        Constructs a new ``DistributionRequirement``, using the
        ``PackageRequirement`` constructor.

        >>> dr = DistributionRequirement(apt_get='libclang', dnf='libclangg')
        >>> dr.package['apt_get']
        'libclang'
        >>> dr.package['dnf']
        'libclangg'

        :param manager_commands: comma separated (type='package') pairs.
        """
        self.package = manager_commands
