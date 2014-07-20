__author__ = 'Celery'

import gtk
from base_widg import BaseWidg
from option_widg import OptionWidg
import midi.defaults.defaults as d


class KeyWidg(BaseWidg):
    def __init__(self, parent, engine):
        BaseWidg.__init__(self, parent, engine)

        self.set_label_text(parent.get_name())
        self.drawing_area.set_events(gtk.gdk.EXPOSURE_MASK  # drawing areas
                                     | gtk.gdk.BUTTON_PRESS_MASK  # do not receive mouse
                                     | gtk.gdk.BUTTON_RELEASE_MASK)  # clicks by default
        self.option_widg = OptionWidg(self)
        self.h_box.pack_end(self.option_widg.alignment)
        self.connect()
        self.show_self()
        self.option_widg.set_visibility(False)

    def connect(self):
        self.drawing_area.connect('expose_event', self.draw)
        self.drawing_area.connect('button_release_event', self.button_pressed)
        self.drawing_area.connect('button_press_event', self.button_pressed)

    def draw(self, widget, event, data=None):
        self.surface = self.drawing_area.window
        self.context = self.surface.new_gc()
        self.colour_map = self.drawing_area.get_colormap()
        self.surface.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
        self.context.set_values(foreground=self.colour_map.alloc('white'))
        self.surface.draw_rectangle(self.context,
                                    True,
                                    0,
                                    0,
                                    d.DRAWING_AREA_WIDTH,
                                    d.DRAWING_AREA_HEIGHT)  # fill the frame with white
        self.context.set_values(foreground=self.colour_map.alloc('grey'),
                                line_width=d.DRAWING_AREA_OUTLINE_THICKNESS,
                                cap_style=gtk.gdk.CAP_ROUND,
                                join_style=gtk.gdk.JOIN_ROUND)
        self.surface.draw_rectangle(self.context,
                                    False,  # only draw outline
                                    d.DRAWING_AREA_INDENT,  # x
                                    d.DRAWING_AREA_INDENT,  # y
                                    d.DRAWING_AREA_WIDTH - d.DRAWING_AREA_INDENT*2,  # width
                                    d.DRAWING_AREA_WIDTH - d.DRAWING_AREA_INDENT*2)  # height
        self.fill()
        return True

    def fill(self):  # whether or not to draw the coloured square in the middle
        if self.parent.state:  # it should be filled
            r, g, b = self.parent.get_gtk_colour()
            self.context.set_values(foreground=self.colour_map.alloc(r, g, b))
        else:
            self.context.set_values(foreground=self.colour_map.alloc('white'))
        self.surface.draw_rectangle(self.context,
                                    True,
                                    d.DRAWING_AREA_INDENT + d.DRAWING_AREA_OUTLINE_THICKNESS / 2,
                                    d.DRAWING_AREA_INDENT + d.DRAWING_AREA_OUTLINE_THICKNESS / 2,
                                    d.KEY_SQUARE_WIDTH - d.DRAWING_AREA_OUTLINE_THICKNESS,
                                    d.KEY_SQUARE_HEIGHT - d.DRAWING_AREA_OUTLINE_THICKNESS)

    def button_pressed(self, widget, event, data=None):
        if event.button == 1:  # left click
            if event.type == gtk.gdk.BUTTON_PRESS:
                if self.parent.set_state('press'):  # if state has changed
                    self.send_midi_msg(self.parent.get_channel(),
                                       self.parent.get_midi_loc(),
                                       self.parent.get_midi_vel())
                    self.fill()
            elif event.type == gtk.gdk.BUTTON_RELEASE:
                if self.parent.set_state('release'):
                    self.fill()
        elif event.button == 3 and event.type == gtk.gdk.BUTTON_PRESS:  # right click
            self.options_visible = not self.options_visible  # toggle boolean
            self.option_widg.set_visibility(self.options_visible)
        return True