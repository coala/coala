import inspect
import os
import platform
import sys
from coalib.misc.Decorators import arguments_to_lists, yield_once
from coalib.misc.ContextManagers import suppress_stdout


def _import_module(file_path):
    if not os.path.exists(file_path):
        raise ImportError

    module_name = os.path.splitext(os.path.basename(file_path))[0]
    module_dir = os.path.dirname(file_path)

    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

    # Ugly inconsistency: Python will insist on correctly cased module names
    # independent of whether the OS is case-sensitive or not.
    # We want all cases to match though.
    if platform.system() == 'Windows':  # pragma: nocover
        for cased_file_path in os.listdir(module_dir):
            cased_module_name = os.path.splitext(cased_file_path)[0]
            if cased_module_name.lower() == module_name.lower():
                module_name = cased_module_name
                break

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
        source = inspect.getfile(obj)
        if (platform.system() == 'Windows' and
                source.lower() == file_path.lower() or
                source == file_path):
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
    :raises Exception: Any exception that is thrown in module code or an
                       ImportError if paths are erroneous.
    """
    if (file_paths == [] or
            (names == [] and
             types == [] and
             supers == [] and
             attributes == [])):
        raise StopIteration

    for file_path in file_paths:
        module = _import_module(file_path)
        for obj_name, obj in inspect.getmembers(module):
            if ((names == [] or obj_name in names) and
                    (types == [] or isinstance(obj, tuple(types))) and
                    (supers == [] or _is_subclass(obj, supers)) and
                    (attributes == [] or _has_all(obj, attributes)) and
                    (local[0] is False or _is_defined_in(obj, file_path))):
                yield obj


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
    :raises Exception: Any exception that is thrown in module code or an
                       ImportError if paths are erroneous.
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
    :raises Exception: Any exception that is thrown in module code or an
                       ImportError if paths are erroneous.
    """
    return list(iimport_objects(file_paths, names, types, supers, attributes,
                                local, verbose))
