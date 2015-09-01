from pyprint.ClosableObject import ClosableObject


class HTMLWriter(ClosableObject):
    """
    Printer for outputting HTML Log files.

    :param filename:            the name of the file to put the data into
                                (string).
    :param indentation_per_tag: spaces used to indent every subsequent HTML
                                tag.
    :raises TypeError:          if directory of given file doesn't exist or in
                                case of access problems.
    """

    def __init__(self, filename, indentation_per_tag=2, indentation=0):
        ClosableObject.__init__(self)

        self.indentation_per_tag = indentation_per_tag
        self.indentation = indentation
        self.file = None
        self.filename = filename

        if not isinstance(filename, str):
            raise TypeError("filename must be a string")

        self.file = open(filename, 'w+')
        self.__write_header()

    def _close(self):
        # Check if the file object is NoneType, trying to close a None object
        # does not make sense
        if self.file is not None:
            self.__write_footer()
            self.file.close()

    def __write_header(self):
        self.write("<!DOCTYPE html>")
        self.open_tag("html")

    def __write_footer(self):
        self.close_tag("html")

    def write_comment(self, *comments):
        """
        Function for writing HTML comments in the output HTML log files.

        :param comments: an arbitrary number of comments to add to the HTML
                         log file
        """
        for comment in comments:
            self.write("<!-- " + comment + " -->")

    def write_tag(self, tag, content="", **tagargs):
        """
        Function for writing an HTML tag, along with the required tag
        attributes and content.

        :param tag:     HTML Tag for formatting the content.
        :param content: content to output into the HTML Log file.
        :param tagargs: arbitrary HTML tag attributes mapped to their
                        respective values. Ordering of the tags is
                        not preserved.
        """
        name = tag
        for arg in tagargs:
            name += " " + arg + "=\"" + tagargs[arg] + "\""

        if content == "":
            self.write("<"+name+"/>")
            return

        self.open_tag(name)
        self.write(content)
        self.close_tag(tag)

    def open_tag(self, tag_name):
        """
        Function to open HTML tag. e.g. <p>

        :param tag_name: the name of HTML Tag to written in the output logfile.
        """
        self.write("<"+tag_name+">")
        self.indentation += 4

    def close_tag(self, tag_name):
        """
        Function to close an open HTML tag. e.g. </p>

        :param tag_name: the name of HTML Tag to be written to output logfile.
        """
        self.indentation -= 4
        self.write("</"+tag_name+">")

    def write(self, *args):
        """
        Function to write in the given output HTML log file.

        :param args: arbitrary number of arguments to be written to output
                     logfile.
        """
        for line in args:
            self.file.write(" "*self.indentation + line + "\n")
