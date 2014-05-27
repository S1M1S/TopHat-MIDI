__author__ = 'Celery'

from defaults import rgb_cols

class Key():
    def __init__(self, name, midi_val, colour=None, state=None):
        self.name = name
        self.midi_val = midi_val
        if colour is not None: #defaults to red
            self.colour = colour
        else:
            self.colour = rgb_cols['red']
        self.state = state

    def stub(self):
        pass #the cheese please