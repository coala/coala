import unittest

from coalib.parsing.info_extraction.Info import Info


class InfoTest(unittest.TestCase):

    def setUp(self):
        self.base_info = Info(
            'source_file',
            'base_info_value')

        class InfoA(Info):
            description = 'Information A'

            def __init__(self,
                         source,
                         value,
                         extra_param):
                super().__init__(source, value)
                self.extra_param = extra_param

        self.info_a = InfoA(
            'source_file',
            'info_a_value',
            'extra_param_value')

    def test_main(self):
        self.assertEqual(self.base_info.name, 'Info')
        self.assertEqual(self.base_info.value, 'base_info_value')
        self.assertEqual(self.base_info.source, 'source_file')
        self.assertEqual(self.base_info.description, 'Some information')

    def test_derived_instances(self):
        self.assertEqual(self.info_a.name, 'InfoA')
        self.assertEqual(self.info_a.value, 'info_a_value')
        self.assertEqual(self.info_a.source, 'source_file')
        self.assertEqual(self.info_a.extra_param, 'extra_param_value')
        self.assertEqual(self.info_a.description, 'Information A')
