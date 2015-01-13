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
from coalib.settings.DocumentationComment import DocumentationComment


class DocumentationCommentParserTestCase(unittest.TestCase):
    def test_construction(self):
        self.assertRaises(TypeError, DocumentationComment, desc=5, param_dict={}, retval_desc="")
        self.assertRaises(TypeError, DocumentationComment, desc="", param_dict=5, retval_desc="")
        self.assertRaises(TypeError, DocumentationComment, desc="", param_dict={}, retval_desc=5)
        self.assertRaises(TypeError, DocumentationComment.from_docstring, docstring=5)

    def test_from_docstring(self):
        self.check_from_docstring_dataset("")
        self.check_from_docstring_dataset(" description only ", desc="description only")
        self.check_from_docstring_dataset(" :param test:  test description ", param_dict={
            "test": "test description"
        })
        self.check_from_docstring_dataset(" @param test:  test description ", param_dict={
            "test": "test description"
        })
        self.check_from_docstring_dataset(" :return: something ", retval_desc="something")
        self.check_from_docstring_dataset(" @return: something ", retval_desc="something")
        self.check_from_docstring_dataset("""
        Main description

        @param p1: this is
        a multiline desc for p1

        main description continues.
        :param p2: p2 description

        @return: retval description
        :return: retval description
        override
        """, desc="Main description main description continues.", param_dict={
            "p1": "this is a multiline desc for p1",
            "p2": "p2 description"
        }, retval_desc="retval description override")

    def check_from_docstring_dataset(self, docstring, desc="", param_dict={}, retval_desc=""):
        self.assertIsInstance(docstring, str, "docstring needs to be a string for this test.")
        doc_comment = DocumentationComment.from_docstring(docstring)
        self.assertEqual(doc_comment.desc, desc)
        self.assertEqual(doc_comment.param_dict, param_dict)
        self.assertEqual(doc_comment.retval_desc, retval_desc)


if __name__ == '__main__':
    unittest.main(verbosity=2)
