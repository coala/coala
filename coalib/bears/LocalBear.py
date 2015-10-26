from coalib.bears.Bear import Bear
from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.bears.GlobalBear import GlobalBear
from coalib.settings.FunctionMetadata import FunctionMetadata


class LocalBear(Bear):
    """
    A LocalBear is a Bear that analyzes only one file at once. It therefore can
    not analyze semantical facts over multiple files.

    This has the advantage that it can be highly parrallelized. In addition,
    the results from multiple bears for one file can be shown together for that
    file, which is better to grasp for the user. coala takes care of all that.

    Examples for LocalBear's could be:
    - A SpaceConsistencyBear that checks every line for trailing whitespaces,
      tabs, ...
    - A VariableNameBear that checks variable names and constant names for
      certain conditions
    """

    @staticmethod
    def kind():
        return BEAR_KIND.LOCAL

    def run(self,
            filename,
            file,
            *args,
            dependency_results=None,
            **kwargs):
        """
        Handles the given file.

        :param filename: The filename of the file
        :param file:     The file contents as string array
        :return:         A list of Result
        """
        raise NotImplementedError("This function has to be implemented for a "
                                  "runnable bear.")

    @classmethod
    def get_metadata(cls):
        return FunctionMetadata.from_function(
            cls.run,
            omit={"self", "filename", "file", "dependency_results"}) # asd asd asd asd


def LocalBearDecorator(run_function):
    class Decorated(GlobalBear):
        __name__ = run_function.__name__

        @staticmethod
        def kind():
            return BEAR_KIND.GLOBAL

        def run(self,
                *args,
                **kwargs):
            for filename in self.file_dict:
                for result in run_function(
                        *args,
                        filename=filename,
                        file=self.file_dict[filename],
                        **kwargs):
                    yield result

        @classmethod
        def get_metadata(cls):
            return FunctionMetadata.from_function(
                run_function,
                omit={"self", "filename", "file", "dependency_results"})

    return Decorated
