import os
from gi.repository import Gtk, Gio

from gui.src.workspace.coalaWindow import coalaWindow
from gui.src.project.coalaProject import coalaProject


class coalaApp(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="org.coala",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.resource = Gio.resource_load(os.getcwd()+"/data/coala.gresource")
        Gio.Resource._register(self.resource)

        self.connect("activate", self.activateCb)

    def activateCb(self, app):
        window = coalaWindow(app)
        window2 = coalaProject(app)
        app.add_window(window2)
