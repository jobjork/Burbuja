from burbuja_object import Burbuja
from state import State
from utils import *

BURBUJAS_LIST = [
    ["First title text", "First list \nof \ncontents"], 
    ["Second title text", "Second list \nof \ncontents"],
    ["Third title text", "Third list \nof \ncontents"], 
    ["Fourth title text", "Fourth list \nof \ncontents"]
]
NUM_BURBUJAS = len(BURBUJAS_LIST)

positions = (PVector(random(WIDTH * 0.9)
                     , random(HEIGHT * 0.9))
             for _ in range(NUM_BURBUJAS))
velocities = (PVector(random(-VELOCITY_MAX, VELOCITY_MAX),
                      random(-VELOCITY_MAX, VELOCITY_MAX)) for _ in range(NUM_BURBUJAS))

c = Color(192, 0, 210)
b_list = [Burbuja(c, b[0], DEFAULT_TITLE_TEXT_SIZE, b[1], DEFAULT_CONTENTS_TEXT_SIZE, None, 40, p, v)
          for b, p, v in zip(BURBUJAS_LIST, positions, velocities)]
state = State(b_list)
f = PFont()


def setup():
    frameRate(400)
    size(WIDTH, HEIGHT)
    f = createFont("Helvetica", 16, True)
    textFont(f)
    fill(0)


def draw():
    smooth(80)
    background(192, 165, 210)
    state.update()
    state.resize_ball_in_list(b_list)
    [b.move(state.dt_s) for b in b_list]
    Burbuja.check_collisions(b_list)
    [b.bounce() for b in b_list]
    [b.do_draw() for b in b_list]
