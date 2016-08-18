from coalib.bears.Bear import Bear
from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.settings.FunctionMetadata import FunctionMetadata


class ProjectWideBear(Bear):
    """
    A ProjectWideBear is a Bear that analyzes all files at once. This has the
    advantage of drawing advanced semantic analysis that give results that are
    applicable to the whole codebase.
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
        return BEAR_KIND.PROJECTWIDE

    def execute_task(self, task, kwargs):
        """
        This method is responsible for getting results from the
        analysis routines.
        """
        return list(self.analyze(task, **kwargs))

    def analyze(self,
                file_set,
                *args,
                dependency_results=None,
                **kwargs):
        """
        Handles the given file.

        :param file_set:       A set of FileProxy objects.
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
        return [self.file_set, self.kwargs]

    @classmethod
    def get_metadata(cls):
        return FunctionMetadata.from_function(
            cls.run,
            omit={"self", "file_proxy", "dependency_results"})