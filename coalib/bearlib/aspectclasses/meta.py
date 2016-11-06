from inspect import getmembers

from .base import aspectbase
from .docs import Documentation
from .taste import Taste


class aspectclass(type):
    """Metaclass for class-based aspects.

    Root aspectclass is :class:`coalib.bearlib.aspectclasses.Root`.
    """
    def __init__(cls, clsname, bases, clsattrs):
        """Initialize some class attributes.
        """
        cls.subaspects = {}

    @property
    def docs(cls):
        return cls.aspect.docs

    @property
    def tastes(cls):
        """Get a dictionary of all taste names mapped to their
        :class:`coalib.bearlib.aspectclasses.Taste` instances.
        """
        result = dict(cls._tastes)
        if cls.parent:
            result.update(cls.parent.tastes)
        return result

    def subaspect(cls, subcls):
        """The sub-aspectclass decorator.

        See :class:`coalib.bearlib.aspectclasses.Root` for description
        and usage.
        """
        aspectname = subcls.__name__

        docs = getattr(subcls, 'docs', None)
        docs = Documentation(subcls.__doc__.strip(), **{
            attr: getattr(docs, attr, '').strip() for attr in [
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

            _tastes = subtastes

        Sub.__name__ = aspectname
        Sub.__qualname__ = '%s.%s' % (cls.__qualname__, aspectname)
        cls.subaspects[aspectname] = Sub
        setattr(cls, aspectname, Sub)
        return Sub

    def __repr__(cls):
        return "<%s %s>" % (type(cls).__name__, repr(cls.__qualname__))
