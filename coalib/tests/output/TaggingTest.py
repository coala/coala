import unittest
import hashlib
import os
import sys

sys.path.insert(0, ".")
from coalib.output.Tagging import tag_results
from coalib.misc.Constants import Constants


class TaggingTest(unittest.TestCase):
    def test_tag_results(self):
        tag_results("test_tag", "/root", {})
        default_hash = hashlib.sha224(
            ("/root" + " test_tag").encode()).hexdigest()
        self.assertTrue(os.path.exists(Constants.TAGS_DIR+"/"+default_hash))
        os.remove(Constants.TAGS_DIR+"/"+default_hash)


if __name__ == "__main__":
    unittest.main(verbosity=2)
