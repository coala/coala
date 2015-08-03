import os
import signal
import platform

if platform.system() == "Windows":
    from ctypes import windll
    from time import sleep
    CTRL_C_EVENT = 0x0


def interrupt_process(pid):
    """
    Interrupt a process by its pid.

    Note for Windows users:
    Be sure that the pid you pass shares the same process group as your program
    that calls this function. If they don't share the same process group, this
    call blocks for 10 seconds to be sure that this is the case.

    :param pid: The pid of the process to interrupt.
    """
    if platform.system() == "Windows":  # pragma: no cover
        try:
            windll.kernel32.GenerateConsoleCtrlEvent(CTRL_C_EVENT, pid)
            sleep(10)
        except KeyboardInterrupt:
            pass
    else:
        os.kill(pid, signal.SIGINT)
