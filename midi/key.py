__author__ = 'Celery'

from defaults import rgb_cols
import pygtk
import gtk


class Key():
    def __init__(self, name, x_loc, y_loc, midi_loc, func, colour=None, state=False):
        self.name = name
        self.midi_loc = midi_loc
        self.func = func
        self.state = state
        if colour is not None:
            self.colour = colour
        else:
            self.colour = rgb_cols['red']  # defaults to red

    def pre_save(self):  # called just before saving
        if self.func == 'hold':
            self.state = False

    def post_load(self):  # called just after loading
        if self.func == 'hold':
            self.state = False

    def set_state(self, mouse_state):
        if self.func == 'toggle':
            if mouse_state == 'press':
                self.state = not self.state

        elif self.func == 'hold':
            self.state = not self.state  # toggle the boolean

    def set_name(self, new_name):
        self.name = new_name

    def set_xy(self, new_x_loc, new_y_loc):
        self.x_loc = new_x_loc
        self.y_loc = new_y_loc

    def set_midi_loc(self, new_midi_loc):
        self.midi_loc = new_midi_loc

    def get_gtk_colour(self):
        gtk_colour = map(lambda rgb: int((rgb/255.0)*65535), self.colour)  # gtk does not accept regular rgb vals
        return gtk_colour