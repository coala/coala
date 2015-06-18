import os
import signal
import platform


def interrupt_processes(pid):
    if platform.system() == "Windows":  # pragma: no cover
        os.kill(pid, signal.CTRL_BREAK_EVENT)
    else:
        os.kill(pid, signal.SIGINT)
