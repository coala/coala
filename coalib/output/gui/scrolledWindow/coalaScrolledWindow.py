from gi.repository import Gtk
from gi.repository import GObject


class coalaScrolledWindow(Gtk.ScrolledWindow):

    __gtype_name__ = 'coalaScrolledWindow'

    max_contentwidth = GObject.property(type=int,
                                       default=-1,
                                       flags=GObject.PARAM_READWRITE)
    max_contentheight = GObject.property(type=int,
                                        default=-1,
                                        flags=GObject.PARAM_READWRITE)

    def __init__(self, *args, **kwargs):
        Gtk.ScrolledWindow.__init__(self, *args, **kwargs)
        self.max_content_width = -1
        self.max_content_height = -1
        self.connect("notify::max-contentheight",
                     self.on_notify_max_height_changed)
        self.connect("notify::max-contentwidth",
                     self.on_notify_max_width_changed)

    @staticmethod
    def on_notify_max_height_changed(obj, gparamstring):
        print("Success")
        obj.max_content_height = obj.get_property("max-contentheight")
        obj.set_size_request(obj.get_allocated_width(), obj.max_content_height)

    @staticmethod
    def on_notify_max_width_changed(obj, gparamstring):
        print("Success")
        obj.max_content_width = obj.get_property("max-contentwidth")
        obj.set_size_request(obj.max_content_width,
                             obj.get_allocated_height())
