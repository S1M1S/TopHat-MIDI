__author__ = 'Celery'
import os
from pot import Pot
from key import Key

NUM_OF_POTS = 8
NUM_OF_KEYS = 16

class Main():
    def __init__(self):
        self.dir = None
        self.file = ''
        self.raw_data = ''
        self.pots = []*NUM_OF_POTS
        self.keys = []*NUM_OF_KEYS

    def open(self, filename):
        self.file = filename
        self.dir = os.path.split(self.file)[0] #get the directory of the file
        print(self.dir)

        f = open(self.file, 'r')
        self.raw_data = f.read()

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
            self.pots[i] = Pot(str(i), str())

    def save(self):
        f = open(os.path.join(self.dir, self.file), 'w')
        f.write(self.raw_data)
        f.close()

    def save_as(self, filename, project_dir=None):
        self.raw_data = 'test'

        if project_dir is not None:
            self.dir = project_dir()
        else:
            self.dir = os.path.join(os.environ['USERPROFILE'], 'Documents', 'TopHat-MIDI') #default to my documents

        self.new_file(filename, self.dir)
        self.save()


if __name__ == '__main__':
    main = Main()
    main.save_as('default')