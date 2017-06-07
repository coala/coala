"""
Replacement for ``multiprocessing`` library in coala's debug mode.
"""

import sys
import queue
from functools import partial

from coalib.processes.communication.LogMessage import LogMessage

__all__ = ['Manager', 'Process', 'Queue']


class Manager:
    """
    A debug replacement for ``multiprocessing.Manager``, just offering
    ``builtins.dict`` as ``.dict`` member.
    """

    def __init__(self):
        """
        Just add ``dict`` as instance member.
        """
        self.dict = dict


class Process(partial):
    """
    A debug replacement for ``multiprocessing.Process``, running the callable
    target without any process parallelization or threading.
    """

    def __new__(cls, target, kwargs):
        """
        Just pass the arguments to underlying ``functools.partial``.
        """
        return partial.__new__(cls, target, **kwargs)

    def start(self):
        """
        Just call the underlying ``functools.partial`` instaed of any thread
        or parallel process creation.
        """
        return self()


class Queue(queue.Queue):
    """
    A debug replacement for ``multiprocessing.Queue``, directly processing
    any incoming :class:`coalib.processes.communication.LogMessage.LogMessage`
    instances (if the queue was instantiated from a function with a local
    ``log_printer``).
    """

    def __init__(self):
        """
        Gets local ``log_printer`` from function that created this instance.
        """
        super().__init__()
        # same kind of HACK as can be found in collections.namedtuple for
        # setting .__module__ of created classes
        self.log_printer = sys._getframe(1).f_locals.get('log_printer')

    def put(self, item):
        """
        Add `item` to queue.

        Except `item` is an instance of
        :class:`coalib.processes.communication.LogMessage.LogMessage` and
        there is a ``self.log_printer``. Then `item` is just sent to logger
        instead.
        """
        if self.log_printer is not None and isinstance(item, LogMessage):
            self.log_printer.log_message(item)
        else:
            super().put(item)
