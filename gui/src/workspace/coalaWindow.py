import os
from collections import OrderedDict
from gi.repository import Gtk

from gui.src.support.fileTree import coalaFileTree
from gui.src.support.settingTree import coalaSettingTree
from coalib.settings.ConfigurationGathering import load_config_file
from coalib.settings.Section import Section


class coalaWindow(Gtk.ApplicationWindow):

    def __init__(self, app, src):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title="coala")

        self.path = src
        os.chdir(self.path)
        self.sections = {}
        self.sections_view = {}

        self._ui = Gtk.Builder()
        self._ui.add_from_resource("/coala/coalaWindow.ui")

        self.header_bar = self._ui.get_object("header-bar")
        self.set_titlebar(self.header_bar)

        self.window_stack = self._ui.get_object("coalaWindowStack")
        self.add(self.window_stack)

        self.add_button = self._ui.get_object("add_section_button")
        self.add_button.connect("clicked", self.add_section_dialog, "Section name:")
        self.add_setting_button = self._ui.get_object("addsetting")
        self.add_setting_button.connect("clicked", self.add_setting)
        self.delete_setting_button = self._ui.get_object("delsetting")
        self.delete_setting_button.connect("clicked", self.del_setting)

        self.section_stack = self._ui.get_object("sections")
        self.section_stack_switcher = self._ui.get_object("section_switcher")
        self.section_stack_switcher.set_size_request(242, -1)
        self.section_window = self._ui.get_object("section_window")
        self.section_window.set_size_request(244, -1)

        self.filetree = coalaFileTree(src)
        self.filetreecontainer = self._ui.get_object("filetree")
        self.filetreecontainer.add(self.filetree.fileTreeView)
        self.filetreecontainer.set_size_request(244, -1)

        self.setup_config_file()

        self.set_default_size(1000, 800)

    def setup_config_file(self):
        if os.path.isfile(self.path+'/.coafile'):
            self.sections = load_config_file(self.path+'/.coafile', None)
        else:
            coafile = open(".coafile", "w")
            coafile.close()
        self.setup_sections()

    def setup_sections(self):
        for key in self.sections:
            self.add_section(key)

    def add_section_dialog(self, button, message):
        dialogWindow = Gtk.MessageDialog(self,
                                         Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                         Gtk.MessageType.QUESTION,
                                         Gtk.ButtonsType.OK_CANCEL,
                                         message)
        dialogBox = dialogWindow.get_content_area()
        userEntry = Gtk.Entry()
        userEntry.set_size_request(250, 0)
        userEntry.set_text("Test")
        userEntry.show_all()
        dialogBox.pack_end(userEntry, False, False, 0)
        response = dialogWindow.run()
        text = userEntry.get_text()
        dialogWindow.destroy()
        if response == Gtk.ResponseType.OK:
            self.add_section(text)
        else:
            return None

    def add_section(self, section):
        frame = Gtk.Frame()
        frame.set_name(section)
        frame.set_vexpand(True)
        frame.set_hexpand(True)
        frame.set_visible(True)
        frame.set_border_width(5)
        box = Gtk.Box()
        box.set_visible(True)
        box.set_hexpand(True)
        sw = Gtk.ScrolledWindow()
        sw.set_visible(True)
        sw.set_hexpand(True)
        settings = coalaSettingTree()
        self.sections_view[section] = settings
        sw.add(settings.treeView)
        box.add(sw)
        frame.add(box)
        if section in self.sections:
            for key in self.sections[section]:
                settings.append([key,
                                 str(self.sections[section][key])])
        self.section_stack.add_titled(frame, section, section)
        self.section_stack_switcher.queue_draw()

    def del_setting(self, button):
        section = self.section_stack.get_visible_child()
        settings = self.sections_view[section.get_name()]
        selection = settings.treeView.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
        model.remove(iter)

    def add_setting(self, button):
        section = self.section_stack.get_visible_child()
        settings = self.sections_view[section.get_name()]
        settings.append(["Entry", "Value"])
