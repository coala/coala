from coalib.bearlib.aspects import Root, Taste


@Root.subaspect
class Spelling:
    """
    How words should be written.
    """
    class docs:
        example = """
        'Tihs si surly som incoreclt speling.
        `Coala` is always written with a lowercase `c`.
        """
        example_language = 'reStructuredText'
        importance_reason = """
        Words should always be written as they are supposed to be;
        standardisation facilitates communication.
        """
        fix_suggestions = """
        Use the correct spelling for the misspelled words.
        """


@Spelling.subaspect
class DictionarySpelling:
    """
    Valid language's words spelling.
    """
    class docs:
        example = """
        This is toatly wonrg.
        """
        example_language = 'reStructuredText'
        importance_reason = """
        Good spelling facilitates communication and avoids confusion. By
        following the same rules for spelling words, we can all understand
        the text we read. Poor spelling distracts the reader and they lose
        focus.
        """
        fix_suggestions = """
        You can use a spell-checker to fix this for you or just ensure
        yourself that things are well written.
        """


@Spelling.subaspect
class OrgSpecificWordSpelling:
    """
    Organisations like coala specified words' spelling.
    """
    class docs:
        example = """
        `Coala` is always written with a lower case c, also at the beginning
        of the sentence.
        """
        example_language = 'reStructuredText'
        importance_reason = """
        There are words you want to be written as you want, like your
        organisation's name.
        """
        fix_suggestions = """
        Simply make sure those words match with what is provided by the
        organisation.
        """
    specific_word = Taste[list](
        'Represents the regex of the specific word to check.',
        (('c[o|O][a|A][l|L][a|A]',), ), default=list())
