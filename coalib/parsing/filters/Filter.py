from functools import wraps


def filter(filter_function):
    def filter_section_bears(bears, args):
        return {section:
                tuple(bear for bear in bears[section]
                      if filter_function(bear, args))
                for section in bears}

    @wraps(filter_function)
    def filter_wrapper(section_to_bears_dict, args):
        args = {arg.lower() for arg in args}
        local_bears, global_bears = section_to_bears_dict
        local_bears = filter_section_bears(local_bears, args)
        global_bears = filter_section_bears(global_bears, args)
        return local_bears, global_bears

    return filter_wrapper
