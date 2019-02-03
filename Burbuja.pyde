
WIDTH = HEIGHT = 800

class StateCollection:
    BASE = 0
    FOCUSED = 1
    TO_FOCUSED = 2
    FROM_FOCUSED = 3
    
    @staticmethod
    def time_to_switch_state(current_state, time_ms):

        if current_state == StateCollection.BASE:
            time_limit_ms = 1000
        elif current_state == StateCollection.FOCUSED:
            time_limit_ms = 1000
        elif current_state == StateCollection.TO_FOCUSED:
            time_limit_ms = 1000
        elif current_state == StateCollection.FROM_FOCUSED:
            time_limit_ms = 1000
        
        return time_ms >= time_limit_ms
    
    @staticmethod
    def next_state(current_state):
        return (current_state + 1) % 4

class State:

    def __init__(self, b_list):
        self.time = 0
        self.dt_s = 0.0  # Time in seconds
        self.started = False
        self.b_list = b_list
        self.state = StateCollection.BASE
        self.millis_of_last_switch = 0

    def update(self):
        if not self.started:
            self.started = True
            return
        new_time = millis()
        self.dt_s = (new_time - self.time) / 1000.0
        self.time = new_time
        
        time_this_state_ms = millis() - self.millis_of_last_switch
        if StateCollection.time_to_switch_state(self.state, time_this_state_ms):
            self.state = StateCollection.next_state(self.state)   
            self.millis_of_last_switch = millis()
            print(millis(), "New state: ", self.state)

class Color:

    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b

class Object:

    def __init__(self, position, velocity):
        self.position, self.velocity = position, velocity

    def move(self, dt):
        self.position += self.velocity * dt


class Burbuja(Object):

    def __init__(self, _color, _title, _text, _media, _radius, position, velocity):
        Object.__init__(self, position, velocity)
        self.color = _color
        self.title = _title
        self.text = _text
        self.media = _media
        self.radius = _radius
        self.neighbors = []

    def do_draw(self):
        fill(255)
        ellipse(self.position.x, self.position.y,
                self.radius * 2, self.radius * 2)
        self.draw_title()
        # self.draw_text()

    def draw_title(self):
        fill(0)
        textAlign(CENTER)
        text(self.title, self.position.x, self.position.y)

    """
    def draw_text(self):
        textAlign(CENTER)
        text(self.title, self.position.x, self.position.y)
    """

    def move(self, dt):
        Object.move(self, dt)

    def bounce(self):
        self.edge_bounce()
        self.neighbor_bounce()

    def edge_bounce(self):
        x, y, r = self.position.x, self.position.y, self.radius

        if not r < x < WIDTH - r:
            self.velocity.x *= -1  # Change velocity direction
            self.position.x = WIDTH - r
            if x < r:
                self.position.x = r

        if not r < y < HEIGHT - r:
            self.velocity.y *= -1
            self.position.y = HEIGHT - r
            if y < r:
                self.position.y = r

    def neighbor_bounce(self):
        for neighbor in self.neighbors:
            delta_pos = neighbor.position - self.position
            diff = (self.radius + neighbor.radius - delta_pos.mag()) / \
                delta_pos.mag()
            self.position -= diff * delta_pos
            angle = atan2(delta_pos.y, delta_pos.x)
            # TODO: Solve bounce when several balls collider
            # TODO: Use momentum preservation priciple at collision
            speed = self.velocity.mag()

            self.velocity.x = -speed * cos(angle)
            self.velocity.y = -speed * sin(angle)

    @staticmethod
    def check_collisions(_b_list):
        for b in _b_list:
            del b.neighbors[:]
        i_start = 1
        for b1 in _b_list[:-2]:
            b_to_check = _b_list[i_start:]
            i_start += 1
            for b2 in b_to_check:
                ball_distance = dist(
                    b1.position.x, b1.position.y, b2.position.x, b2.position.y)
                collision_distance = b1.radius + b2.radius
                if collision_distance >= ball_distance:
                    b1.neighbors.append(b2)
                    b2.neighbors.append(b1)


NUM_BURBUJAS = 10
VELOCITY_MAX = 50
positions = (PVector(random(WIDTH * 0.9), random(HEIGHT * 0.9))
             for _ in range(NUM_BURBUJAS))
velocities = (PVector(random(-VELOCITY_MAX, VELOCITY_MAX),
                      random(-VELOCITY_MAX, VELOCITY_MAX)) for _ in range(NUM_BURBUJAS))
c = Color(192, 0, 210)
b_list = [Burbuja(c, "Spam", "Monty Python", None, 40, p, v)
          for p, v in zip(positions, velocities)]
state = State(b_list)
f = PFont()


def setup():
    size(WIDTH, HEIGHT)
    f = createFont("Helvetica", 16, True)
    textFont(f)
    fill(0)


def draw():
    background(192, 165, 210)
    state.update()
    [b.move(state.dt_s) for b in b_list]
    Burbuja.check_collisions(b_list)
    [b.bounce() for b in b_list]
    [b.do_draw() for b in b_list]
