from abc import ABCMeta


class LinterClass(metaclass=ABCMeta):
    """
    Every ``linter`` is also a subclass of the ``LinterClass`` class.
    """
