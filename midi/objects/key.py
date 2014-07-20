__author__ = 'Celery'

from base import Base
import midi.defaults.defaults as d


class Key(Base):
    def __init__(self, name, midi_loc, func, colour=None, state=False):
        Base.__init__(self, name, midi_loc, func, colour=None, state=False)
        self.available_funcs = ('toggle', 'hold')

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

    def get_channel(self):
        return 0x90  # NOTE ON

    def get_state(self):
        return self.state

    def get_midi_vel(self):
        return self.state*127  # return either 0 or 127