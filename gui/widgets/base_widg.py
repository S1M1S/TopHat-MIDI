import gtk
import midi.defaults.defaults as d


class BaseWidg():
    def __init__(self, parent, engine):
        self.parent = parent
        self.engine = engine

        self.alignment = gtk.Alignment()
        self.h_box = gtk.HBox()
        self.frame = gtk.Frame()
        self.v_box = gtk.VBox()
        self.drawing_area = gtk.DrawingArea()
        self.label = gtk.Label()
        self.context = None
        self.surface = None
        self.colour_map = None
        self.options_visible = False

        self.alignment.set(0.5, 0.5, 0, 0)  # centrally align everything inside
        self.drawing_area.set_size_request(d.DRAWING_AREA_WIDTH, d.DRAWING_AREA_HEIGHT)

        self.v_box.pack_start(self.drawing_area)
        self.v_box.pack_start(self.label)
        self.frame.add(self.v_box)
        self.h_box.pack_start(self.frame)
        self.alignment.add(self.h_box)

    def show_self(self):
        self.alignment.show_all()  # show everything
        # this is needed because of the inheritor's __init__ function
        # everything should show at the end of THAT function, not this __init__.

    def send_midi_msg(self, channel, note, vel):
        self.engine.midi_out(channel, note, vel)

    def set_label_text(self, new_text):
        self.label.set_text(new_text)

    def set_visibility(self, visibility):
        if visibility:
            self.alignment.show()
        else:
            self.alignment.hide()

    def set_parent(self, new_parent):
        self.parent = new_parent
        self.label.set_text(self.parent.get_name())
        self.option_widg.update_text()

    def get_parent(self):
        return self.parent