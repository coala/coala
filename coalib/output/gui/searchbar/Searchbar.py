from gi.repository import Gtk, GLib, Gdk


class Searchbar(Gtk.Revealer):
    __gtype_name__ = 'Searchbar'

    def __init__(self, window=None, search_button=None):
        Gtk.Revealer.__init__(self)

        self._searchContainer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                                        halign=Gtk.Align.CENTER)

        self._search_entry = Gtk.SearchEntry(max_width_chars=45)
        self._search_entry.connect("search-changed", self.on_search_changed)
        self._search_entry.show()
        self._searchContainer.add(self._search_entry)

        self._searchContainer.show_all()
        toolbar = Gtk.Toolbar()
        toolbar.get_style_context().add_class("search-bar")
        toolbar.show()
        self.add(toolbar)

        item = Gtk.ToolItem()
        item.set_expand(True)
        item.show()
        toolbar.insert(item, 0)
        item.add(self._searchContainer)

        self.window = window
        self.search_button = search_button
        self.show = False

    def on_search_changed(self, widget):
        self.window.refilter(self._search_entry.get_text())

    def set_window(self, window, search_button):
        self.window = window
        self.search_button = search_button
        self.window.connect("key-press-event", self._on_key_press)
        self.window.connect_after("key-press-event", self._after_key_press)

    def show_bar(self, show):
        self.show = show
        if not self.show:
            self._search_entry.set_text('')
        self.set_reveal_child(show)

    def toggle_bar(self):
        self.show_bar(not self.get_child_revealed())

    def _on_key_press(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)

        if keyname == 'Escape' and self.search_button.get_active():
            if self._search_entry.is_focus():
                self.search_button.set_active(False)
            else:
                self._search_entry.grab_focus()
            return True

        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if keyname == 'f':
                self.search_button.set_active(True)
                return True

        return False

    def _after_key_press(self, widget, event):
        if (not self.search_button.get_active() or
                not self._search_entry.is_focus()):
            if self._search_entry.im_context_filter_keypress(event):
                self.search_button.set_active(True)
                self._search_entry.grab_focus()

                # Text in entry is selected, deselect it
                l = self._search_entry.get_text_length()
                self._search_entry.select_region(l, l)

                return True

        return False
