from gi.repository import Gtk


class WorkspaceWindow(Gtk.ApplicationWindow):
    def __init__(self, application, src):
        Gtk.ApplicationWindow.__init__(self, application=application)

        self.connect("delete_event", self.on_close)

        self._ui = Gtk.Builder()
        self._ui.add_from_resource("/org/coala/WorkspaceWindow.ui")

        self._setup_view()

    def _setup_view(self):
        self.headerbar = self._ui.get_object("headerbar")
        self.set_titlebar(self.headerbar)

        self.add(self._ui.get_object("container"))

        self.stack = self._ui.get_object("main_stack")
        self.sections = self._ui.get_object("sections")
        self.section_switcher = self._ui.get_object("section_switcher")
        self.add_section_button = self._ui.get_object("add_section_button")
        self.add_section_button.connect("clicked", self.add_section)

    def add_section(self, button=None):
        section_row_template = Gtk.Builder()
        section_row_template.add_from_resource('/org/coala/SectionRow.ui')

        section_row = Gtk.ListBoxRow()
        box = section_row_template.get_object("section_row")
        delete_button = section_row_template.get_object("delete_button")
        section_row.add(box)
        section_row.set_visible(True)
        delete_button.connect("clicked", self.delete_row, section_row)

        self.section_switcher.add(section_row)
        self.section_switcher.queue_draw()

    def delete_row(self, button, listboxrow):
        listboxrow.destroy()

    def on_close(self, event, widget):
        self.get_application().greeter.show()
        self.destroy()
