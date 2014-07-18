import math

__author__ = 'Celery'

import gtk
from base_widg import BaseWidg
from option_widg import OptionWidg
import midi.defaults.defaults as d


class PotWidg(BaseWidg):
    def __init__(self, parent, engine):
        BaseWidg.__init__(self, parent, engine)

        self.set_label_text(parent.get_name())
        self.drawing_area.set_events(gtk.gdk.EXPOSURE_MASK
                                     | gtk.gdk.BUTTON1_MOTION_MASK
                                     | gtk.gdk.BUTTON_PRESS_MASK)
        self.option_widg = OptionWidg(self)
        self.options_visible = False
        self.still_dragging = self.drag_start = False
        self.start_pos = 0
        self.h_box.pack_end(self.option_widg.alignment)
        self.connect()
        self.show_self()
        self.option_widg.set_visibility(False)

    def connect(self):
        self.drawing_area.connect('expose_event', self.draw)
        self.drawing_area.connect('motion_notify_event', self.dragged)
        self.drawing_area.connect('button_press_event', self.button_pressed)

    def draw(self, widget, event, data=None):
        self. surface = self.drawing_area.window
        self.context = self.surface.new_gc()
        self.colour_map = self.drawing_area.get_colormap()
        self.surface.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
        self.context.set_values(foreground=self.colour_map.alloc('white'))
        self.surface.draw_rectangle(self.context,
                                    True,  # filled
                                    0,
                                    0,
                                    d.DRAWING_AREA_WIDTH,
                                    d.DRAWING_AREA_HEIGHT)  # fill the frame with white
        self.context.set_values(foreground=self.colour_map.alloc('grey'),
                                line_width=d.DRAWING_AREA_OUTLINE_THICKNESS,
                                cap_style=gtk.gdk.CAP_ROUND,
                                join_style=gtk.gdk.JOIN_ROUND)
        self.surface.draw_arc(self.context,
                              False,  # outline only
                              d.DRAWING_AREA_INDENT,  # start x
                              d.DRAWING_AREA_INDENT,  # start y
                              d.DRAWING_AREA_WIDTH - d.DRAWING_AREA_INDENT*2,  # width
                              d.DRAWING_AREA_WIDTH - d.DRAWING_AREA_INDENT*2,  # height
                              0,
                              64*360)  # circle
        self.fill()
        return True

    def fill(self):
        self.context.set_values(foreground=self.colour_map.alloc('white'))
        self.surface.draw_arc(self.context,
                              True,  # filled
                              d.DRAWING_AREA_INDENT + d.DRAWING_AREA_OUTLINE_THICKNESS/2,
                              d.DRAWING_AREA_INDENT + d.DRAWING_AREA_OUTLINE_THICKNESS/2,
                              d.DRAWING_AREA_WIDTH - d.DRAWING_AREA_INDENT*2 - d.DRAWING_AREA_OUTLINE_THICKNESS + 1,
                              d.DRAWING_AREA_WIDTH - d.DRAWING_AREA_INDENT*2 - d.DRAWING_AREA_OUTLINE_THICKNESS + 1,
                              0,                           # + 1 is needed above because of the way GTK handles outlines
                              64*360)
        r, g, b = self.parent.get_gtk_colour()
        self.context.set_values(foreground=self.colour_map.alloc(r, g, b),
                                line_width=d.POT_LINE_THICKNESS)
        angle = ((self.parent.get_midi_vel() * 2*math.pi) / 127.0) - math.pi/2  # angle in radians, set to point up
        line_end_x = int(d.DRAWING_AREA_CENTRE + math.cos(angle) * (d.POT_CIRCLE_RADIUS-d.DRAWING_AREA_OUTLINE_THICKNESS))
        line_end_y = int(d.DRAWING_AREA_CENTRE + math.sin(angle) * (d.POT_CIRCLE_RADIUS-d.DRAWING_AREA_OUTLINE_THICKNESS))
        self.surface.draw_line(self.context,
                               d.DRAWING_AREA_CENTRE,
                               d.DRAWING_AREA_CENTRE,
                               line_end_x,  # x
                               line_end_y)  # y

    def dragged(self, widget, event, data=None):
        if self.still_dragging:  # user is holding the mouse down
            if self.drag_start:
                self.start_pos = event.y
                self.drag_start = False
            delta_y = event.y - self.start_pos
            new_vel = int(delta_y/2)  # /2 for easier precision for user
            if self.parent.set_vel(new_vel):  # don't send midi messages unless vel has changed
                self.send_midi_msg(self.parent.get_midi_loc(),
                                   self.parent.get_midi_vel(),
                                   True)  # pots are always NOTE_ON messages
            self.fill()
            self.start_pos = event.y
        return True

    def button_pressed(self, widget, event, data=None):
        if event.button == 1:  # left click
            if event.type == gtk.gdk.BUTTON_PRESS:
                self.still_dragging = self.drag_start = True
            elif event.type == gtk.gdk.BUTTON_RELEASE:
                self.still_dragging = False
        if event.button == 3:  # right click
            self.options_visible = not self.options_visible
            self.option_widg.set_visibility(self.options_visible)
        return True
