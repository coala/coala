import time
from gui.src.support.projectMetadata import ProjectMetadata
from gi.repository import Gtk


class coalaProject(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title="project")
        self.application = self.get_application()

        self.projectMetadata = ProjectMetadata()

        self._ui = Gtk.Builder()
        self._ui.add_from_resource("/coala/coalaProject.ui")

        self.list_box = None

        self._setup_view()

    def _setup_view(self):
        self.header_bar = self._ui.get_object("header-bar")
        self.set_titlebar(self.header_bar)

        self.set_default_size(800, 600)

        self.add(self._ui.get_object("project-box"))

        self.list_box = self._ui.get_object("listbox")
        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        projects = self.projectMetadata.get_projects_dict()
        if projects is not None:
            for key in projects:
                self.create_project_row(key, projects[key][0], projects[key][1])

        self.accept_button = self._ui.get_object("accept-project-button")
        self.new_button = self._ui.get_object("new-button")
        self.new_button.connect("clicked", self.on_new_button_clicked)

    def create_project_row(self, name, date, loc):
        list_box_template = Gtk.Builder()
        list_box_template.add_from_resource("/coala/coalaRecentProjectRow.ui")

        list_box_row = Gtk.ListBoxRow()

        list_box_template.get_object("name_label").set_text(name)
        list_box_template.get_object("location_label").set_text(loc)
        list_box_template.get_object("date_label").set_text(date)
        box = list_box_template.get_object("row")
        box.set_name(loc)
        list_box_row.add(box)

        self.list_box.insert(list_box_row, 0)

    def on_new_button_clicked(self, button):
        dialog = Gtk.FileChooserDialog("Please choose a project",
                                       self,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       ("Cancel",
                                        Gtk.ResponseType.CANCEL,
                                        "Select",
                                        Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
            self.projectMetadata.add_project_to_dict(str(dialog.get_filename()),
                                                     str(time.time()),
                                                     str(dialog.get_filename()))
            self.hide()
            self.application.setup_and_show_workspace(self.application,
                                                      dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()
