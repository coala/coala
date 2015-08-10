from gi.repository import Gtk
import os
from collections import OrderedDict
from coalib.settings.ConfigurationGathering import load_configuration
from coalib.output.ConfWriter import ConfWriter
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.printers.NullPrinter import NullPrinter
from coalib.settings.Section import Section
from coalib.misc.DictUtilities import update_ordered_dict_key

from coalib.output.gui.workspace.SectionView import SectionView


class WorkspaceWindow(Gtk.ApplicationWindow):
    def __init__(self, application, src):
        Gtk.ApplicationWindow.__init__(self, application=application)

        self.connect("delete_event", self.on_close)

        self._ui = Gtk.Builder()
        self._ui.add_from_resource("/org/coala/WorkspaceWindow.ui")

        self.section_stack_map = {}
        self.sections_dict = OrderedDict()
        self.src = src

        self._setup_view()
        self.read_coafile()

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

    def add_section(self, button=None, name=None):
        section_row_template = Gtk.Builder()
        section_row_template.add_from_resource('/org/coala/SectionRow.ui')

        section_row = Gtk.ListBoxRow()
        box = section_row_template.get_object("section_row")
        editable_label = section_row_template.get_object("name-edit")
        delete_button = section_row_template.get_object("delete_button")
        if name is not None:
            editable_label.entry.set_text(name)
            self.create_section_view(widget=editable_label,
                                     row_obejct=section_row)
            editable_label.connect("edited",
                                   self.update_section_name,
                                   name,
                                   self.section_stack_map[section_row])
        else:
            editable_label.connect("edited",
                                   self.create_section_view,
                                   section_row)
        section_row.add(box)
        section_row.set_visible(True)
        delete_button.connect("clicked", self.delete_row, section_row)

        self.section_switcher.add(section_row)
        self.section_switcher.queue_draw()
        return section_row

    def delete_row(self, button, listboxrow):
        del self.sections_dict[self.section_stack_map[listboxrow].get_name()]
        self.section_stack_map[listboxrow].destroy()
        del self.section_stack_map[listboxrow]
        listboxrow.destroy()
        conf_writer = ConfWriter(self.src+'/.coafile')
        conf_writer.write_sections(self.sections_dict)
        conf_writer.close()

    def on_close(self, event, widget):
        self.get_application().greeter.show()
        self.destroy()

    def create_section_view(self, widget=None, arg=None, row_obejct=None):
        section_view = SectionView(self.sections_dict, self.src)
        section_view.set_visible(True)
        section_view.set_name(widget.get_name())
        self.sections.add_named(section_view, widget.get_name())
        self.sections.set_visible_child_name(widget.get_name())
        if arg is not None:
            widget.connect("edited",
                           self.update_section_name,
                           widget.get_name(),
                           section_view)
            self.sections_dict[widget.get_name()] = Section(widget.get_name())
            section_view.add_setting()
            conf_writer = ConfWriter(self.src+'/.coafile')
            conf_writer.write_sections(self.sections_dict)
            conf_writer.close()
        self.section_stack_map[row_obejct] = section_view

    def on_row_selection_changed(self, listbox, row):
        self.sections.set_visible_child(self.section_stack_map[row])

    def read_coafile(self):
        if os.path.isfile(self.src+'/.coafile'):
            self.sections_dict = load_configuration(
                ["-c", self.src+'/.coafile'], LogPrinter(NullPrinter()))[0]
            for section in self.sections_dict:
                section_row = self.add_section(name=section)
                for setting in self.sections_dict[section].contents:
                    if "comment" in setting:
                        continue
                    self.section_stack_map[section_row].add_setting(
                        self.sections_dict[section].contents[setting])
                self.section_stack_map[section_row].add_setting()

    def update_section_name(self, widget, arg, old_name, section_view):
        section_view.set_name(widget.get_name())
        self.sections_dict[old_name].name = widget.get_name()
        self.sections_dict = update_ordered_dict_key(self.sections_dict,
                                                     old_name,
                                                     widget.get_name())
        widget.connect("edited", self.update_section_name, widget.get_name())
        conf_writer = ConfWriter(self.src+'/.coafile')
        conf_writer.write_sections(self.sections_dict)
        conf_writer.close()
