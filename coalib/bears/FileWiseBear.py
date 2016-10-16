from coalib.bears.Bear import Bear
from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.settings.FunctionMetadata import FunctionMetadata


class FileWiseBear(Bear):
    """
    A FileWiseBear is a Bear that analyzes only one file at once. It therefore
    can not analyze semantical facts over multiple files.

    This has the advantage that it can be highly parallelized. In addition,
    the results from multiple bears for one file can be shown together for that
    file, which is better to grasp for the user. coala takes care of all that.

    Examples for LocalBear's could be:

    -   A SpaceConsistencyBear that checks every line for trailing whitespaces,
        tabs, etc.
    -   A VariableNameBear that checks variable names and constant names for
        certain conditions
    """

    def __init__(self,
                 file_set,  # A set of file_proxies
                 section,
                 message_queue,
                 timeout=0):
        Bear.__init__(self, section, message_queue, timeout)
        self.file_set = file_set

        try:
            self.kwargs = self.get_metadata().create_params_from_section(
                section)
        except ValueError as err:
            self.warn("The bear {} cannot be executed.".format(
                self.name), str(err))

    @staticmethod
    def kind():
        return BEAR_KIND.FILEWISE

    def execute_task(self, task, kwargs):
        """
        This method is responsible for getting results from the
        analysis routines.
        """
        return list(self.analyze(task, **kwargs))

    def analyze(self,
                file_proxy,
                *args,
                dependency_results=None,
                **kwargs):
        """
        Handles the given file.

        :param file_proxy:     Object containing filename and contents.
        :return:               A list of Result
        """
        raise NotImplementedError("This function has to be implemented for a "
                                  "runnable bear.")

    def generate_tasks(self, kwargs={}):
        """
        This method is responsible for providing the files and arguments for
        the tasks the bear needs to perform.
        """
        self.kwargs.update(kwargs)
        return ((file, self.kwargs) for file in self.file_set)

    @classmethod
    def get_metadata(cls):
        return FunctionMetadata.from_function(
            cls.run,
            omit={"self", "file_proxy", "dependency_results"})