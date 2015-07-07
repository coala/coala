from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.settings.Setting import typed_list


def get_language_tool_results(file_contents):
    from jpype import startJVM, shutdownJVM, java, getDefaultJVMPath
    startJVM(getDefaultJVMPath())
    langtool = java.org.languagetool.JLanguageTool()
    matches = langtool.check("\n".join(file_contents))
    print(matches)
    shutdownJVM()


class PyLintBear(LocalBear):
    def run(self,
            filename,
            file,
            langtool_disable: typed_list(str)=None,
            langtool_enable: typed_list(str)=None,
            langtool_cli_options: str=""):
        '''
        Checks the code with LanguageTool.

        :param langtool_disable:     Disable the message, report, category or
                                     checker with the given id(s).
        :param langtool_enable:      Enable the message, report, category or
                                     checker with the given id(s).
        :param langtool_cli_options: Any command line options you wish to be
                                     passed to pylint.
        '''
        print(filename)
        get_language_tool_results(file)
