import inspect
import os
import sys
from coalib.misc.Decorators import cached_iterator, listify_arguments
from coalib.misc.ContextManagers import suppress_stdout


def _import_module(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    module_dir = os.path.dirname(file_path)

    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

    return __import__(module_name)


def _is_subclass_of_one_of(test_class, superclasses):
    for superclass in superclasses:
        if issubclass(test_class, superclass):
            return True
    return False


def _has_all_attributes(obj, attribute_names):
    for attribute_name in attribute_names:
        if not hasattr(obj, attribute_name):
            return False
    return True

@listify_arguments
@cached_iterator
def _iimport_object(file_paths, names=None, types=None, supers=None, attributes=None, local=True):
    """
    Import all objects from the all given modules that fulfill the requirements
    :param file_paths: File path or list of paths from which objects will eb imported
    :param names: String or list of strings: Objects will be imported that have one of the given names
    :param types: Type or list of types: Object will be imported that are an instance of at least one given type
    :param supers: Class or list of classes: Objects will be imported that are a subclass of at least one
    :param attributes: String or List of: Objects will be imported that contain all given attributes
    :param local: If True, only objects will be imported that get defined in the file they appear in.
    :return: iterator that yields all python objects that match above requirements
    """
    for file_path in file_paths:
        module = _import_module(file_path)
        for obj_name, obj in inspect.getmembers(module):
            if (names == [] or obj_name in names) and \
                    (types == [] or isinstance(obj, tuple(types))) and \
                    (supers == [] or _is_subclass_of_one_of(obj, supers)) and \
                    (attributes == [] or _has_all_attributes(obj, attributes)) and \
                    (local is False or inspect.getfile(obj) == inspect.getfile(module)):
                yield obj


def iimport_object(file_paths, names=None, types=None, supers=None, attributes=None, local=True, verbose=False):
    """
    Import all objects from the all given modules that fulfill the requirements
    :param file_paths: File path or list of paths from which objects will eb imported
    :param names: String or list of strings: Objects will be imported that have one of the given names
    :param types: Type or list of types: Object will be imported that are of an instance at least one given type
    :param supers: Class or list of classes: Objects will be imported that are a subclass of at least one
    :param attributes: String or List of: Objects will be imported that contain all given attributes
    :param local: If True, only objects will be imported that get defined in the file they appear in.
    :param verbose: whether ot not to allow module code of imported modules to print to sys.stdout
    :return: iterator that yields all python objects that match above requirements
    """
    if not verbose:
        with suppress_stdout():
            for obj in _iimport_object(file_paths, names, types, supers, attributes, local):
                yield obj
    else:
        for obj in _iimport_object(file_paths, names, types, supers, attributes, local):
                yield obj

def import_object(file_paths, names=None, types=None, supers=None, attributes=None, local=True, verbose=False):
    """
    Import all objects from the all given modules that fulfill the requirements
    :param file_paths: File path or list of paths from which objects will eb imported
    :param names: String or list of strings: Objects will be imported that have one of the given names
    :param types: Type or list of types: Object will be imported that are an instance of at least one given type
    :param supers: Class or list of classes: Objects will be imported that are a subclass of at least one
    :param attributes: String or List of: Objects will be imported that contain all given attributes
    :param local: If True, only objects will be imported that get defined in the file they appear in.
    :param verbose: whether ot not to allow module code of imported modules to print to sys.stdout
    :return: list of all python objects that match above requirements
    """
    return list(iimport_object(file_paths, names, types, supers, attributes, local, verbose))