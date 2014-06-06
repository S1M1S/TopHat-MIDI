__author__ = 'Celery'

NUM_OF_POTS = 8
NUM_OF_KEYS_H = 4
NUM_OF_KEYS_V = 4

KEY_AREA_H = 100
KEY_AREA_V = 100

MAX_NAME_LENGTH = 10
KEY_PARAMS = [[0+i, 1+i, 2+i, 3+i] for i in range(4)]  # default key params, 2D list from 0 to 15
KEY_NAMES = [['CC#'+str(col) for col in row] for row in KEY_PARAMS]  # convert params to names

rgb_cols = {
    'white':    (255,255,255),
    'red':      (255,0,0),
    'green':    (0,255,0),
    'blue':     (0,0,255),
    'yellow':   (255,255,0),
    'pink':     (255,0,255),
    'cyan':     (0,255,255),
    'black':    (0,0,0)
}