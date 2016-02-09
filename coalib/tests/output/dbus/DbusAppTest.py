import unittest
from unittest.case import skipIf

try:
    from coalib.output.dbus.DbusApp import DbusApp
    skip, message = False, ''
except ImportError as err:
    skip, message = True, str(err)


@skipIf(skip, message)
class DbusAppTest(unittest.TestCase):

    def test_docs(self):
        uut = DbusApp(app_id=1)
        doc1 = __file__
        doc2 = __file__ + ".txt"

        uut.create_document(doc1)
        self.assertIn(doc1, uut.docs)

        uut.dispose_document(doc2)
        self.assertNotIn(doc2, uut.docs)
        self.assertIn(doc1, uut.docs)

        uut.dispose_document(doc1)
        self.assertNotIn(doc1, uut.docs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
