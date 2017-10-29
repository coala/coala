from inspect import cleandoc

from coala_utils.decorators import (
    enforce_signature, generate_consistency_check)


@generate_consistency_check('definition', 'example', 'example_language',
                            'importance_reason', 'fix_suggestions')
class Documentation:
    """
    This class contains documentation about an aspectclass.
    The documentation is consistent if all members are given:

    >>> Documentation('defined').check_consistency()
    False
    >>> Documentation('definition', 'example',
    ...               'example_language', 'importance',
    ...               'fix').check_consistency()
    True
    """

    @enforce_signature
    def __init__(self, definition: str='', example: str='',
                 example_language: str='', importance_reason: str='',
                 fix_suggestions: str=''):
        """
        Contains documentation for an aspectclass.

        :param definition:        What is this about?
        :param example:           An example in a well known language.
        :param example_language:  The language used for the example.
        :param importance_reason: A reason why this aspect is important.
        :param fix_suggestions:   Suggestions on how this can be fixed.
        """
        self.definition = cleandoc(definition)
        self.example = cleandoc(example)
        self.example_language = cleandoc(example_language)
        self.importance_reason = cleandoc(importance_reason)
        self.fix_suggestions = cleandoc(fix_suggestions)
