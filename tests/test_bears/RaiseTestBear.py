from coalib.bears.LocalBear import LocalBear


class RaiseTestBear(LocalBear):
    """
    Just raises a ``RuntimeError`` when run.
    """
    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()

    def run(self, filename, file):
        """
        Just raise ``RuntimeError``.
        """
        raise RuntimeError("That's all the RaiseTestBear can do.")
