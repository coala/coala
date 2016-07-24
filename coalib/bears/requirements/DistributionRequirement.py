import platform

from coalib.bears.requirements.PackageRequirement import PackageRequirement


class DistributionRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    distribution specific requirements, without using the manager name.
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

        :param manager_commands: comma separated (manager='package') pairs.
        """
        self.package = manager_commands

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        :param return: A string with the installation command. An empty string
                       if the command could not be supplied.
        """
        manager_dict = {'Fedora': 'dnf',
                        'Ubuntu': 'apt_get',
                        'Debian': 'apt_get',
                        'SuSE': 'zypper',
                        'redhat': 'yum',
                        'arch': 'pacman'}

        if (platform.linux_distribution()[0] in manager_dict.keys() and
                manager_dict[platform.linux_distribution()[0]]
                in self.package.keys()):
            manager = manager_dict[platform.linux_distribution()[0]]
            return [manager.replace("_", "-"),
                    'install', self.package[manager]]
        else:
            package_possibilites = (
                {package for package in self.package.values()})
            print('The package could not be automatically installed on your '
                  'operating system. Please try installing it manually. It'
                  ' should look like this: ' + repr(package_possibilites))
            raise OSError
