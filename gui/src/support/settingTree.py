from gi.repository import Gtk


class coalaSettingTree(Gtk.ListStore):
    def __init__(self):
        Gtk.ListStore.__init__(self, str, str)

        self.treeView = Gtk.TreeView(self)

        renderer1 = Gtk.CellRendererText()
        column1 = Gtk.TreeViewColumn("Key", renderer1, text=0)
        self.treeView.append_column(column1)
        renderer2 = Gtk.CellRendererText()
        column2 = Gtk.TreeViewColumn("Value", renderer2, text=1)
        self.treeView.append_column(column2)
        self.treeView.set_headers_visible(False)

