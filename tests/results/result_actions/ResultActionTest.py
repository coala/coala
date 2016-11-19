import unittest

from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction
from coalib.settings.Section import Section


class ResultActionTest(unittest.TestCase):

    def test_api(self):
        uut = ResultAction()
        result = Result('', '')

        self.assertRaises(NotImplementedError, uut.apply, 5, {}, {})
        self.assertRaises(NotImplementedError,
                          uut.apply_from_section,
                          '',
                          {},
                          {},
                          Section('name'))

        self.assertRaises(TypeError, uut.apply_from_section, '', {}, {}, 5)
        self.assertRaises(TypeError,
                          uut.apply_from_section,
                          '',
                          5,
                          {},
                          Section('name'))
        self.assertRaises(TypeError,
                          uut.apply_from_section,
                          '',
                          {},
                          5,
                          Section('name'))

        self.assertEqual(len(uut.get_metadata().non_optional_params), 0)
        self.assertEqual(len(uut.get_metadata().optional_params), 0)
        self.assertEqual(uut.get_metadata().name, 'ResultAction')
        self.assertTrue(uut.is_applicable(result, None, None))
