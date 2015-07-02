import os
from gi.repository import Gtk, Gio

from gui.src.workspace.coalaWindow import coalaWindow
from gui.src.project.coalaProject import coalaProject


class coalaApp(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="org.coala",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.resource = Gio.resource_load(os.getcwd()+"/gui/data/coala.gresource")
        Gio.Resource._register(self.resource)

        self.project_window = None
        self.workspace_window = None

        self.connect("activate", self.activateCb)

    def _setup_project_window(self, app):
        self.project_window = coalaProject(app)
        self.project_window.accept_button.connect(
            "clicked", self._setup_and_show_workspace, app)

    def _setup_and_show_workspace(self, button, app):
        row = self.project_window.list_box.get_selected_row()
        self.workspace_window = coalaWindow(app, row.get_child().get_name())
        self.project_window.destroy()
        self.workspace_window.show_all()

    def setup_and_show_workspace(self, app, src):
        self.workspace_window = coalaWindow(app, src)
        self.workspace_window.show_all()

    def activateCb(self, app):
        self._setup_project_window(app)
        self.project_window.show_all()