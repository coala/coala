"""
Replacement for ``multiprocessing`` library in coala's debug mode.
"""

import logging
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
    instances.
    """

    def __init__(self):
        super().__init__()

    def put(self, item):
        """
        Add `item` to queue.

        Except `item` is an instance of
        :class:`coalib.processes.communication.LogMessage.LogMessage`.
        Then `item` is just sent to logger instead.
        """
        if isinstance(item, LogMessage):
            logging.log(item.log_level, item.message)
        else:
            super().put(item)
