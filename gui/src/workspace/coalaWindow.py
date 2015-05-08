from gi.repository import Gtk


class coalaWindow(Gtk.ApplicationWindow):

    def __init__(self,app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title="coala")

        self._ui = Gtk.Builder()
        self._ui.add_from_resource("/coala/coalaWindow.ui")

        self.header_bar = self._ui.get_object("header-bar")
        self.set_titlebar(self.header_bar)

        self.window_stack = self._ui.get_object("coalaWindowStack")
        self.add(self.window_stack)

        self.show_all()