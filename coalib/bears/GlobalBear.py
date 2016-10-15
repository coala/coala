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

    def __init__(self,
                 file_dict,  # filename : file contents
                 section,
                 message_queue,
                 timeout=0):
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

        :return: A list of Result type.
        """
        raise NotImplementedError(
            "This function has to be implemented for a runnable bear.")

    def get_warning_msg(self, *args):
        """
        This method is responsible to generate the warning message
        when a GlobalBear instance fails while executing on a file.

        :param args: The arguments that are to be passed to the bear.
        :return: Returns the appropriate error message

        """
        return "Bear {} failed to run. Take a look at debug messages"
        " (`-V`) for further information.".format(self.name)
