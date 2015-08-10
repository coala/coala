from gi.repository import Gtk, Gdk

from coalib.settings.Setting import Setting
from coalib.output.ConfWriter import ConfWriter


class SectionView(Gtk.ListBox):
    def __init__(self, sections_dict, src):
        Gtk.ListBox.__init__(self, selection_mode=Gtk.SelectionMode.NONE)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/org/coala/workspace.css')
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen,
                                        css_provider,
                                        Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.get_style_context().add_class("settings-group")

        self.sections_dict = sections_dict
        self.src = src

    def add_setting(self, setting=None):
        setting_row_template = Gtk.Builder()
        setting_row_template.add_from_resource("/org/coala/SettingRow.ui")
        box = setting_row_template.get_object("setting_row")
        key_label = setting_row_template.get_object("name")
        delete_button = setting_row_template.get_object("delete_button")
        value_entry = setting_row_template.get_object("value")
        key_label.connect("edited",
                          self.on_key_changed,
                          delete_button,
                          value_entry)
        setting_row = Gtk.ListBoxRow()
        setting_row.get_style_context().add_class("setting")
        setting_row.add(box)
        setting_row.set_visible(True)
        delete_button.connect("clicked", self.delete_setting, setting_row)

        if setting is not None:
            key_label.label.set_label(setting.key)
            value_entry.set_text(setting.value)
            key_label.connect("edited", self.update_key, setting)
            value_entry.connect("changed", self.update_value, setting)
            delete_button.set_sensitive(True)
            delete_button.set_name(setting.key)

        self.add(setting_row)

    def delete_setting(self, button, setting_row):
        self.sections_dict[self.get_name()].delete_setting(button.get_name())
        setting_row.destroy()
        conf_writer = ConfWriter(self.src+'/.coafile')
        conf_writer.write_sections(self.sections_dict)
        conf_writer.close()

    def on_key_changed(self, widget, arg, sensitive_button, value_entry):
        setting = Setting(widget.get_name(), value_entry.get_text())
        self.sections_dict[self.get_name()].append(setting)
        self.add_setting()
        sensitive_button.set_sensitive(True)
        sensitive_button.set_name(setting.key)
        widget.connect("edited", self.update_key, setting, sensitive_button)
        value_entry.connect("focus-out-event", self.update_value, setting)
        conf_writer = ConfWriter(self.src+'/.coafile')
        conf_writer.write_sections(self.sections_dict)
        conf_writer.close()

    def update_key(self, widget, arg, setting, delete_button):
        setting.key = widget.get_name()
        delete_button.set_name(widget.get_name())
        conf_writer = ConfWriter(self.src+'/.coafile')
        conf_writer.write_sections(self.sections_dict)
        conf_writer.close()

    def update_value(self, widget, setting):
        setting.value = widget.get_text()
        conf_writer = ConfWriter(self.src+'/.coafile')
        conf_writer.write_sections(self.sections_dict)
        conf_writer.close()

