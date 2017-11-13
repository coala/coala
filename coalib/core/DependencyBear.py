from coalib.core.Bear import Bear
from coalib.settings.FunctionMetadata import FunctionMetadata


class DependencyBear(Bear):
    """
    This bear base class parallelizes tasks for each dependency result.

    You can specify dependency bears with the ``BEAR_DEPS`` field.
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
        Bear.__init__(self, section, file_dict)

        self._kwargs = self.get_metadata().create_params_from_section(section)

    def execute_task(self, args, kwargs):
        # To optimize performance and memory usage, we use kwargs from this
        # class instance instead of passing the same settings thousand times in
        # the tasks themselves.
        return Bear.execute_task(self, args, self._kwargs)

    @classmethod
    def get_metadata(cls):
        """
        :return:
            Metadata for the ``analyze`` function extracted from its signature.
            Excludes parameters ``self``, ``filename`` and ``file``.
        """
        return FunctionMetadata.from_function(
            cls.analyze,
            omit={'self', 'dependency_bear', 'dependency_result'})

    def generate_tasks(self):
        return (((bear, dependency_result), {})
                for bear, dependency_results in self.dependency_results.items()
                for dependency_result in dependency_results)
