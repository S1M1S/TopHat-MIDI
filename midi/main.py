__author__ = 'Celery'
import os
import sys
import rtmidi
from rtmidi import midiconstants as rt_const
from midi.pot import Pot
from midi.key import Key
import pickle #TODO: import cPickle as pickle
from rtmidi.midiutil import open_midiport
import midi.defaults as default


class Engine():
    def __init__(self):
        self.dir = None
        self.file = ''
        self.raw_data = ''
        self.pots = [None]*default.NUM_OF_POTS
        self.keys = [[None]*default.NUM_OF_KEYS_H for i in range(default.NUM_OF_KEYS_V)]
        self.midiout, self.portname = open_midiport(3, 'output')

    def open(self, filename):
        self.pots = [None]*default.NUM_OF_POTS
        self.file = filename
        self.dir = os.path.split(self.file)[0] #get the directory of the file
        f = open(os.path.join(self.dir, self.file), 'rb')

        for i in range(default.NUM_OF_POTS):
            self.pots[i] = pickle.load(f)
        for i in range(default.NUM_OF_KEYS_V):
            for j in range(default.NUM_OF_KEYS_H):
                self.keys[i][j] = pickle.load(f)
                self.keys[i][j].post_load()
        f.close()

    def new_file(self, filename, project_dir):
        self.dir = project_dir
        self.file = filename + '.txt'

        #fill the file out with default things
        for i in range(default.NUM_OF_POTS):
            self.pots[i] = Pot(str(i), i, 'forward')

        for i in range(default.NUM_OF_KEYS_V):
            for j in range(default.NUM_OF_KEYS_H):
                self.keys[i][j] = Key(default.KEY_NAMES[i][j], default.KEY_PARAMS[i][j], 'toggle')
        self.save()

    def save(self):
        f = open(os.path.join(self.dir, self.file), 'wb')
        for pot in self.pots:
            pickle.dump(pot, f)
        for row in self.keys:
            for key in row:
                key.pre_save()
                pickle.dump(key, f)
        f.close()

    def midi_out(self, midi_signal, midi_vel):
        self.midiout.send_message([rt_const.CONTROLLER_CHANGE, midi_signal, midi_vel])


if __name__ == '__main__':
    main = Engine()
    main.new_file('default', 'C:\\Users\\Celery\\Documents\\TopHat-MIDI')