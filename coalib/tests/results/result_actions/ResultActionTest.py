import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.result_actions.ResultAction import ResultAction
from coalib.settings.Section import Section


class ResultActionTestCase(unittest.TestCase):
    def test_api(self):
        uut = ResultAction()

        self.assertRaises(NotImplementedError, uut.apply, 5, {}, {})
        self.assertRaises(NotImplementedError, uut.apply_from_section, "", {}, {}, Section("name"))

        self.assertRaises(TypeError, uut.apply_from_section, "", {}, {}, 5)
        self.assertRaises(TypeError, uut.apply_from_section, "", 5, {}, Section("name"))
        self.assertRaises(TypeError, uut.apply_from_section, "", {}, 5, Section("name"))

        self.assertEqual(len(uut.get_metadata().non_optional_params), 0)
        self.assertEqual(len(uut.get_metadata().optional_params), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
