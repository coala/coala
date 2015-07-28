import os
from gi.repository import Gtk, Gio, GObject

from coalib.output.gui.greeter.GreeterWindow import GreeterWindow
from coalib.output.gui.scrolledWindow.coalaScrolledWindow import (
    coalaScrolledWindow)
from coalib.output.gui.searchbar.Searchbar import Searchbar


class coalaApp(Gtk.Application):
    def __init__(self):
        GObject.type_register(coalaScrolledWindow)
        GObject.type_register(Searchbar)
        Gtk.Application.__init__(self,
                                 application_id="org.coala",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        gresource = os.path.join(os.path.dirname(__file__),
                                 "data",
                                 "coala.gresource")
        self.resource = Gio.resource_load(gresource)
        Gio.Resource._register(self.resource)

        self.greeter = None
        self.workspace = None

        self.connect("activate", self.activate)

    def _setup_greeter(self, app):
        self.greeter = GreeterWindow(app)
        self.greeter.list_box.connect("row-activated",
                                      self._setup_workspace,
                                      app)

    def _setup_workspace(self, listbox, listboxrow, app):
        print(listboxrow.get_child().get_name())

    def activate(self, app):
        self._setup_greeter(app)
        self.greeter.show()
