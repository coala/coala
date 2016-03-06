import unittest

from coalib.bearlib.abstractions.DefaultLinterInterface import (
    DefaultLinterInterface)


class DefaultLinterInterfaceTest(unittest.TestCase):

    def test_create_arguments(self):
        with self.assertRaises(NotImplementedError):
            DefaultLinterInterface.create_arguments("somefile", [], None)

    def test_generate_config(self):
        self.assertIsNone(
            DefaultLinterInterface.generate_config("somefile", []))
