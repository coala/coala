# import sys
#
# sys.path.insert(0, ".")
# import unittest
# from coalib.collecting.Collector import Collector
#
#
# class TestEmptyBasicCollector(unittest.TestCase):
#     def setUp(self):
#         self.uut = Collector()
#
#     def test_raises(self):
#         self.assertRaises(NotImplementedError, self.uut.collect)
#
#         self.assertRaises(ValueError, iter, self.uut)
#         self.assertRaises(ValueError, list, self.uut)
#         self.assertRaises(ValueError, len, self.uut)
#         self.assertRaises(ValueError, self.uut.__getitem__, 90)
#         self.assertRaises(ValueError, reversed, self.uut)
#
#
# class TestCollectedBasicCollector(unittest.TestCase):
#     def setUp(self):
#         self.uut = Collector()
#         self.uut._items = [1, 2, 3]
#
#     def test_list(self):
#         self.assertEqual(list(self.uut), [1, 2, 3])
#
#     def test_len(self):
#         self.assertEqual(len(self.uut), 3)
#
#     def test_getitem(self):
#         self.assertEqual(self.uut[0], 1)
#         self.assertEqual(self.uut[2], 3)
#         self.assertEqual(self.uut[-1], 3)
#
#         self.assertRaises(IndexError, self.uut.__getitem__, 90)
#
#     def test_reversed(self):
#         self.assertEqual(list(reversed(self.uut)), [3, 2, 1])
#
#
# if __name__ == '__main__':
#     unittest.main(verbosity=2)
