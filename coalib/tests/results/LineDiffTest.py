import unittest

from coalib.results.LineDiff import LineDiff


class LineDiffTest(unittest.TestCase):

    def test_everything(self):
        self.assertRaises(TypeError, LineDiff, delete=5)
        self.assertRaises(TypeError, LineDiff, change=5)
        self.assertRaises(TypeError, LineDiff, add_after=5)
        self.assertRaises(TypeError, LineDiff, change=True)
        self.assertRaises(TypeError, LineDiff, add_after=True)
        self.assertRaises(AssertionError,
                          LineDiff,
                          change=("1", "2"),
                          delete=True)

        self.assertEqual(LineDiff(change=("1", "2")).change, ("1", "2"))
        self.assertEqual(LineDiff(delete=True).delete, True)
        self.assertEqual(LineDiff(add_after=[]).add_after, False)
        self.assertEqual(LineDiff(add_after=["t"]).add_after, ["t"])

        uut = LineDiff()
        uut.delete = True
        self.assertRaises(AssertionError, setattr, uut, "change", ("1", "2"))
        uut.delete = False
        uut.change = ("1", "2")
        self.assertRaises(AssertionError, setattr, uut, "delete", True)

    def test_equality(self):
        self.assertEqual(LineDiff(), LineDiff())
        self.assertNotEqual(LineDiff(), LineDiff(delete=True))
        self.assertNotEqual(LineDiff(add_after=['']), LineDiff())
        self.assertNotEqual(LineDiff(add_after=['']), LineDiff(delete=True))
        self.assertNotEqual(LineDiff(change=('', 'a')), LineDiff())


if __name__ == '__main__':
    unittest.main(verbosity=2)
