from gi.repository import Gtk


class coalaProject(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title="project")

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

        self.accept_button = self._ui.get_object("accept-project-button")

    def create_project_row(self, name, date, loc):
        list_box_template = Gtk.Builder()
        list_box_template.add_from_resource("/coala/coalaRecentProjectRow.ui")

        list_box_row = Gtk.ListBoxRow()

        list_box_template.get_object("name_label").set_text(name)
        list_box_template.get_object("location_label").set_text(loc)
        list_box_template.get_object("date_label").set_text(date)
        box = list_box_template.get_object("row")
        list_box_row.add(box)

        self.list_box.add(list_box_row)