import unittest
from os.path import exists

from coala_utils.ContextManagers import make_temp
from coalib.results.Result import Result
from coalib.results.result_actions.IgnoreResultAction import IgnoreResultAction


class IgnoreResultActionTest(unittest.TestCase):

    def test_is_applicable(self):
        prior_ignore = ('IgnoreResultAction')
        associated_result = Result.from_values('origin', 'msg',
                                               "file doesn't exist", 2)

        with self.assertRaises(TypeError) as context:
            IgnoreResultAction.is_applicable('str', {}, {})
        with self.assertRaises(TypeError) as context:
            IgnoreResultAction.is_applicable('str', {}, {}, prior_ignore)

        self.assertEqual(
            IgnoreResultAction.is_applicable(associated_result, {}, {}),
            "The result is associated with source code that doesn't "
            'seem to exist.')

        self.assertEqual(
            IgnoreResultAction.is_applicable(
                associated_result,
                {},
                {},
                prior_ignore),
            'An ignore comment was already added for this result.')

        self.assertEqual(
            IgnoreResultAction.is_applicable(
                Result('', ''),
                {},
                {},
                prior_ignore),
            'An ignore comment was already added for this result.')

        self.assertEqual(
            IgnoreResultAction.is_applicable(
                Result('', ''),
                {},
                {}
            ),
            'The result is not associated with any source code.'
        )

        with make_temp() as f_a:
            result = Result.from_values('origin', 'msg', f_a, 2)
            self.assertTrue(IgnoreResultAction.is_applicable(result, {}, {}))
            self.assertEqual(
                IgnoreResultAction.is_applicable(
                    result,
                    {},
                    {},
                    prior_ignore),
                'An ignore comment was already added for this result.')

    def test_no_orig(self):
        uut = IgnoreResultAction()
        with make_temp() as f_a:
            file_dict = {
                f_a: ['1\n', '2\n', '3\n']
            }

            file_diff_dict = {}

            # Apply an initial patch
            uut.apply(Result.from_values('origin', 'msg', f_a, 2),
                      file_dict, file_diff_dict, 'c', no_orig=True)
            self.assertFalse(exists(f_a + '.orig'))

    def test_ignore(self):
        uut = IgnoreResultAction()
        with make_temp() as f_a:
            file_dict = {
                f_a: ['1\n', '2\n', '3\n']
            }

            file_diff_dict = {}

            # Apply an initial patch
            uut.apply(Result.from_values('origin', 'msg', f_a, 2),
                      file_dict, file_diff_dict, 'c')
            self.assertEqual(
                file_diff_dict[f_a].modified,
                ['1\n', '2  // Ignore origin\n', '3\n'])
            with open(f_a, 'r') as f:
                self.assertEqual(file_diff_dict[f_a].modified, f.readlines())
            self.assertTrue(exists(f_a + '.orig'))

            # Apply a second patch, old patch has to stay!
            uut.apply(Result.from_values('else', 'msg', f_a, 1),
                      file_dict, file_diff_dict, 'css')
            self.assertEqual(
                file_diff_dict[f_a].modified,
                ['1  /* Ignore else */\n', '2  // Ignore origin\n', '3\n'])
            with open(f_a, 'r') as f:
                self.assertEqual(file_diff_dict[f_a].modified, f.readlines())

            import logging
            logger = logging.getLogger()

            with unittest.mock.patch('subprocess.call'):
                with self.assertLogs(logger, 'WARNING') as log:
                    uut.apply(Result.from_values('else', 'msg', f_a, 1),
                              file_dict, file_diff_dict, 'dothraki')

                    self.assertEqual(1, len(log.output))
                    self.assertIn(
                        'coala does not support Ignore in "dothraki".',
                        log.output[0]
                    )
