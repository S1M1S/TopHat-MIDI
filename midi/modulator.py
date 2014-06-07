__author__ = 'Celery'
from threading import Thread
import math
import time


class Mod(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.rate = 60  # beats per minute
        self.vel = 0
        self.x_coord = 0
        self.start_time = time.time()
        self.relatives = []
        self.exit = False


    def increment_vel(self):
        self.x_coord += (math.pi*self.rate) / 3000.0  # move the x_coord along the x axis of our sine curve
        new_vel = (math.sin(self.x_coord) + 1) / 2  # so it oscillates between 0 and 1
        self.vel = new_vel

    def set_rate(self, new_rate):
        self.rate = new_rate

    def get_vel(self):
        return self.vel

    def run(self):
        while not self.exit:
            time.sleep(0.001)  # one millisecond
            self.increment_vel()


if __name__ == '__main__':
    m = Mod('test')
    m.start()
