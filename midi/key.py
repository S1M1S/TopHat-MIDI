__author__ = 'Celery'

import midi.defaults as d
import pygtk
import gtk


class Key:
    def __init__(self, name, midi_loc, func, colour=None, state=False):
        self.name = name
        self.midi_loc = midi_loc
        self.func = func
        self.state = state
        self.linked_mod = None
        if colour is not None:
            self.colour = colour
        else:
            self.colour = d.rgb_cols['red']  # defaults to red

    def pre_save(self):  # called just before saving
        if self.func == 'hold':
            self.state = False

    def post_load(self):  # called just after loading
        if self.func == 'hold':
            self.state = False

    def set_state(self, mouse_state):
        change_state = False
        if self.func == 'toggle':
            if mouse_state == 'press':
                change_state = True
        elif self.func == 'hold':
            change_state = True

        if change_state:
            self.state = not self.state  # toggle the boolean

        return change_state

    def set_name(self, new_name):
        self.name = new_name

    def set_midi_loc(self, new_midi_loc):
        if new_midi_loc.isdigit:
            self.midi_loc = int(new_midi_loc)

    def set_func(self, new_func):
        if new_func in ('toggle', 'hold'):  # if it is an acceptable function
            self.func = new_func

    def set_colour(self, new_colour):
        if new_colour.startswith(('(','[')):  # it must be an rgb tuple or list
            self.colour = [int(x) for x in new_colour[1:-1].split(",")]  # make each item an integer
        elif new_colour in d.rgb_cols:  # it must be a named colour
            self.colour = d.rgb_cols[new_colour]

    def set_linked_mod(self, new_mod):
        self.linked_mod = new_mod

    def get_gtk_colour(self):
        gtk_colour = map(lambda rgb: int((rgb/255.0)*65535), self.colour)  # gtk does not accept regular rgb vals
        return gtk_colour

    def get_midi_vel(self):
        return self.state*127  # return either 0 or 127