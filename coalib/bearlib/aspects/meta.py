from inspect import getmembers
from itertools import chain

from coala_utils.decorators import generate_ordering, generate_repr

from .base import aspectbase
from .docs import Documentation
from .taste import Taste


class aspectclass(type):
    """
    Metaclass for aspectclasses.

    Root aspectclass is :class:`coalib.bearlib.aspectclasses.Root`.
    """
    def __init__(cls, clsname, bases, clsattrs):
        """
        Initializes the ``.subaspects`` dict on new aspectclasses.
        """
        cls.subaspects = {}

    @property
    def tastes(cls):
        """
        Get a dictionary of all taste names mapped to their
        :class:`coalib.bearlib.aspectclasses.Taste` instances.
        """
        if cls.parent:
            return dict(cls.parent.tastes, **cls._tastes)

        return dict(cls._tastes)

    def subaspect(cls, subcls):
        """
        The sub-aspectclass decorator.

        See :class:`coalib.bearlib.aspectclasses.Root` for description
        and usage.
        """
        aspectname = subcls.__name__

        docs = getattr(subcls, 'docs', None)
        aspectdocs = Documentation(subcls.__doc__, **{
            attr: getattr(docs, attr, '') for attr in [
                'example',
                'example_language',
                'importance_reason',
                'fix_suggestions',
            ]})

        subtastes = {}
        # search for tastes int the sub-aspectclass
        for name, member in getmembers(subcls):
            if isinstance(member, Taste):
                subtastes[name] = member

        class Sub(subcls, aspectbase, metaclass=aspectclass):
            __module__ = subcls.__module__

            parent = cls

            docs = aspectdocs
            _tastes = subtastes

        members = sorted(Sub.tastes)
        if members:
            Sub = generate_repr(*members)(generate_ordering(*members)(Sub))

        Sub.__name__ = aspectname
        Sub.__qualname__ = '%s.%s' % (cls.__qualname__, aspectname)
        cls.subaspects[aspectname] = Sub
        setattr(cls, aspectname, Sub)
        return Sub

    def __repr__(cls):
        return "<%s %s>" % (type(cls).__name__, repr(cls.__qualname__))
