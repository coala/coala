class DefaultLinterInterface:
    @staticmethod
    def generate_config(filename, file):
        """
        Generates the content of a config-file the linter-tool might need.

        The contents generated from this function are written to a temporary
        file and the path is provided inside ``create_arguments()``.

        By default no configuration is generated.

        You can provide additional keyword arguments and defaults. These will
        be interpreted as required settings that need to be provided through a
        coafile-section.

        :param filename: The name of the file currently processed.
        :param file:     The contents of the file currently processed.
        :return:         The config-file-contents as a string or ``None``.
        """
        return None

    @staticmethod
    def create_arguments(filename, file, config_file):
        """
        Creates the arguments for the linter.

        You can provide additional keyword arguments and defaults. These will
        be interpreted as required settings that need to be provided through a
        coafile-section.

        :param filename:    The name of the file the linter-tool shall process.
        :param file:        The contents of the file.
        :param config_file: The path of the config-file if used. ``None`` if
                            unused.
        :return:            A sequence of arguments to feed the linter-tool
                            with.
        """
        raise NotImplementedError
