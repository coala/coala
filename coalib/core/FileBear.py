from coalib.core.Bear import Bear
from coalib.settings.FunctionMetadata import FunctionMetadata


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
        Bear.__init__(self, section, file_dict)

        self._kwargs = self.get_metadata().create_params_from_section(section)

    @classmethod
    def get_metadata(cls):
        """
        :return:
            Metadata for the ``analyze`` function extracted from its signature.
            Excludes parameters ``self``, ``filename`` and ``file``.
        """
        return FunctionMetadata.from_function(
            cls.analyze,
            omit={'self', 'filename', 'file'})

    def generate_tasks(self):
        return (((filename, file), self._kwargs)
                for filename, file in self.file_dict.items())
