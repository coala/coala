from coalib.results.Result import Result
from coala_utils.decorators import generate_ordering, generate_repr


@generate_repr(('id', hex),
               'origin',
               'message',
               'contents')
@generate_ordering('contents',
                   'origin',
                   'message_base')
class HiddenResult(Result):
    """
    This is a result that is not meant to be shown to the user. It can be used
    to transfer any data from a dependent bear to others.
    """

    def __init__(self, origin, contents):
        """
        Creates a new HiddenResult. The contents can be accessed with
        obj.contents later.

        :param origin:   The originating bear.
        :param contents: Any object that is picklable since it will be
                         transferred across processes.
        """
        Result.__init__(self, origin, '')

        self.contents = contents
