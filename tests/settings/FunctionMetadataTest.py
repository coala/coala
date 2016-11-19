import unittest

from coalib.settings.FunctionMetadata import FunctionMetadata
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class TestClass:

    def __init__(self, param1, param2, param3=5, param4: int=6):
        """
        Description

        :param param2: d
        :param param4: p4 desc
        :return:       ret
        """

    def good_function(self, a_param: int):
        pass

    def bad_function(self, bad_param: 'no function'):
        pass


class FunctionMetadataTest(unittest.TestCase):

    def test_construction(self):
        self.check_function_metadata_data_set(FunctionMetadata('name'), 'name')

    def test_from_function(self):
        uut = FunctionMetadata.from_function(self.test_from_function)
        self.check_function_metadata_data_set(uut, 'test_from_function')
        # setattr on bound methods will fail, vars() will use the dict from
        # the unbound method which is ok.
        vars(self.test_from_function)['__metadata__'] = (
            FunctionMetadata('t'))
        uut = FunctionMetadata.from_function(self.test_from_function)
        self.check_function_metadata_data_set(uut, 't')

        uut = FunctionMetadata.from_function(TestClass(5, 5).__init__)
        self.check_function_metadata_data_set(
            uut,
            '__init__',
            desc='Description',
            retval_desc='ret',
            non_optional_params={
                'param1': (uut.str_nodesc, None),
                'param2': ('d', None)
            },
            optional_params={
                'param3': (uut.str_nodesc + ' ('
                           + uut.str_optional.format('5') + ')',
                           None, 5),
                'param4': ('p4 desc ('
                           + uut.str_optional.format('6') + ')', int, 6)})

        uut = FunctionMetadata.from_function(TestClass(5, 5).__init__,
                                             omit={'param3', 'param2'})
        self.check_function_metadata_data_set(
            uut,
            '__init__',
            desc='Description',
            retval_desc='ret',
            non_optional_params={
                'param1': (uut.str_nodesc,
                           None)
            },
            optional_params={
                'param4': ('p4 desc (' + uut.str_optional.format('6') + ')',
                           int,
                           6)})

    def test_create_params_from_section_invalid(self):
        section = Section('name')
        section.append(Setting('bad_param', 'value'))
        uut = FunctionMetadata.from_function(TestClass(5, 5).bad_function)

        with self.assertRaises(ValueError):
            uut.create_params_from_section(section)

    def test_create_params_from_section_valid(self):
        section = Section('name')
        section.append(Setting('a_param', 'value'))
        uut = FunctionMetadata.from_function(TestClass(5, 5).good_function)

        with self.assertRaises(ValueError):
            uut.create_params_from_section(section)

        section.append(Setting('a_param', '5'))
        params = uut.create_params_from_section(section)
        self.assertEqual(params['a_param'], 5)

    def check_function_metadata_data_set(self,
                                         metadata,
                                         name,
                                         desc='',
                                         retval_desc='',
                                         non_optional_params=None,
                                         optional_params=None):
        non_optional_params = non_optional_params or {}
        optional_params = optional_params or {}

        self.assertEqual(metadata.name, name)
        self.assertEqual(metadata.desc, desc)
        self.assertEqual(metadata.retval_desc, retval_desc)
        self.assertEqual(metadata.non_optional_params, non_optional_params)
        self.assertEqual(metadata.optional_params, optional_params)

    def test_add_deprecated_param(self):
        uut = FunctionMetadata(
            'test',
            non_optional_params={'not_optional': ('desc', str)},
            optional_params={'optional': ('desc2', str, 'default')})

        uut.add_deprecated_param('optional', 'old_optional')
        uut.add_deprecated_param('not_optional', 'old_not_optional')

        self.assertEqual(uut.non_optional_params,
                         {'not_optional': ('desc', str)})
        self.assertEqual(uut.optional_params,
                         {'optional': ('desc2', str, 'default'),
                          'old_optional': ('desc2', str, 'default'),
                          'old_not_optional': ('desc', str, None)})

    def test_merge(self):
        metadata1 = FunctionMetadata(
            'main',
            'Desc of main.\n',
            'Returns 0 on success',
            {'argc': ('argc desc', None), 'argv': ('argv desc', None)},
            {'opt': ('opt desc', int, 88)},
            {'self', 'A'},
            {'test1'})

        metadata2 = FunctionMetadata(
            'process',
            'Desc of process.\n',
            'Returns the processed stuff.',
            {'argc': ('argc desc from process', int),
             'to_process': ('to_process desc', int)},
            {'opt2': ('opt2 desc', str, 'hello')},
            {'self', 'B'},
            {'test2'})

        metadata3 = FunctionMetadata('nodesc', '', '', {}, {})

        merged_metadata = FunctionMetadata.merge(metadata1,
                                                 metadata2,
                                                 metadata3)

        self.assertEqual(
            merged_metadata.name,
            "<Merged signature of 'main', 'process', 'nodesc'>")
        self.assertEqual(merged_metadata.desc, 'Desc of process.\n')
        self.assertEqual(merged_metadata.retval_desc,
                         'Returns the processed stuff.')
        self.assertEqual(
            merged_metadata.non_optional_params,
            {'argc': ('argc desc from process', int),
             'argv': ('argv desc', None),
             'to_process': ('to_process desc', int)})
        self.assertEqual(
            merged_metadata.optional_params,
            {'opt': ('opt desc', int, 88),
             'opt2': ('opt2 desc', str, 'hello')})
        self.assertEqual(
            merged_metadata.omit,
            frozenset({'self', 'A', 'B'}))
        self.assertEqual(
            merged_metadata.deprecated_params,
            frozenset({'test1', 'test2'}))
