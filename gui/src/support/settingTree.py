from gi.repository import Gtk


class coalaSettingTree(Gtk.ListStore):
    def __init__(self):
        Gtk.ListStore.__init__(self, str, str)

        self.treeView = Gtk.TreeView(self)

        renderer1 = Gtk.CellRendererText()
        renderer1.set_property("editable", True)
        column1 = Gtk.TreeViewColumn("Key", renderer1, text=0)
        self.treeView.append_column(column1)
        renderer1.connect("edited", self.text_edited_column1)
        renderer2 = Gtk.CellRendererText()
        renderer2.set_property("editable", True)
        column2 = Gtk.TreeViewColumn("Value", renderer2, text=1)
        self.treeView.append_column(column2)
        renderer2.connect("edited", self.text_edited_column2)
        self.treeView.set_headers_visible(False)
        self.treeView.set_visible(True)
        self.treeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)

    def text_edited_column1(self, widget, path, text):
        self[path][0] = text

    def text_edited_column2(self, widget, path, text):
        self[path][1] = text

