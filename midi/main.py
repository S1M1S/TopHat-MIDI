__author__ = 'Celery'
import os
import cPickle as pickle
import rtmidi
from rtmidi import midiconstants as rt_const

from midi.objects.pot import Pot
from midi.objects.key import Key
import midi.defaults.defaults as d


class Engine():
    def __init__(self):
        self.dir = None
        self.file = ''
        self.raw_data = ''
        self.pots = [[None]*d.NUM_OF_POTS_H for i in range(d.NUM_OF_POTS_V)]
        self.keys = [[None]*d.NUM_OF_KEYS_H for i in range(d.NUM_OF_KEYS_V)]
        self.midiout = rtmidi.MidiOut()
        midi_ports = self.midiout.get_ports()
        self.midiout.open_port(2)

    def open(self, filename):
        self.file = filename
        self.dir = os.path.split(self.file)[0]  # get the directory of the file
        f = open(os.path.join(self.dir, self.file), 'rb')

        for i in range(d.NUM_OF_POTS_V):
            for j in range(d.NUM_OF_POTS_H):
                self.pots[i][j] = pickle.load(f)

        for i in range(d.NUM_OF_KEYS_V):
            for j in range(d.NUM_OF_KEYS_H):
                self.keys[i][j] = pickle.load(f)
                self.keys[i][j].post_load()
        f.close()

    def save_as(self, filename, project_dir):
        self.dir = project_dir
        self.file = filename + '.txt'
        self.save()

    def new_file(self, filename, project_dir):
        self.dir = project_dir
        self.file = filename + '.txt'

        #fill the file out with default things
        for i in range(d.NUM_OF_POTS_V):
            for j in range(d.NUM_OF_POTS_H):
                self.pots[i][j] = Pot(d.POT_NAMES[i][j], d.POT_CCS[i][j], 'forward')

        for i in range(d.NUM_OF_KEYS_V):
            for j in range(d.NUM_OF_KEYS_H):
                self.keys[i][j] = Key(d.KEY_NAMES[i][j], d.KEY_CCS[i][j], 'toggle')
        self.save()

    def save(self):
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
        f = open(os.path.join(self.dir, self.file), 'wb')
        for row in self.pots:
            for pot in row:
                pickle.dump(pot, f)
        for row in self.keys:
            for key in row:
                key.pre_save()
                pickle.dump(key, f)
        f.close()

    def midi_out(self, midi_channel, midi_signal, midi_vel):
        self.midiout.send_message([midi_channel, midi_signal, midi_vel])


if __name__ == '__main__':
    main = Engine()
    main.new_file('default', 'C:\\Users\\Celery\\Documents\\TopHat-MIDI')