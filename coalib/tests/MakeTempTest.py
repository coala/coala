import os
import unittest

from coalib.misc.ContextManagers import make_temp


class MakeTempTest(unittest.TestCase):

    def test_temp_file_existence(self):
        """
        Test that the temporary file created exists only within the with
        statement context and not outside it
        """
        with make_temp() as temporary:
            self.assertTrue(os.path.isfile(temporary))
        self.assertFalse(os.path.isfile(temporary))

if __name__ == '__main__':
    unittest.main(verbosity=2)
