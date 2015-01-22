class SectionParser:
    def parse(self, input_data):
        """
        Parses the input and adds the new data to the existing

        :param input_data: filename or other input
        :return: the section dictionary
        """

        raise NotImplementedError

    def reparse(self, input_data):
        """
        Parses the input and overwrites all existent data

        :param input_data: filename or other input
        :return: the section dictionary
        """
        raise NotImplementedError

    def export_to_settings(self):
        """
        :return a dict of section objects representing the current parsed things
        """
        raise NotImplementedError
