import sys
import unittest

sys.path.insert(0, ".")
from coalib.output.ClosableObject import ClosableObject, close_objects


class ClosableObjectTest(unittest.TestCase):
    def setUp(self):
        self.uut = ClosableObject()

    def test_closing(self):
        self.assertFalse(self.uut._closed)
        self.uut.close()
        self.assertTrue(self.uut._closed)
        self.uut.close()
        self.assertTrue(self.uut._closed)

    def test_close_objects(self):
        close_objects(None, 5)
        close_objects(self.uut)
        self.assertTrue(self.uut._closed)


if __name__ == '__main__':
    unittest.main(verbosity=2)
