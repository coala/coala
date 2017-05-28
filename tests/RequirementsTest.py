import os
import sys
import unittest

from coalib.misc.Shell import run_shell_command
from packaging import version


class coalaaCITest(unittest.TestCase):

    def test_find_no_issues(self):
        with open(os.path.dirname(__file__) + '/../requirements.txt') as f:
            content = f.readlines()
        reqiredpac = []
        req_pac_ver = []

        for x in content:
            if '=' in x:
                reqiredpac.append(x[:x.find('=')-1])
                req_pac_ver.append(x[x.find('=')+1:-1])

        with open(os.path.dirname(__file__) + '/../test-requirements.txt') as f:
            content = f.readlines()
        for x in content:
            if '=' in x:
                reqiredpac.append(x[:x.find('=')-1])
                req_pac_ver.append(x[x.find('=')+1:-1])

        output = run_shell_command([sys.executable, '-m', 'pip', 'freeze'])
        split_list = output[0].split('\n')
        package = []
        temporary = []
        for i in split_list:
            package.append(i[:i.find('=')])
            temporary.append(i[i.find('==')+2:])

        package = [x.lower() for x in package]
        reqiredpac = [x.lower() for x in reqiredpac]
        package = [x.replace('-', '_') for x in package]
        reqiredpac = [x.replace('-', '_') for x in reqiredpac]

        cur_version = []
        for k in temporary:
            while(k.count('.') > 1):
                k = k[:k.rfind('.')]
            cur_version.append(k)

        req_version = []
        for k in req_pac_ver:
            while(k.count('.') > 1):
                k = k[:k.rfind('.')]
            req_version.append(k)

        for k in reqiredpac:
            if 'wheel' not in k:
                self.assertIn(k, package)

        for k in reqiredpac:
            if 'wheel' not in k:
                self.assertEqual(version.parse(req_version[
                                 reqiredpac.index(k)])
                                 <= version.parse(cur_version[
                                     package.index(k)]),
                                 True, 'Not correct cur_version of '+k+'. Need '
                                 + req_pac_ver[reqiredpac.index(k)]
                                 + ' Installed: '
                                 + cur_version[package.index(k)])
