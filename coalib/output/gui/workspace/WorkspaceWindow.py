from gi.repository import Gtk

from coalib.output.gui.workspace.SectionView import SectionView


class WorkspaceWindow(Gtk.ApplicationWindow):
    def __init__(self, application, src):
        Gtk.ApplicationWindow.__init__(self, application=application)

        self.connect("delete_event", self.on_close)

        self._ui = Gtk.Builder()
        self._ui.add_from_resource("/org/coala/WorkspaceWindow.ui")

        self.section_stack_map = {}

        self._setup_view()

    def _setup_view(self):
        self.headerbar = self._ui.get_object("headerbar")
        self.set_titlebar(self.headerbar)

        self.add(self._ui.get_object("container"))

        self.stack = self._ui.get_object("main_stack")
        self.sections = self._ui.get_object("sections")
        self.section_switcher = self._ui.get_object("section_switcher")
        self.section_switcher.connect("row-selected",
                                      self.on_row_selection_changed)
        self.add_section_button = self._ui.get_object("add_section_button")
        self.add_section_button.connect("clicked", self.add_section)

    def add_section(self, button=None):
        section_row_template = Gtk.Builder()
        section_row_template.add_from_resource('/org/coala/SectionRow.ui')

        section_row = Gtk.ListBoxRow()
        box = section_row_template.get_object("section_row")
        editable_label = section_row_template.get_object("name-edit")
        editable_label.connect("edited", self.create_section_view, section_row)
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

    def create_section_view(self, widget=None, arg=None, row_obejct=None):
        section_view = SectionView()
        section_view.set_visible(True)
        section_view.add_setting()
        section_view.set_name(widget.get_name())
        self.sections.add_named(section_view, widget.get_name())
        self.sections.set_visible_child_name(widget.get_name())
        widget.connect("edited", self.set_section_view_name, section_view)
        self.section_stack_map[row_obejct] = section_view

    def set_section_view_name(self, widget, arg, view):
        view.set_name(widget.get_name())

    def on_row_selection_changed(self, listbox, row):
        self.sections.set_visible_child(self.section_stack_map[row])
