from coalib.core.Bear import Bear


class ProjectBear(Bear):
    """
    This bear base class does not parallelize tasks at all, it runs on the
    whole file base provided.
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
        return ((self.file_dict,), self._kwargs),
