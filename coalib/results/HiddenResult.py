from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.bearlib.aspects import aspectbase
from coala_utils.decorators import (
    enforce_signature, generate_ordering, generate_repr)


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

    @enforce_signature
    def __init__(self,
                 origin,
                 contents,
                 message: str='',
                 affected_code: (tuple, list)=(),
                 severity: int=RESULT_SEVERITY.NORMAL,
                 additional_info: str='',
                 debug_msg='',
                 diffs: (dict, None)=None,
                 confidence: int=100,
                 aspect: (aspectbase, None)=None,
                 message_arguments: dict={},
                 applied_actions: dict={}):
        """
        Creates a new HiddenResult. The contents can be accessed with
        obj.contents later.

        :param origin:
            The originating bear.
        :param contents:
            Any object to send additional data (arbitrary python objects)
            besides a message to the dependent bear. The data has to
            be picklable.
        :param affected_code:
            A tuple of ``SourceRange`` objects pointing to related positions in
            the source code.
        :param severity:
            Severity of this result.
        :param additional_info:
            A long description holding additional information about the issue
            and/or how to fix it. You can use this like a manual entry for a
            category of issues.
        :param debug_msg:
            A message which may help the user find out why this result was
            yielded.
        :param diffs:
            A dictionary with filename as key and ``Diff`` object
            associated with it as value.
        :param confidence:
            A number between 0 and 100 describing the likelihood of this result
            being a real issue.
        :param aspect:
            An aspectclass instance which this result is associated to.
            Note that this should be a leaf of the aspect tree!
            (If you have a node, spend some time figuring out which of
            the leafs exactly your result belongs to.)
        :param message_arguments:
            Arguments to be provided to the base message.
        :param applied_actions:
            A dictionary that contains the result, file_dict, file_diff_dict and
            the section for an action.
        """
        Result.__init__(self,
                        origin,
                        message,
                        affected_code,
                        severity,
                        additional_info,
                        debug_msg,
                        diffs,
                        confidence,
                        aspect,
                        message_arguments,
                        applied_actions)

        self.contents = contents
