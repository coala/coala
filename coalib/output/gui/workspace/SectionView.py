from gi.repository import Gtk, Gdk


class SectionView(Gtk.ListBox):
    def __init__(self):
        Gtk.ListBox.__init__(self, selection_mode=Gtk.SelectionMode.NONE)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/org/coala/workspace.css')
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen,
                                        css_provider,
                                        Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.get_style_context().add_class("settings-group")

    def add_setting(self):
        setting_row_template = Gtk.Builder()
        setting_row_template.add_from_resource("/org/coala/SettingRow.ui")
        box = setting_row_template.get_object("setting_row")
        key_label = setting_row_template.get_object("name")
        delete_button = setting_row_template.get_object("delete_button")
        key_label.connect("edited", self.on_key_changed, delete_button)

        setting_row = Gtk.ListBoxRow()
        setting_row.get_style_context().add_class("setting")
        setting_row.add(box)
        setting_row.set_visible(True)
        delete_button.connect("clicked", self.delete_setting, setting_row)
        self.add(setting_row)

    def delete_setting(self, button, setting_row):
        setting_row.destroy()

    def on_key_changed(self, widget, arg, sensitive_button):
        self.add_setting()
        sensitive_button.set_sensitive(True)
        widget.connect("edited", lambda a, b: None)

