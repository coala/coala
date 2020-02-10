import unittest
import sys

from coalib.core.PersistentHash import persistent_hash


class PersistentHashTest(unittest.TestCase):

    def test_int(self):
        # FAILS only in python 3.7 builds
        # the hash string tends to be b'\xf9\x85\xb9\x15H\xa0\x8f\xb7;\xb3\xa8\
        # xc3\x82\xa3\xe8\xe0!\xf7\xfc\xfc'
        if sys.version_info.major == 3 and sys.version_info.minor >= 7:
            self.assertEqual(
                persistent_hash(3),
                b'\xf9\x85\xb9\x15H\xa0\x8f\xb7;\xb3\xa8\xc3\x82\xa3\xe8\xe0
                !\xf7\xfc\xfc')
        else:
            self.assertEqual(
                persistent_hash(3),
                b'\xd8YA\x03x|c"@\xe8\x8b~\xb9\xb6\x8d\x95\x8dzp\x8a')

    def test_int_tuples(self):
        self.assertEqual(
            persistent_hash((1, 2, 3)),
            b'\xb5\xd6\xd7\xbeLD\x90\x9fz.\xae\xc4\xb9P\n\xf8\xf5\x03S\xb6')

    def test_sets(self):
        self.assertEqual(
            persistent_hash({'a', '1', 'g'}),
            b'\xbc\x99\x95\x97#F\x13<8\x1cK\x81\xf2KxQ@\xf6\x01%')

    def test_plain_dicts(self):
        self.assertEqual(
            persistent_hash({'a': '1', 'g': '9'}),
            b'D\xe8NL!\x8c\xec\xff\xf3\x93\xee=0K#\x1fVL\x06$')

    def test_dicts(self):
        self.assertEqual(
            persistent_hash(((), {'a': '1', 'g': '9'})),
            b'\x99E\xday\xd3\xc0;S\xb7\x01\xb1\xd6>F\xdb\xc3y\x12\xf7W')

    def test_tuple_with_sets_and_dicts(self):
        self.assertEqual(
            persistent_hash((({'g', 'a'}, {'e': '7', 'a': '1'}), {})),
            b'xvr\xa0\xd3\x9c\x125\x12H\xcf\x13\xc4\xba\xf5\x15Hz\xe2\x00')

    def test_nested_dicts(self):
        self.assertEqual(
            persistent_hash(((), {'q': {'g': '1', 'b': '8'}, 'a': {},
                                  'g': {'z', 'c', 'd'}, 'b': '8'})),
            b'\xdaI\xb5S(wb\xd7\x82\xa0\x17cV-}\x1cL\x9d\xc1a')

    def test_nested_tuples_and_dicts(self):
        self.assertEqual(
            persistent_hash((('a', 'b', {'g', 'b', '8'},
                              {'g': '1', 'a': {}, 'b': '8'}),
                             {'q': {'g': '1', 'a': '1'}, 'a': {},
                              'g': {'z', 'd'}, 'b': '8'})),
            b'\xa9z[U\xfa\xd1x\x95\x00\xf1,h%Y\xa2u\x87\xb0\xb2\x13')
