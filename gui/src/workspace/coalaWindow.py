from gi.repository import Gtk


class coalaWindow(Gtk.ApplicationWindow):

    def __init__(self, app, src):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title="coala")

        self._ui = Gtk.Builder()
        self._ui.add_from_resource("/coala/coalaWindow.ui")

        self.header_bar = self._ui.get_object("header-bar")
        self.set_titlebar(self.header_bar)

        self.window_stack = self._ui.get_object("coalaWindowStack")
        self.add(self.window_stack)

        self.add_button = self._ui.get_object("add_section_button")
        self.add_button.connect("clicked", self.add_section_dialog, "Section name:")

        self.section_stack = self._ui.get_object("sections")
        self.section_stack_switcher = self._ui.get_object("section_switcher")

        self.set_default_size(1000, 800)

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
        box = Gtk.Box()
        box.set_visible(True)
        button = Gtk.Button()
        button.set_label(section)
        button.show_all()
        box.add(button)
        self.section_stack.add_titled(box, section, section)
        self.section_stack_switcher.queue_draw()


