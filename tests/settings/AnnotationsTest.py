from unittest import TestCase

from coalib.settings.Annotations import typechain


class AnnotationsTest(TestCase):

    def test_empty(self):
        with self.assertRaises(TypeError) as ctx:
            typechain()
        self.assertEqual(str(ctx.exception), 'No arguments were provided.')

    def test_with_lambda(self):
        function = typechain(lambda x: int(x) > 0)
        with self.assertRaises(ValueError):
            function('str')
        self.assertEqual(function('10'), True)

    def test_with_function(self):
        def positive(val):
            val = int(val)
            if val > 0:
                return val
            raise ValueError
        function = typechain(positive, ord)
        with self.assertRaises(ValueError):
            function(0)
        with self.assertRaises(ValueError):
            function('str')
        self.assertEqual(function('10'), 10)
        self.assertEqual(function('0'), 48)

    def test_with_function_without_arguments(self):
        def dummy():
            return 10
        function = typechain(dummy)
        with self.assertRaises(ValueError):
            function(0)

    def test_with_custom_type(self):
        class Positive:

            def __init__(self, val):
                val = int(val)
                if val > 0:
                    self.val = val
                else:
                    raise ValueError

        function = typechain(Positive, ord)
        with self.assertRaises(ValueError):
            function(0)
        obj = function('10')
        self.assertIsInstance(obj, Positive)
        self.assertEqual(obj.val, 10)
        self.assertEqual(function('0'), 48)

    def test_with_empty_class(self):
        class Dummy:
            pass

        function = typechain(Dummy)
        with self.assertRaises(ValueError):
            function('str')
        dummy = Dummy()
        self.assertEqual(function(dummy), dummy)
