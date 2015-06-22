from gi.repository import Gtk


class coalaSettingTree(Gtk.ListStore):
    def __init__(self):
        Gtk.ListStore.__init__(self, str, str)

        self.treeView = Gtk.TreeView(self)

        self.renderer1 = Gtk.CellRendererText()
        self.renderer1.set_property("editable", True)
        column1 = Gtk.TreeViewColumn("Key", self.renderer1, text=0)
        self.treeView.append_column(column1)
        self.renderer2 = Gtk.CellRendererText()
        self.renderer2.set_property("editable", True)
        column2 = Gtk.TreeViewColumn("Value", self.renderer2, text=1)
        self.treeView.append_column(column2)
        self.treeView.set_headers_visible(False)
        self.treeView.set_visible(True)
        self.treeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)

