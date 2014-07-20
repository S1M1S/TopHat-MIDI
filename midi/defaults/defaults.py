__author__ = 'Celery'
import os

DIRECTORY = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split('\\')[:-2])

NUM_OF_POTS_H = 4
NUM_OF_POTS_V = 2

NUM_OF_KEYS_H = 4
NUM_OF_KEYS_V = 4

DRAWING_AREA_WIDTH = DRAWING_AREA_HEIGHT = 100
DRAWING_AREA_OUTLINE_THICKNESS = 6
DRAWING_AREA_INDENT = 10
DRAWING_AREA_CENTRE = 50

POT_LINE_THICKNESS = 5
POT_CIRCLE_RADIUS = 40

KEY_SQUARE_WIDTH = KEY_SQUARE_HEIGHT = 80

DEFAULT_WIDGET_WIDTH = 100
DEFAULT_WIDGET_HEIGHT = 121

OPTION_MENU_X = 2
OPTION_MENU_Y = 4
OPTION_WIDGET_WIDTH = 130
OPTION_PADDING = 3

LABEL_HEIGHT = 21

MAX_NAME_LENGTH = 10

POT_CCS = [[0+i, 1+i, 2+i, 3+i] for i in range(0, NUM_OF_POTS_V*NUM_OF_POTS_H, NUM_OF_POTS_H)]
POT_NAMES = [['CC#'+str(col) for col in row] for row in POT_CCS]

KEY_CCS = [[64+i, 65+i, 66+i, 67+i] for i in range(0, 16, 4)]  # default key params, 2D list from 0 to 15
KEY_NAMES = [['CC#'+str(col) for col in row] for row in KEY_CCS]  # convert params to names

rgb_cols = {}

for line in open(os.path.join(DIRECTORY, 'midi', 'defaults', 'colours.tsv'), 'rU'):
    key, r, g, b = line.rstrip().split('\t')
    r, g, b = [int(x) for x in [r, g, b]]
    rgb_cols[key] = (r, g, b)