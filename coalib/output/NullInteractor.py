from coalib.output.Interactor import Interactor


class NullInteractor(Interactor):
    """
    This interactor can be used for headless setups, it requires no interaction
    from the user.
    """

    def print_result(self, result, file_dict):
        pass

    def print_results(self, result_list, file_dict):
        pass

    def did_nothing(self):
        pass

    def begin_section(self, section):
        pass

    def acquire_settings(self, settings):
        # We can't get settings here, if bears need them, they better fail.
        pass

    def show_bears(self, bears):
        pass
