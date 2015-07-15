import platform

from coalib.parsing.StringProcessing import escape


def escape_path_argument(path, os=platform.system()):
    """
    Makes a raw path ready for using as parameter in a shell command (escapes
    illegal characters, surrounds with quotes etc.).

    :param path: The path to make ready for shell.
    :param os:   The shell platform to escape the path argument for. Possible
                 values are "Windows" and "Linux" (others will be ignored and
                 return the given path without modification).
    :return:     The escaped path argument.
    """
    if os == "Windows":
        # If a quote (") occurs in path (which is illegal for NTFS file
        # systems, but maybe for others), escape it by preceding it with
        # a caret (^).
        return '"' + escape(path, '"', '^') + '"'
    elif os == "Linux":
        return escape(path, " ")
    else:
        # Any other non-supported system doesn't get a path escape.
        return path
