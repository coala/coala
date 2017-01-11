import logging

from coalib.bears.Bear import Bear
from coalib.bears.BEAR_KIND import BEAR_KIND


class GlobalBear(Bear):
    """
    A GlobalBear is able to analyze semantic facts across several file.

    The results of a GlobalBear will be presented grouped by the origin Bear.
    Therefore Results spanning above multiple files are allowed and will be
    handled right.

    If you only look at one file at once anyway a LocalBear is better for your
    needs. (And better for performance and usability for both user and
    developer.)
    """

    def __init__(self, section, file_dict):
        logging.warning('coalib.bears.GlobalBear is deprecated, please use '
                        'coalib.core.ProjectBear instead.')

        Bear.__init__(self, section, file_dict)

    @staticmethod
    def kind():
        return BEAR_KIND.GLOBAL

    def run(self,
            *args,
            dependency_results=None,
            **kwargs):
        """
        Handles all files in file_dict.

        :return: A list of Result type.
        """
        raise NotImplementedError(
            'This function has to be implemented for a runnable bear.')
