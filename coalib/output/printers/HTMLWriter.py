class HTMLWriter:
    """
    Printer for outputting HTML Log files.

    :raises TypeError: If directory of given file doesn't exist or in case of
    access problems

    :param filename:            the name of the file to put the data into (string).
    :param indentation_per_tag: spaces used to indent every subsequent HTML tag
    """

    def __init__(self, filename, indentation_per_tag=2, indentation=0):
        self.indentation_per_tag = indentation_per_tag
        self.indentation = indentation
        self.file = None
        self.filename = filename

        if not isinstance(filename, str):
            raise TypeError("filename must be a string")

        self.file = open(filename, 'w+')
        self.__write_header()


    def __del__(self):
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

        :param comments: string denoting the comment to be inserted
        """
        for comment in comments:
            self.write("<!-- " + comment + " -->")

    def write_tag(self, tag, content="", **tagargs):
        """

        :param tag:     HTML Tag for formatting the content
        :param content: content to output into the HTML Log file
        :param tagargs: attributes to the HTML tag param
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

    def write_tags(self, **tags):
        """

        :param tags: dict(HTML tag name: HTML content): mapping of HTML tag to its content
        """
        for tag in tags:
            content = tags[tag]
            if not content:
                self.write("<"+tag+"/>")
                continue

            self.open_tag(tag)
            self.write(content)
            self.close_tag(tag)

    def open_tag(self, tag_name):
        """

        :param tag_name: the name of HTML Tag to written in the output logfile
        """
        self.write("<"+tag_name+">")
        self.indentation += 4

    def close_tag(self, tag_name):
        """

        :param tag_name: the name of HTML Tag to be written to output logfile
        """
        self.indentation -= 4
        self.write("</"+tag_name+">")

    def write(self, *args):
        """

        :param args: arbitrary number of arguments to be written to output logfile
        """
        for line in args:
            self.file.write(" "*self.indentation + line + "\n")
