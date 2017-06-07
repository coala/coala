from coalib.bearlib.aspects import Root


@Root.subaspect
class Spelling:
    """
    This aspect describes spelling of your source code.
    """


@Spelling.subaspect
class aspectsYEAH:
    """
    This aspect dictates that the term ``aspects`` and ``aspect`` must have
    all letters in lower case and the term ``aspectsYEAH`` must match the
    exact expression.
    """
    class docs:
        example = """
        Valid Cases:
        # aspects are the mother of all futures of coala
        # ``aspectsYEAH`` project is simply awesome
        Invalid Cases:
        # Aspects are the mother of all futures of coala
        # ``aspectsyeah`` project is simply awesome
        """
        example_language = 'All'
        importance_reason = """
        The concepts of aspects in coala are too fundamental to contain any
        upper-case letters.
        """
        fix_suggestions = """
        ``aspects`` or ``aspect`` are always written with all lower-case
        letters or the term ``aspectsYEAH`` must match the exact expression.
        """


@Spelling.subaspect
class coalaCorrect:
    """
    This aspect dictates that the term ``coala`` must always be written with
    with a lowercase `c`.
    """
    class docs:
        example = """
        Valid Cases:
        # ``coala`` is so much fun!
        # ``coalA`` hmm... not exactly ``coala`` but it is fine ;)
        Invalid Cases:
        # ``Coala`` hmm... this is wrong :(
        # ``CoalA``... @cobot please do something about this :(
        """
        example_language = 'All'
        importance_reason = """
        We like it this way ;).
        """
        fix_suggestions = """
        Always write ``coala`` with a lower case ``c``.
        """
