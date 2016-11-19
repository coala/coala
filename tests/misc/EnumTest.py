import unittest

from coalib.misc.Enum import enum


class ProcessTest(unittest.TestCase):

    def setUp(self):
        self.uut = enum('ZERO', 'ONE', 'TWO', THREE='val')

    def test_sequentials(self):
        self.assertEqual(self.uut.ZERO, 0)
        self.assertEqual(self.uut.ONE, 1)
        self.assertEqual(self.uut.TWO, 2)
        self.assertEqual(self.uut.THREE, 'val')
        self.assertEqual(self.uut.str_dict['ZERO'], 0)
        self.assertRaises(KeyError, self.uut.str_dict.__getitem__, 'reverse')

    def test_reverse_mapping(self):
        self.assertEqual(self.uut.reverse[self.uut.ZERO], 'ZERO')
        self.assertEqual(self.uut.reverse[self.uut.ONE], 'ONE')
        self.assertEqual(self.uut.reverse[self.uut.TWO], 'TWO')
        self.assertEqual(self.uut.reverse[self.uut.THREE], 'THREE')
