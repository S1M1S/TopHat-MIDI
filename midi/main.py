__author__ = 'Celery'
import os
import sys
import rtmidi
from midi.pot import Pot
from midi.key import Key
import pickle #TODO: import cPickle as pickle
from rtmidi.midiutil import open_midiport
from midi.defaults import NUM_OF_POTS, NUM_OF_KEYS

class Engine():
    def __init__(self):

        self.dir = None
        self.file = ''
        self.raw_data = ''
        self.pots = [None]*NUM_OF_POTS
        self.keys = [None]*NUM_OF_KEYS

        self.midiout, self.portname = open_midiport(3, 'output')

    def open(self, filename):
        self.pots = [None]*NUM_OF_POTS
        self.file = filename
        self.dir = os.path.split(self.file)[0] #get the directory of the file
        f = open(os.path.join(self.dir, self.file), 'rb')

        for i in range(NUM_OF_POTS):
            self.pots[i] = pickle.load(f)
        for i in range(NUM_OF_KEYS):
            self.keys[i] = pickle.load(f)

        f.close()

    def new_file(self, filename, project_dir):
        self.dir = project_dir()
        self.file = filename + '.txt'

        #fill the file out with default things
        for i in range(NUM_OF_POTS):
            self.pots[i] = Pot(str(i), i, 'forward')
        for i in range(NUM_OF_KEYS):
            self.keys[i] = Key(str(i), NUM_OF_POTS + i, 'toggle')
        self.save()

    def save(self):
        f = open(os.path.join(self.dir, self.file), 'wb')

        for pot in self.pots:
            pickle.dump(pot, f)
        for key in self.keys:
            pickle.dump(key, f)

        f.close()

if __name__ == '__main__':
    main = Engine()
    main.save_as('default')
    main.open('C:\\Users\\Celery\\Documents\\TopHat-MIDI\\default.txt')
    print main.pots