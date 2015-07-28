import shelve
import os
import time
from gi.repository import Gtk, GObject

from coalib.output.gui.support.ProjectMetadata import ProjectMetadata
from coalib.output.gui.support.Timestamp import process_timestamp


class GreeterWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        Gtk.ApplicationWindow.__init__(self,
                                       application=application,
                                       title="Select a Project")
        self.application = self.get_application()
        self.projectMetadata = ProjectMetadata()
        self.check_box_revealers = []
        self.search_text = ""

        self._ui = Gtk.Builder()
        self._ui.add_from_resource("/org/coala/GreeterWindow.ui")

        self._setup_view()

    def _setup_view(self):
        self.header_bar = self._ui.get_object("headerbar")
        self.set_titlebar(self.header_bar)

        self.set_default_size(800, 600)

        self.add(self._ui.get_object("project_box"))

        self.list_box = self._ui.get_object("projects")
        self.list_box.set_filter_func(self.filter_func, None)
        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        projects = shelve.open(self.projectMetadata.file)
        for key in projects:
            self.create_project_row(key, projects[key][0], projects[key][1])
        projects.close()
        self.new_button = self._ui.get_object("new")
        self.new_button.connect("clicked", self.on_new_button_clicked)
        self.selection_mode = self._ui.get_object("selection_mode")
        self.selection_mode.connect("clicked", self.on_select_button_clicked)
        self.search_button = self._ui.get_object("search_button")
        self.search_button.connect("toggled", self.on_search_button_clicked)
        self.selection_cancel = self._ui.get_object("cancel_button")
        self.selection_cancel.set_visible(False)
        self.selection_cancel.connect("clicked", self.on_cancel_button_clicked)
        self.action_bar = self._ui.get_object("action_bar")
        self.action_bar.set_visible(False)
        self.remove_button = self._ui.get_object("remove_button")
        self.remove_button.connect("clicked", self.delete_rows)

        self.search_bar = self._ui.get_object("search_bar")
        self.search_bar.set_window(self, self.search_button)

    def create_project_row(self, name, timestamp, location):
        list_box_template = Gtk.Builder()
        list_box_template.add_from_resource("/org/coala/ProjectRow.ui")

        list_box_row = Gtk.ListBoxRow()

        list_box_template.get_object("name_label").set_text(name)
        list_box_template.get_object("location_label").set_text(location)
        list_box_template.get_object("date_label").set_text(
            process_timestamp(timestamp, time.localtime()))
        self.check_box_revealers.append(
            list_box_template.get_object("revealer"))
        box = list_box_template.get_object("row")
        box.set_name(location)
        list_box_row.add(box)
        list_box_row.set_visible(True)
        list_box_row.set_activatable(True)

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
            self.projectMetadata.add_project(
                os.path.basename(dialog.get_filename()),
                str(dialog.get_filename()))
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def on_select_button_clicked(self, button):
        self.header_bar.get_style_context().add_class("selection-mode")
        self.new_button.set_visible(False)
        self.selection_mode.set_visible(False)
        self.selection_cancel.set_visible(True)
        self.action_bar.set_visible(True)
        for revealer in self.check_box_revealers:
            revealer.set_reveal_child(not revealer.get_child_revealed())

    def on_cancel_button_clicked(self, button):
        self.header_bar.get_style_context().remove_class("selection-mode")
        self.new_button.set_visible(True)
        self.selection_mode.set_visible(True)
        self.selection_cancel.set_visible(False)
        self.action_bar.set_visible(False)
        for revealer in self.check_box_revealers:
            revealer.set_reveal_child(not revealer.get_child_revealed())

    def on_search_button_clicked(self, button):
        self.search_bar.toggle_bar()

    def delete_rows(self, button):
        for revealer in self.check_box_revealers:
            if revealer.get_child().get_active():
                row_box = revealer.get_parent()
                self.projectMetadata.delete_project(
                    os.path.basename(row_box.get_name()))
                row_box.get_parent().destroy()

    def filter_func(self, row, data=None):
        if self.search_text == "":
            return True
        elif self.search_text.lower() in row.get_child().get_name().lower():
            return True
        return False

    def refilter(self, search_text):
        self.search_text = search_text
        self.list_box.invalidate_filter()
