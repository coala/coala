import unittest

from coalib.bearlib import deprecate_settings


@deprecate_settings(new='old')
def func(new):
    """
    This docstring will not be lost.
    """


class DeprecateSettingsTest(unittest.TestCase):

    def test_docstring(self):
        self.assertEqual(func.__doc__.strip(),
                         'This docstring will not be lost.')
