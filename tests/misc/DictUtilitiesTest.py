import unittest
from collections import OrderedDict

from coalib.misc.DictUtilities import inverse_dicts, update_ordered_dict_key


class DictUtilitiesTest(unittest.TestCase):

    def test_inverse_dicts(self):
        self.dict1 = {1: [1, 2, 3], 2: [3, 4, 5]}
        self.dict2 = {2: [1], 3: [2], 4: [3, 4]}
        self.dict3 = {1: 2, 3: 4, 4: 4, 5: 4}
        self.dict4 = {2: 3, 4: 4}
        result = inverse_dicts(self.dict3)
        self.assertEqual({2: [1], 4: [3, 4, 5]}, result)

        result = inverse_dicts(self.dict1)
        self.assertEqual({1: [1], 2: [1], 3: [1, 2], 4: [2], 5: [2]}, result)

        result = inverse_dicts(self.dict3, self.dict4)
        self.assertEqual({2: [1], 3: [2], 4: [3, 4, 5, 4]}, result)

        result = inverse_dicts(self.dict1, self.dict2)
        self.assertEqual({1: [1, 2],
                          2: [1, 3],
                          3: [1, 2, 4],
                          4: [2, 4],
                          5: [2]}, result)

    def test_update_ordered_dict_key(self):
        self.ordered_dict = OrderedDict()
        self.ordered_dict['default'] = 'Some stuff'
        self.ordered_dict['pythoncheck'] = 'Somemore stuff'
        self.ordered_dict = update_ordered_dict_key(self.ordered_dict,
                                                    'default',
                                                    'coala')
        self.assertTrue('coala' in self.ordered_dict)
        self.assertEqual("OrderedDict([('coala', 'Some stuff'), "
                         "('pythoncheck', 'Somemore stuff')])",
                         self.ordered_dict.__str__())
        self.ordered_dict = update_ordered_dict_key(self.ordered_dict,
                                                    'coala',
                                                    'section')
        self.assertTrue('section' in self.ordered_dict)
        self.assertEqual("OrderedDict([('section', 'Some stuff'), "
                         "('pythoncheck', 'Somemore stuff')])",
                         self.ordered_dict.__str__())
