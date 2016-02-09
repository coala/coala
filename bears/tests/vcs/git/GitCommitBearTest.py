from queue import Queue
from tempfile import mkdtemp
import os
import platform
import stat
import shutil
import unittest

from coalib.misc.Shell import run_shell_command
from coalib.settings.Section import Section
from bears.vcs.git.GitCommitBear import GitCommitBear
from bears.tests.BearTestHelper import generate_skip_decorator


@generate_skip_decorator(GitCommitBear)
class GitCommitBearTest(unittest.TestCase):

    @staticmethod
    def run_git_command(*args, stdin=None):
        run_shell_command(" ".join(("git",) + args), stdin)

    @staticmethod
    def git_commit(msg):
        # Use stdin mode from git, since -m on Windows cmd does not support
        # multiline messages.
        GitCommitBearTest.run_git_command("commit",
                                          "--allow-empty",
                                          "--allow-empty-message",
                                          "--file=-",
                                          stdin=msg)

    def run_uut(self, *args, **kwargs):
        """
        Runs the unit-under-test (via `self.uut.run()`) and collects the
        messages of the yielded results as a list.

        :param args:   Positional arguments to forward to the run function.
        :param kwargs: Keyword arguments to forward to the run function.
        :return:       A list of the message strings.
        """
        return list(result.message for result in self.uut.run(*args, **kwargs))

    def setUp(self):
        self.msg_queue = Queue()
        self.uut = GitCommitBear(None, Section(""), self.msg_queue)

        self._old_cwd = os.getcwd()
        self.gitdir = mkdtemp()
        os.chdir(self.gitdir)
        self.run_git_command("init")
        self.run_git_command("config", "user.email coala@coala-analyzer.io")
        self.run_git_command("config", "user.name coala")

    @staticmethod
    def _windows_rmtree_remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def tearDown(self):
        os.chdir(self._old_cwd)
        if platform.system() == "Windows":
            onerror = self._windows_rmtree_remove_readonly
        else:
            onerror = None
        shutil.rmtree(self.gitdir, onerror=onerror)

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertEqual(GitCommitBear.check_prerequisites(),
                             "git is not installed.")

            shutil.which = lambda *args, **kwargs: "path/to/git"
            self.assertTrue(GitCommitBear.check_prerequisites())
        finally:
            shutil.which = _shutil_which

    def test_git_failure(self):
        # In this case use a reference to a non-existing commit, so just try
        # to log all commits on a newly created repository.
        self.assertEqual(self.run_uut(), [])

        git_error = self.msg_queue.get().message
        self.assertEqual(git_error[:4], "git:")

        self.assertTrue(self.msg_queue.empty())

    def test_empty_message(self):
        self.git_commit("")

        self.assertEqual(self.run_uut(),
                         ["HEAD commit has no message."])
        self.assertTrue(self.msg_queue.empty())

        self.assertEqual(self.run_uut(allow_empty_commit_message=True),
                         [])
        self.assertTrue(self.msg_queue.empty())

    def test_shortlog_checks(self):
        self.git_commit("Commits messages that nearly exceeds default limit")

        self.assertEqual(self.run_uut(), [])
        self.assertTrue(self.msg_queue.empty())

        self.assertEqual(self.run_uut(shortlog_length=17),
                         ["Shortlog of HEAD commit is too long."])
        self.assertTrue(self.msg_queue.empty())

        self.git_commit("A shortlog that is too long is not good for history")
        self.assertEqual(self.run_uut(),
                         ["Shortlog of HEAD commit is too long."])
        self.assertTrue(self.msg_queue.empty())

    def test_body_checks(self):
        self.git_commit(
            "Commits message with a body\n\n"
            "nearly exceeding the default length of a body, but not quite. "
            "haaaaaaands")

        self.assertEqual(self.run_uut(), [])
        self.assertTrue(self.msg_queue.empty())

        self.git_commit("Shortlog only")

        self.assertEqual(self.run_uut(), [])
        self.assertTrue(self.msg_queue.empty())

        # Force a body.
        self.git_commit("Shortlog only ...")
        self.assertEqual(self.run_uut(force_body=True),
                         ["No commit message body at HEAD."])
        self.assertTrue(self.msg_queue.empty())

        # Miss a newline between shortlog and body.
        self.git_commit("Shortlog\nOops, body too early")
        self.assertEqual(self.run_uut(),
                         ["No newline between shortlog and body at HEAD."])
        self.assertTrue(self.msg_queue.empty())

        # And now too long lines.
        self.git_commit("Shortlog\n\n"
                        "This line is ok.\n"
                        "This line is by far too long (in this case).\n"
                        "This one too, blablablablablablablablabla.")
        self.assertEqual(self.run_uut(body_line_length=41),
                         ["Body of HEAD commit contains too long lines."])
        self.assertTrue(self.msg_queue.empty())


if __name__ == '__main__':
    unittest.main(verbosity=2)
