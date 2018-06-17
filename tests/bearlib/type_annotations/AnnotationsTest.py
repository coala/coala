import unittest
from coalib.settings.Section import Section
from tests.test_bears.AnnotationsTestBear import (
    AnnotationsTestBear)


class AnnotationsTest(unittest.TestCase):
    def setUp(self):
        self.section = Section('new_section')
        self.bear = AnnotationsTestBear(self.section, None)
        self.acceptable_values = [
            ('number', [3, 4]), ('fruit', ['mango', 'banana']),
            ('d', [5, 6, 'pineapple'])]

    def test_add_value_checks_1(self):
        with self.assertRaises(ValueError,
                               msg='Invalid value "pineapple"'
                                   'given to the bear setting "fruit"'):
            self.bear.run(3, 'pineapple')
        self.assertEqual(self.bear.ACCEPTABLE_VALUES_FOR_SETTINGS,
                         self.acceptable_values)

    def test_add_value_checks_2(self):
        with self.assertRaises(ValueError,
                               msg='Invalid value "5" given to'
                                   'the bear setting "number"'):
            self.bear.run(5, 'mango')
        self.assertEqual(self.bear.ACCEPTABLE_VALUES_FOR_SETTINGS,
                         self.acceptable_values)

    def test_add_value_checks_3(self):
        with self.assertRaises(ValueError,
                               msg='Invalid value "5" given to'
                                   'the bear setting "number"'):
            self.bear.run(5, 'pineapple')
        self.assertEqual(self.bear.ACCEPTABLE_VALUES_FOR_SETTINGS,
                         self.acceptable_values)

    def test_add_value_checks_4(self):
        with self.assertRaises(ValueError,
                               msg='Invalid value "4" given to the'
                                   'bear setting "d"'):
            self.bear.run(3, 'mango', 'anything', 4)
        self.assertEqual(self.bear.ACCEPTABLE_VALUES_FOR_SETTINGS,
                         self.acceptable_values)

    def test_Add_value_checks_5(self):
        self.bear.run(3, 'mango')
        self.assertEqual(self.bear.ACCEPTABLE_VALUES_FOR_SETTINGS,
                         self.acceptable_values)

    def test_CALL_FROM_QUICKSTART(self):
        self.bear.CALL_TO_POPULATE = True
        self.bear.run(3, 'pineapple')  # invalid value to bear setting
        self.assertEqual(self.bear.ACCEPTABLE_VALUES_FOR_SETTINGS,
                         self.acceptable_values)
