from gi.repository import Gtk, Gdk, GObject


class EditableLabel(Gtk.Stack):
    __gtype_name__  = 'EditableLabel'

    __gsignals__ = {
        'edited': (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }

    default_label = GObject.property(type=str,
                                     default="EditableLabel",
                                     flags=GObject.PARAM_READWRITE)
    char_width = GObject.property(type=int,
                                  default=-1,
                                  flags=GObject.PARAM_READWRITE)

    def __init__(self):
        Gtk.Stack.__init__(self)

        self._ui = Gtk.Builder()
        self._ui.add_from_resource('/org/coala/EditableLabel.ui')

        self.entry = self._ui.get_object("entry")
        self.entry.connect("changed", self._on_entry_changed)
        self.entry.connect("focus-out-event", self._on_entry_focus_out)
        self.entry.connect("key-press-event", self._on_key_press_event)
        self.label = self._ui.get_object("label")
        self.edit_button = self._ui.get_object("edit-button")
        self.edit_button.connect("clicked", self._on_edit_button_clicked)

        self.box1 = self._ui.get_object("label-container")
        self.box2 = self._ui.get_object("entry-container")

        self.add_named(self.box1, "label")
        self.add_named(self.box2, "entry")

        self.connect("notify::default-label", self._on_default_label_changed)
        self.connect("notify::char-width", self._on_char_width_changed)

    def _on_edit_button_clicked(self, button):
        self.set_visible_child_name("entry")
        self.entry.grab_focus()

    def _on_entry_changed(self, widget):
        self.label.set_text(widget.get_text())
        self.set_name(widget.get_text())

    def _on_entry_focus_out(self, widget, event):
        self.set_visible_child_name("label")
        self.emit("edited", 0)

    def _on_key_press_event(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)

        if keyname == 'Escape':
            self.set_visible_child_name("label")
        if keyname == 'Return':
            self.set_visible_child_name("label")

    @staticmethod
    def _on_default_label_changed(obj, gparamstring):
        obj.label.set_text(obj.get_property("default-label"))

    @staticmethod
    def _on_char_width_changed(obj, gparamstring):
        obj.label.set_max_width_chars(obj.get_property("char-width"))
        obj.entry.set_max_width_chars(obj.get_property("char-width"))
