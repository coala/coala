from coalib.bears.LocalBear import LocalBear


class RaiseTestBear(LocalBear):
    """
    Just raises an exception (default ``RuntimeError``) when run.
    """
    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()

    def run(self, filename, file,
            cls: str = 'RuntimeError',
            msg: str = "That's all the RaiseTestBear can do."):
        """
        Just raise ``cls``.
        """
        cls = eval(cls)
        raise cls(msg)


class RaiseTestExecuteBear(LocalBear):
    """
    Just raises an exception (default ``RuntimeError``) in execute.
    """
    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()

    def execute(self, filename, file, debug=False, **kwargs):
        """
        Just raise ``cls``.
        """
        cls = eval(str(self.section['cls']))
        raise cls(self.section['msg'])
