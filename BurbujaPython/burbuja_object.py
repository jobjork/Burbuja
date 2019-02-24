from utils import *

class Object:

    def __init__(self, position, velocity):
        self.position, self.velocity = position, velocity

    def move(self, dt):
        self.position += self.velocity * dt

class Burbuja(Object):

    def __init__(self, _color, _title, _title_size, _text, _text_size, _media, _radius, position, velocity):
        Object.__init__(self, position, velocity)
        self.color = _color
        self.title = _title
        self.title_size = _title_size
        self.text = _text
        self.text_size = _text_size
        self.media = _media
        self.radius = _radius
        self.neighbors = []
        self.is_growing = False
        self.is_shrinking = False

    def do_draw(self):
        fill(255)
        self.update_radius()
        ellipse(self.position.x, self.position.y,
                self.radius * 2, self.radius * 2)
        self.draw_title()
        self.draw_contents()

    def draw_title(self):
        fill(0)
        textAlign(CENTER)
        textSize(MIN_TITLE_TEXT_SIZE + self.radius/TITLE_SCALE_FACTOR)
        y_coordinate = self.position.y - self.radius* CONTENTS_SHIFT_Y
        text(self.title, self.position.x, y_coordinate)
    
    def draw_contents(self):
        text_size = MIN_TEXT_SIZE + (self.radius - MIN_RADIUS)/CONTENTS_SCALE_FACTOR
        if text_size > 0:
            fill(0)
            textAlign(CENTER)
            y_coordinate = self.position.y + self.radius* CONTENTS_SHIFT_Y
            textSize(text_size)
            text(self.text, self.position.x, y_coordinate)

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

    def start_growth(self):
        self.is_shrinking = False
        self.is_growing = True

    def start_shrinkage(self):
        self.is_growing = False
        self.is_shrinking = True

    def update_radius(self):
        if self.is_growing:
            self.radius += RADIUS_GROWTH
        elif self.is_shrinking:
            self.radius -= RADIUS_GROWTH
        self.radius = constrain(self.radius, MIN_RADIUS, MAX_RADIUS)
        
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
