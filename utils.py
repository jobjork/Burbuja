# Default constants
WIDTH = HEIGHT = 800
MIN_RADIUS = 40
MAX_RADIUS = 100
RADIUS_GROWTH = 0.8
TEXT_SCALE_FACTOR = 5
MIN_TITLE_TEXT_SIZE = 12
DEFAULT_TITLE_TEXT_SIZE = MIN_TITLE_TEXT_SIZE + MIN_RADIUS/TEXT_SCALE_FACTOR
MIN_TEXT_SIZE = 0
DEFAULT_TEXT_SIZE = MIN_TEXT_SIZE + MIN_RADIUS/TEXT_SCALE_FACTOR
NUM_BURBUJAS = 10
VELOCITY_MAX = 50

class Color:

    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b
