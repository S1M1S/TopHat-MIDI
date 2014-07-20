__author__ = 'Celery'

from base import Base
import rtmidi.midiconstants as m


def clamp(n, min_n, max_n):  # clamp input between min and max
    return max(min(max_n, n), min_n)


class Pot(Base):
    def __init__(self, name, midi_loc, func, colour=None, state=False):
        Base.__init__(self, name, midi_loc, func, colour=None, state=False)
        self.available_funcs = ('forward', 'reverse', 'step')
        self.vel = self.old_vel = self.scaled_vel = 0.0
        self.num_steps = 5.0

    def set_vel(self, mouse_y):
        has_changed = False
        new_vel = 0

        if self.func == 'forward':
            new_vel = self.vel + mouse_y
        elif self.func == 'reverse':
            new_vel = self.vel - mouse_y

        if self.func == 'step':
            new_vel = self.scaled_vel + mouse_y * self.num_steps / 127.0
            self.scaled_vel = clamp(new_vel, 0, self.num_steps)
            self.vel = int(self.scaled_vel) * 127.0 / self.num_steps
        else:
            self.vel = clamp(new_vel, 0.0, 127.0)

        if self.vel != self.old_vel:
            has_changed = True
        self.old_vel = self.vel
        return has_changed

    def set_num_steps(self, new_num):
        success = True
        try:
            self.num_steps = float(new_num)
        except ValueError:
            success = False
        return success

    def get_midi_vel(self):
        return self.vel

    def get_num_steps(self):
        return self.num_steps

    def get_channel(self):
        return 0xB0