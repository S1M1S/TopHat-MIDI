__author__ = 'Celery'

import midi.defaults.defaults as d


class Base:
    def __init__(self, name, midi_loc, func, colour=None, state=False):
        self.name = name
        self.midi_loc = midi_loc
        self.func = func
        self.state = state
        self.linked_mod = None
        self.available_funcs = None
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

    def set_name(self, new_name):
        if len(new_name) > 10:
            raise NameError('Name was too long')
        self.name = new_name

    def set_midi_loc(self, new_midi_loc):
        success = True
        if new_midi_loc[:2] == "0x":
            base = 16
            new_midi_loc = new_midi_loc[2:]
        else:
            base = 10
        try:
            self.midi_loc = int(new_midi_loc, base)
        except ValueError:
            success = False
        return success

    def set_func(self, new_func):
        success = False
        if new_func in self.available_funcs:  # if it is an acceptable function
            self.func = new_func
            success = True
        return success

    def set_colour(self, new_colour):
        success = True
        if new_colour.startswith(('(','[')):  # it must be an rgb tuple or list
            try:
                self.colour = [int(x) for x in new_colour[1:-1].split(",")]  # make each item an integer
            except ValueError:
                success = False
            for val in self.colour:
                if val > 255:
                    success = False
        elif new_colour in d.rgb_cols:  # it must be a named colour
            self.colour = d.rgb_cols[new_colour]
        else:
            success = False
        return success

    def set_linked_mod(self, new_mod):
        self.linked_mod = new_mod

    def get_name(self):
        return self.name

    def get_midi_loc(self):
        return self.midi_loc

    def get_func(self):
        return self.func

    def get_colour(self):
        return self.colour

    def get_gtk_colour(self):
        gtk_colour = [int((x/255.0)*65535) for x in self.colour]  # gtk does not accept regular rgb vals
        return gtk_colour

    def get_available_funcs(self):
        return self.available_funcs