import unittest

from bears.tests.LocalBearTestHelper import verify_local_bear
from bears.go.GofmtBear import GofmtBear


GofmtBear = verify_local_bear(
    GofmtBear,
    (['package main', '', 'func main() {', '\treturn 1', '}'],),
    (['package main', 'func main() {', '    return 1', '}'],))


if __name__ == '__main__':
    unittest.main(verbosity=2)
