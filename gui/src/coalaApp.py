import os
from gi.repository import Gtk, Gio

from gui.src.workspace.coalaWindow import coalaWindow


class coalaApp(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="coala",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.resource = Gio.resource_load(os.getcwd()+"/data/coala.gresource")
        Gio.Resource._register(self.resource)

        self.connect("activate", self.activateCb)

    def activateCb(self, app):
        window = coalaWindow(app)
        app.add_window(window)