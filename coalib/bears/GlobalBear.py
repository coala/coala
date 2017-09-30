from coalib.bears.Bear import Bear
from coalib.bears.BEAR_KIND import BEAR_KIND


class GlobalBear(Bear):
    """
    A GlobalBear analyzes semantic facts across several files.

    The results of a GlobalBear will be presented grouped by the origin Bear.
    Therefore Results spanning across multiple files are allowed and will be
    handled correctly.

    If you are inspecting a single file at a time, you should consider
    using a LocalBear.
    """

    def __init__(self,
                 file_dict,
                 section,
                 message_queue,
                 timeout=0):
        """
        Constructs a new GlobalBear.

        :param file_dict: The dictionary of {filename: file contents}.

        See :class:`coalib.bears.Bear` for other parameters.
        """
        Bear.__init__(self, section, message_queue, timeout)
        self.file_dict = file_dict

    @staticmethod
    def kind():
        return BEAR_KIND.GLOBAL

    def run(self,
            *args,
            dependency_results=None,
            **kwargs):
        """
        Handles all files in file_dict.

        :param dependency_results: The dictionary of {bear name:
                                   result list}.
        :return: A list of Result type.

        See :class:`coalib.bears.Bear` for `run` method description.
        """
        raise NotImplementedError(
            'This function has to be implemented for a runnable bear.')
