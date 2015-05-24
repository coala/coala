import os
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf


class coalaFileTree(Gtk.TreeStore):
    def __init__(self, path):
        Gtk.TreeStore.__init__(self, str, Pixbuf, str)

        self.path = path

        self.populateFileTree(self.path)
        self.fileTreeView = Gtk.TreeView(self)

        treeviewcol = Gtk.TreeViewColumn("File")
        colcelltext = Gtk.CellRendererText()
        colcelltext.set_property("foreground", "red")
        colcellimg = Gtk.CellRendererPixbuf()
        treeviewcol.pack_start(colcellimg, False)
        treeviewcol.pack_start(colcelltext, True)
        treeviewcol.add_attribute(colcelltext, "text", 0)
        treeviewcol.add_attribute(colcellimg, "pixbuf", 1)
        self.fileTreeView.append_column(treeviewcol)
        self.fileTreeView.set_size_request(244, -1)

        self.fileTreeView.connect("row-expanded", self.onRowExpanded)
        self.fileTreeView.connect("row-collapsed", self.onRowCollapsed)

    def populateFileTree(self, path, parent=None):
        itemCounter = 0

        for item in os.listdir(path):
            itemFullname = os.path.join(path, item)
            itemIsFolder = os.path.isdir(itemFullname)
            itemIcon = Gtk.IconTheme.get_default().load_icon("folder" if itemIsFolder else "text-x-generic-symbolic", 22, 0)
            currentIter = self.append(parent, [item, itemIcon, itemFullname])
            if itemIsFolder:
                self.append(currentIter, [None, None, None])
            itemCounter += 1

        if itemCounter < 1:
            self.append(parent, [None, None, None])

    def onRowExpanded(self, treeView, treeIter, treePath):
        newPath = self.get_value(treeIter, 2)
        self.populateFileTree(newPath, treeIter)
        self.remove(self.iter_children(treeIter))

    def onRowCollapsed(self, treeView, treeIter, treePath):
        currentChildIter = self.iter_children(treeIter)
        while currentChildIter:
            self.remove(currentChildIter)
            currentChildIter = self.iter_children(treeIter)
        self.append(treeIter, [None, None, None])