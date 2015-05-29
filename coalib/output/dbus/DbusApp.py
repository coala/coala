class DbusApp:
    """
    Stores data about each client that connects to the DbusServer
    """
    def __init__(self, id, name=""):
        self.id = id
        self.name = name

        self.docs = {}
        self.next_doc_id = 0
