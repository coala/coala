import os
from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import Gdk

from gui.src.support.fileTree import coalaFileTree
from gui.src.support.settingTree import coalaSettingTree
from coalib.settings.ConfigurationGathering import load_config_file
from gui.src.support.WriteFile import write_to_file_and_run
from gui.src.support.LineRenderer import LineRenderer


class coalaWindow(Gtk.ApplicationWindow):

    def __init__(self, app, src):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title="coala")

        self.path = src
        os.chdir(self.path)
        self.sections = {}
        self.sections_view = {}
        self.results = None

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
        self.select = self.filetree.fileTreeView.get_selection()
        self.select.connect("changed", self.on_file_tree_selection_changed)

        self.source_view = self._ui.get_object("sourceview")
        self.source_view_iter = 0

        self.setup_config_file()

        self.set_default_size(1000, 800)

    def setup_config_file(self):
        if os.path.isfile(self.path+'/.coafile'):
            self.sections = load_config_file(self.path+'/.coafile', None)
        else:
            coafile = open(".coafile", "w")
            coafile.close()
        self.setup_sections()
        self.results = write_to_file_and_run(self.sections_view)

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
        settings.renderer1.connect("edited", self.text_edited_column1, settings)
        settings.renderer2.connect("edited", self.text_edited_column2, settings)
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
        self.results = write_to_file_and_run(self.sections_view)

    def add_setting(self, button):
        section = self.section_stack.get_visible_child()
        settings = self.sections_view[section.get_name()]
        settings.append(["Entry", "Value"])
        self.results = write_to_file_and_run(self.sections_view)

    def text_edited_column1(self, widget, path, text, liststore):
        liststore[path][0] = text
        self.results = write_to_file_and_run(self.sections_view)

    def text_edited_column2(self, widget, path, text, liststore):
        liststore[path][1] = text
        self.results = write_to_file_and_run(self.sections_view)

    def on_file_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            if os.path.isdir(model[treeiter][2]):
                print("You selected", model[treeiter][0], model[treeiter][2])
            else:
                self.source_view_iter = 0
                print("You selected", model[treeiter][0], model[treeiter][2])
                if self.source_view:
                    children = self.source_view.get_children()
                    for child in children:
                        child.destroy()
                prev = None
                if self.results[model[treeiter][2]]:
                    for result in sorted(self.results[model[treeiter][2]]):
                        print(result)
                        if prev:
                            if prev.line_nr:
                                self.print_result(result, max(result.line_nr-5, prev.line_nr))
                            else:
                                self.print_result(result, max(result.line_nr-5, 1))
                        else:
                            if result.line_nr:
                                self.print_result(result, max(result.line_nr-5, 1))
                            else:
                                self.print_result(result)
                        prev = result

    def print_result(self,result, start_nr=None):
        colored_box = Gtk.Box()
        if result.severity == 0:
            colored_box.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0,255,0,.5))
        elif result.severity == 1:
            colored_box.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(255,255,0,.5))
        else:
            colored_box.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(255,0,0,.5))
        colored_box.set_size_request(21, -1)
        colored_box.set_visible(True)
        colored_box.set_vexpand(True)
        if result.line_nr is None:
            self.source_view.attach(colored_box, 0, self.source_view_iter, 1, 1)
            frame = Gtk.Frame()
            frame.set_hexpand(True)
            frame.set_vexpand(True)
            frame.set_label(result.origin)
            frame_layout = Gtk.Box()
            frame_layout.set_border_width(5)
            label = Gtk.Label()
            label.set_text(result.message)
            label.set_visible(True)
            label.set_vexpand(True)
            label.set_hexpand(True)
            frame_layout.add(label)
            frame_layout.set_hexpand(True)
            frame_layout.set_vexpand(True)
            frame_layout.set_visible(True)
            frame.add(frame_layout)
            frame.set_visible(True)
            frame.set_border_width(10)
            self.source_view.attach(frame, 1, self.source_view_iter, 1,1)
            self.source_view_iter += 1

        else:
            language_manager = GtkSource.LanguageManager.new()
            language = language_manager.guess_language(result.file, None)
            textbuffer = GtkSource.Buffer()
            textbuffer.set_highlight_syntax(True)
            textbuffer.set_language(language)
            textbuffer.set_text(''.join(open(result.file).readlines()[start_nr:result.line_nr])[:-1])
            textview = GtkSource.View(visible=True, buffer=textbuffer, monospace=True, editable=False)
            textview.set_visible(True)
            textview.set_hexpand(True)
            self.source_view.attach(textview, 0,self.source_view_iter, 2, 1)
            gutter = textview.get_gutter(Gtk.TextWindowType.LEFT)
            renderer = LineRenderer(start_nr, xpad=6, xalign=1.0)
            gutter.insert(renderer, 0)
            self.source_view_iter += 1

            self.source_view.attach(colored_box, 0, self.source_view_iter, 1, 1)
            frame = Gtk.Frame()
            frame.set_hexpand(True)
            frame.set_vexpand(True)
            frame.set_label(result.origin)
            frame_layout = Gtk.Grid(row_spacing=3, column_spacing=1)
            frame_layout.set_border_width(5)
            label = Gtk.Label()
            label.set_text(result.message)
            label.set_visible(True)
            label.set_vexpand(True)
            label.set_hexpand(True)
            frame_layout.attach(label, 0, 0, 3,1)
            ignore_button = Gtk.Button()
            ignore_button.set_label("Ignore")
            ignore_button.set_visible(True)
            ignore_button.set_hexpand(True)
            ignore_button.set_vexpand(True)
            frame_layout.attach(ignore_button,0,1,1,1)
            edit_button = Gtk.Button()
            edit_button.set_label("Edit Manually")
            edit_button.set_visible(True)
            edit_button.set_hexpand(True)
            edit_button.set_vexpand(True)
            frame_layout.attach(edit_button,1,1,1,1)
            patch_button = Gtk.Button()
            patch_button.set_label("Apply Patch")
            patch_button.set_visible(True)
            patch_button.set_hexpand(True)
            patch_button.set_vexpand(True)
            frame_layout.attach(patch_button,2,1,1,1)
            frame_layout.set_hexpand(True)
            frame_layout.set_vexpand(True)
            frame_layout.set_visible(True)
            frame.add(frame_layout)
            frame.set_visible(True)
            frame.set_border_width(10)
            ignore_button.connect("clicked", self.ignore_btn, textview, frame, colored_box)
            edit_button.connect("clicked", self.edit_btn, result.file)
            patch_button.connect("clicked", self.patch_btn, result)
            if len(result.get_actions()) == 1:
                patch_button.set_sensitive(False)
            self.source_view.attach(frame, 1, self.source_view_iter, 1,1)
            self.source_view_iter += 1

    def ignore_btn(self, button, source_view, frame, colored_box):
        source_view.destroy()
        frame.destroy()
        colored_box.destroy()

    def edit_btn(self, button, filename):
        os.system("open "+filename)

    def patch_btn(self, button, result):
        print(result.get_actions())
