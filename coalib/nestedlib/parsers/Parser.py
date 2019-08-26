from coalib.nestedlib.NlSection import NlSection
from coalib.io.File import File


class Parser():

    def parse(self, filename):
        """
        Return a list of nl_sections.

        :param file_contents: The contents of the original nested file
        """
        raise NotImplementedError


# The following methods are the utilities for the parsers.

def get_file(filename):
    """
    Get the contents of the file mentioned in filename.
    Returns a tuple of all lines present in the file
    """
    file = File(filename)
    return file.lines


def create_nl_section(file,
                      index,
                      language,
                      start_line=None,
                      start_column=None,
                      end_line=None,
                      end_column=None,):
    """
    Create a NlSection Object from the values.
    Returns the NlSection object
    """
    return NlSection.from_values(file=file,
                                 index=index,
                                 language=language,
                                 start_line=start_line,
                                 start_column=start_column,
                                 end_line=end_line,
                                 end_column=end_column,
                                 )
