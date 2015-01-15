"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import sys

sys.path.insert(0, ".")
import unittest
from coalib.settings.FunctionMetadata import FunctionMetadata


class TestClass:
    def __init__(self, param1, param2, param3=5, param4: int=6):
        """
        Description

        :param param2: d
        :param param4: p4 desc
        :return: ret
        """


class FunctionMetadataTestCase(unittest.TestCase):
    def test_construction(self):
        self.assertRaises(TypeError, FunctionMetadata, 5)
        self.assertRaises(TypeError, FunctionMetadata, "name", desc=5)
        self.assertRaises(TypeError, FunctionMetadata, "name", retval_desc=5)
        self.assertRaises(TypeError, FunctionMetadata, "name", non_optional_params=5)
        self.assertRaises(TypeError, FunctionMetadata, "name", optional_params=5)
        self.assertRaises(TypeError, FunctionMetadata.from_function, 5)
        self.check_function_metadata_data_set(FunctionMetadata("name"), "name")

    def test_from_function(self):
        uut = FunctionMetadata.from_function(self.test_from_function)
        self.check_function_metadata_data_set(uut, "test_from_function")

        uut = FunctionMetadata.from_function(TestClass(5, 5).__init__)
        self.check_function_metadata_data_set(uut,
                                              "__init__",
                                              desc="Description",
                                              retval_desc="ret",
                                              non_optional_params={
                                                  "param1": (uut.str_nodesc, None),
                                                  "param2": ("d", None)
                                              },
                                              optional_params={
                                                  "param3": (uut.str_nodesc + " (" + uut.str_optional.format("5") + ")",
                                                             None, 5),
                                                  "param4": ("p4 desc (" + uut.str_optional.format("6") + ")", int, 6)
                                              })

    def check_function_metadata_data_set(self,
                                         metadata,
                                         name,
                                         desc="",
                                         retval_desc="",
                                         non_optional_params={},
                                         optional_params={}):
        self.assertEqual(metadata.name, name)
        self.assertEqual(metadata.desc, desc)
        self.assertEqual(metadata.retval_desc, retval_desc)
        self.assertEqual(metadata.non_optional_params, non_optional_params)
        self.assertEqual(metadata.optional_params, optional_params)



if __name__ == '__main__':
    unittest.main(verbosity=2)
