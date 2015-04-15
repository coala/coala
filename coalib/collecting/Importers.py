import inspect
import os
import sys
from coalib.misc.Decorators import arguments_to_lists, yield_once
from coalib.misc.ContextManagers import suppress_stdout


def _import_module(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    module_dir = os.path.dirname(file_path)

    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

    return __import__(module_name)


def _is_subclass(test_class, superclasses):
    for superclass in superclasses:
        try:
            if issubclass(test_class, superclass):
                return True
        except TypeError:
            pass
    return False


def _has_all(obj, attribute_names):
    for attribute_name in attribute_names:
        if not hasattr(obj, attribute_name):
            return False
    return True


def _is_defined_in(obj, file_path):
    try:
        if inspect.getfile(obj) == file_path:
            return True
    except TypeError:  # Bool values and others
        pass
    return False


@arguments_to_lists
@yield_once
def _iimport_objects(file_paths, names, types, supers, attributes, local):
    """
    Import all objects from the given modules that fulfill the requirements

    :param file_paths: File path(s) from which objects will be imported
    :param names:      Name(s) an objects need to have one of
    :param types:      Type(s) an objects need to be out of
    :param supers:     Class(es) objects need to be a subclass of
    :param attributes: Attribute(s) an object needs to (all) have
    :param local:      if True: Objects need to be defined in the file they
                       appear in to be collected
    :return:           iterator that yields all matching python objects
    """
    if file_paths == [] or \
            (names == [] and
             types == [] and
             supers == [] and
             attributes == []):
        raise StopIteration

    for file_path in file_paths:
        try:
            module = _import_module(file_path)
            for obj_name, obj in inspect.getmembers(module):
                if (names == [] or obj_name in names) and \
                        (types == [] or isinstance(obj, tuple(types))) and \
                        (supers == [] or _is_subclass(obj, supers)) and \
                        (attributes == [] or _has_all(obj, attributes)) and \
                        (local[0] is False or _is_defined_in(obj, file_path)):
                    yield obj
        except ImportError:
            pass


def iimport_objects(file_paths, names=None, types=None, supers=None,
                    attributes=None, local=False, verbose=False):
    """
    Import all objects from the given modules that fulfill the requirements

    :param file_paths: File path(s) from which objects will be imported
    :param names:      Name(s) an objects need to have one of
    :param types:      Type(s) an objects need to be out of
    :param supers:     Class(es) objects need to be a subclass of
    :param attributes: Attribute(s) an object needs to (all) have
    :param local:      if True: Objects need to be defined in the file they
                       appear in to be collected
    :return:           iterator that yields all matching python objects
    """
    if not verbose:
        with suppress_stdout():
            for obj in _iimport_objects(file_paths, names, types, supers,
                                        attributes, local):
                yield obj
    else:
        for obj in _iimport_objects(file_paths, names, types, supers,
                                    attributes, local):
            yield obj


def import_objects(file_paths, names=None, types=None, supers=None,
                   attributes=None, local=False, verbose=False):
    """
    Import all objects from the given modules that fulfill the requirements

    :param file_paths: File path(s) from which objects will be imported
    :param names:      Name(s) an objects need to have one of
    :param types:      Type(s) an objects need to be out of
    :param supers:     Class(es) objects need to be a subclass of
    :param attributes: Attribute(s) an object needs to (all) have
    :param local:      if True: Objects need to be defined in the file they
                       appear in to be collected
    :return:           list of all matching python objects
    """
    return list(iimport_objects(file_paths, names, types, supers, attributes,
                                local, verbose))
