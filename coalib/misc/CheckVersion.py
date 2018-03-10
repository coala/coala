from pkg_resources import get_distribution, DistributionNotFound


def check_version(package_name, version):
    """
    Check if a particular package version is present or not.

    :param package_name:
        Package name.
    :param version:
        Version number to match.
    :return:
        ``True`` if package is installed with given ``version``,
        ``False`` otherwise.
    """
    try:
        return get_distribution(package_name).version == version
    except DistributionNotFound:
        return False
