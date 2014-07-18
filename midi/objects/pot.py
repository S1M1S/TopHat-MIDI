__author__ = 'Celery'

from base import Base
import rtmidi.midiconstants as m


def clamp(n, min_n, max_n):  # clamp input between min and max
    return max(min(max_n, n), min_n)


class Pot(Base):
    def __init__(self, name, midi_loc, func, colour=None, state=False):
        Base.__init__(self, name, midi_loc, func, colour=None, state=False)
        self.available_funcs = ('forward', 'reverse', 'step', 'modulate')
        self.vel = 0
        self.old_vel = 0

    def set_vel(self, mouse_y):
        has_changed = False
        new_vel = self.vel + mouse_y
        self.vel = clamp(new_vel, 0, 127)
        if self.vel != self.old_vel:
            has_changed = True
        self.old_vel = self.vel
        return has_changed

    def get_midi_vel(self):
        return self.vel