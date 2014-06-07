__author__ = 'Celery'
import rtmidi.midiconstants as m

class Pot:
    def __init__(self, name, midi_loc, func):
        self.name = name
        self.midi_loc = midi_loc
        self.function = func
        self.vel = 0

    def fire(self):
        return [m.CONTROLLER_CHANGE, self.midi_loc, self.vel]

    def set_vel(self, new_vel):
        self.vel = new_vel

    def set_name(self, new_name):
        self.name = new_name

    def set_midi(self, new_midi):
        self.midi = new_midi

    def set_function(self, new_func):
        self.function = new_func