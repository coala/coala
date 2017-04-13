import re

from inspect import getmembers, signature

from coala_utils.decorators import generate_repr

from .base import aspectbase
from .docs import Documentation
from .taste import Taste


class aspectclass(type):
    """
    Metaclass for aspectclasses.

    Root aspectclass is :class:`coalib.bearlib.aspects.Root`.
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
        :class:`coalib.bearlib.aspects.Taste` instances.
        """
        if cls.parent:
            return dict(cls.parent.tastes, **cls._tastes)

        return dict(cls._tastes)

    def subaspect(cls, subcls):
        """
        The sub-aspectclass decorator.

        See :class:`coalib.bearlib.aspects.Root` for description
        and usage.
        """
        aspectname = subcls.__name__

        docs = getattr(subcls, 'docs', None)
        aspectdocs = Documentation(subcls.__doc__, **{
            attr: getattr(docs, attr, '') for attr in
            list(signature(Documentation).parameters.keys())[1:]})

        # search for tastes in the sub-aspectclass
        subtastes = {}
        for name, member in getmembers(subcls):
            if isinstance(member, Taste):
                # tell the taste its own name
                member.name = name
                subtastes[name] = member

        class Sub(subcls, aspectbase, metaclass=aspectclass):
            __module__ = subcls.__module__

            parent = cls

            docs = aspectdocs
            _tastes = subtastes

        members = sorted(Sub.tastes)
        if members:
            Sub = generate_repr(*members)(Sub)

        Sub.__name__ = aspectname
        Sub.__qualname__ = '%s.%s' % (cls.__qualname__, aspectname)
        cls.subaspects[aspectname] = Sub
        setattr(cls, aspectname, Sub)
        return Sub

    def __repr__(cls):
        return '<%s %s>' % (type(cls).__name__, repr(cls.__qualname__))


class aspectTypeError(TypeError):
    """
    This error is raised when an object is not an ``aspectclass`` or an
    instance of ``aspectclass``
    """

    def __init__(self, item):
        self.item = item
        message = ('{} is not an aspectclass or an instance of an '
                   'aspectclass'.format(repr(self.item)))
        super().__init__(message)


def isaspect(item):
    """
    This function checks whether or not an object is an ``aspectclass`` or an
    instance of ``aspectclass``
    """
    return isinstance(item, (aspectclass, aspectbase))


def assert_aspect(item):
    """
    This function raises ``aspectTypeError`` when an object is not an
    ``aspectclass`` or an instance of ``aspectclass``
    """
    if not isaspect(item):
        raise aspectTypeError(item)
    return item


def issubaspect(subaspect, aspect):
    """
    This function checks whether or not ``subaspect`` is a subaspect of
    ``aspect``.
    """
    subaspect = assert_aspect(subaspect)
    aspect = assert_aspect(aspect)
    aspect_qualname = (aspect.__qualname__ if isinstance(
                    aspect, aspectclass) else type(aspect).__qualname__)
    subaspect_qualname = (subaspect.__qualname__ if isinstance(
                    subaspect, aspectclass) else type(subaspect).__qualname__)
    return re.match(aspect_qualname+'(\.|$)', subaspect_qualname) is not None
