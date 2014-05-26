__author__ = 'Celery'

class Pot():
    def __init__(self, name, midi, func):
        self.name = name
        self.midi = midi
        self.function = func

    def change_name(self, new_name):
        self.name = new_name

    def change_midi(self, new_midi):
        self.midi = new_midi

    def change_function(self, new_func):
        self.function = new_func