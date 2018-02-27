import unittest

from coalib.core.PersistentHash import persistent_hash


class PersistentHashTest(unittest.TestCase):

    def test_int(self):
        self.assertEqual(
            persistent_hash(3),
            b'\xd8YA\x03x|c"@\xe8\x8b~\xb9\xb6\x8d\x95\x8dzp\x8a')

    def test_int_tuples(self):
        self.assertEqual(
            persistent_hash((1, 2, 3)),
            b'\xb5\xd6\xd7\xbeLD\x90\x9fz.\xae\xc4\xb9P\n\xf8\xf5\x03S\xb6')
