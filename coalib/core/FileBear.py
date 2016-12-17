from coalib.core.Bear import Bear


class FileBear(Bear):
    """
    This bear base class parallelizes tasks for each file given.
    """

    def __init__(self, section, file_dict):
        """
        :param section:
            The section object where bear settings are contained. A section
            passed here is considered to be immutable.
        :param file_dict:
            A dictionary containing filenames to process as keys and their
            contents (line-split with trailing return characters) as values.
        """
        Bear.__init__(section, file_dict)

        # May raise RuntimeError so bear doesn't get executed on invalid params
        self._kwargs = get_kwargs_for_function(self.analyze, section)

    def generate_tasks(self):
        return (((filename, file), self._kwargs)
                for filename, file in self.file_dict)
