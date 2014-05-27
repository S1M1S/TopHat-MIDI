__author__ = 'Celery'
import os
import sys
import rtmidi
import pickle #TODO: import cPickle as pickle
from rtmidi.midiutil import open_midiport
from pot import Pot
from key import Key

NUM_OF_POTS = 8
NUM_OF_KEYS = 16

class Main():
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
        self.file = filename + '.txt'
        self.dir = project_dir

        try:
            os.stat(self.dir)
        except: #the TopHat-MIDI folder does not exist yet
            print('Making a new TopHat-MIDI folder at %s' % self.dir)
            os.mkdir(self.dir)

        #fill the file out with default things
        for i in range(NUM_OF_POTS):
            self.pots[i] = Pot(str(i), i, 'forward')
        for i in range(NUM_OF_KEYS):
            self.keys[i] = Key(str(i), NUM_OF_POTS + i, 'toggle')

    def save(self):
        f = open(os.path.join(self.dir, self.file), 'wb')

        for pot in self.pots:
            pickle.dump(pot, f)
        for key in self.keys:
            pickle.dump(key, f)

        f.close()

    def save_as(self, filename, project_dir=None):
        if project_dir is not None:
            self.dir = project_dir()
        else:
            self.dir = os.path.join(os.environ['USERPROFILE'], 'Documents', 'TopHat-MIDI') #default to my documents

        self.new_file(filename, self.dir)
        self.save()


if __name__ == '__main__':
    main = Main()
    main.save_as('default')
    pass