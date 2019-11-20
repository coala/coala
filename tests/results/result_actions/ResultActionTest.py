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
        self.assertEqual(uut.get_metadata().id, id(uut))
        self.assertTrue(uut.is_applicable(result, None, None))

        self.assertEqual(uut.get_metadata().desc,
                         'No description. Something went wrong.')
        uut.description = 'Test Action'
        self.assertEqual(uut.get_metadata().desc, 'Test Action')
