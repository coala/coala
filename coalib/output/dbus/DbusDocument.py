import dbus.service


class DbusDocument(dbus.service.Object):
    """
    This is a dbus object-path for every document that a DbusApplication wants
    coala to analyze.
    """
    interface = "org.coala.v1"

    def __init__(self, path=""):
        super(DbusDocument, self).__init__()
        self.path = path

    @dbus.service.method(interface,
                         in_signature="",
                         out_signature="")
    def Analyze(self):
        """
        This method analyzes the document and sends back the result
        """
        # TODO use SectionManager and SectionExecutor to analyze the document
        pass
