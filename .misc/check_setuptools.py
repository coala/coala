from __future__ import print_function

import subprocess
import sys

import setuptools


def get_setuptools_version():
    with open('requirements.txt') as f:
        for line in f:
            if line.startswith('setuptools'):
                line = line.rstrip()
                if '>=' not in line:
                    raise ValueError('%s doesnt use ">="' % line)
                _, version = line.split('>=')
                return version


def check_setuptools_version(version):
    print('Checking setuptools==%s' % version, file=sys.stderr)
    if setuptools.__version__ != version:
        print('Failed! setuptools==%s' % setuptools.__version__,
              file=sys.stderr)
        return 2

    pip_list = subprocess.check_output(['pip', 'list', '--format=legacy'])
    pip_list = pip_list.decode('utf8')
    if 'setuptools (%s)' % version not in pip_list:
        print('Failed! pip list reports wrong setuptools:\n%s' % pip_list,
              file=sys.stderr)
        return 3

if __name__ == '__main__':
    version = None
    try:
        version = get_setuptools_version()
    except Exception as e:
        print('Exception extracting setuptools version from requirements.txt: '
              '%s' % e,
              file=sys.stderr)
        sys.exit(1)

    if not version:
        print('Unable to find setuptools in requirements.txt',
              file=sys.stderr)
        sys.exit(1)
    sys.exit(check_setuptools_version(version))
