import unittest

from coalib.bearlib.aspects.exceptions import AspectLookupError


class ExceptionTest(unittest.TestCase):

    def test_AspectLookupError(self):
        with self.assertRaisesRegex(
                AspectLookupError,
                "^Error when trying to search aspect named 'NOASPECT'$"):
            raise AspectLookupError('NOASPECT')
