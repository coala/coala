"""
Module description.

Some more foobar-like text.
"""


def foobar_explosion(radius):
    """
    A nice and neat way of documenting code.
    :param radius: The explosion radius. """
    def get_55():
        """A function that returns 55."""
        return 55

    return get_55() * radius


"""
Docstring with layouted text.

    layouts inside docs are preserved.
this is intended.
"""


""" Docstring inline with triple quotes.
    Continues here. """


def best_docstring(param1, param2):
    """
    This is the best docstring ever!

    :param param1:
        Very Very Long Parameter description.
    :param param2:
        Short Param description.

    :return: Long Return Description That Makes No Sense And Will
             Cut to the Next Line.
    """
    return None


def docstring_find(filename):
    """
    This is dummy docstring find function.

    :param filename:
        contains filename
    :raises FileNotFoundError:
        raised when the given file name was not found

    :return: returns all possible docstrings in a file
    """


def foobar_triangle(side_A, side_B, side_C):
    """
    This returns perimeter of a triangle.   

    :param side_A:
        length of side_A       
    :param side_B:
        length of side_B    
    :param side_C:
        length of side_C  

    :return: returns perimeter
    """
    return side_A + side_B + side_C

    # This example of triple quote string literal is ignored.
    triple_quote_string_literal_test = """
This is a triple quoted string and is not a valid docstring.
"""
