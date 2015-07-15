from coalib.results.result_actions.ResultAction import ResultAction


class PrintDebugMessageAction(ResultAction):
    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Show debug message to the console.
        """
        print(result.debug_msg)
        return file_diff_dict
