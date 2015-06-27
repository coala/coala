from gi.repository import Gtk
from gi.repository import GtkSource


class LineRenderer(GtkSource.GutterRendererText):
    line_offset = 0

    def __init__(self, start_line, *args, **kwargs):
        self.line_offset = start_line
        GtkSource.GutterRendererText.__init__(self, *args, **kwargs)

    def do_query_data(self, start, end, flags):
        self.props.text = str(start.get_line() + self.line_offset + 1)
        label = Gtk.Label()
        pango_layout = label.get_layout()
        pango_layout.set_text(self.props.text, len(self.props.text))
        self.props.size = pango_layout.get_pixel_size()[0]
