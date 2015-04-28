import sys

sys.path.insert(0, ".")
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.misc.i18n import _
import unittest


class RESULT_SEVERITYTest(unittest.TestCase):
    def test_str_conversion(self):
        self.assertEqual(_("INFO"),
                         RESULT_SEVERITY.__str__(RESULT_SEVERITY.INFO))
        self.assertEqual(_("NORMAL"),
                         RESULT_SEVERITY.__str__(RESULT_SEVERITY.NORMAL))
        self.assertEqual(_("MAJOR"),
                         RESULT_SEVERITY.__str__(RESULT_SEVERITY.MAJOR))


if __name__ == '__main__':
    unittest.main(verbosity=2)
