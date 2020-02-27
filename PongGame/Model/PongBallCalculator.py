from pybricks.tools import print
from Model.ScreenGeometry import *
import math
#from random import random
import urandom

INITIAL_ANGLE_RANGE_DEGREES = 60.0
INITIAL_ANGLE_RANGE = math.radians(INITIAL_ANGLE_RANGE_DEGREES)

def rand_int(min, max):
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val

def rand_float():
    RANGE = 60000
    return rand_int(0, RANGE) / (1.0 * RANGE)

class PongBallCalculator:
    def reset(self):
        self.left_missed = False
        self.right_missed = False
        self.game_over = False
        self.randomize_speed_angle()
        self.x = SCREEN_WIDTH / 2.0
        self.y = SCREEN_HEIGHT / 2.0

    def randomize_speed_angle(self):
        # Limit angle to +-INITIAL_ANGLE_RANGE and either right or left side
        side = 0.0 if rand_float() < 0.5 else 1.0
        angle = -INITIAL_ANGLE_RANGE + 2.0 * INITIAL_ANGLE_RANGE * rand_float()
        speed_angle = angle + side * math.pi

        self.speed_x = BALL_SPEED * math.cos(speed_angle)
        self.speed_y = BALL_SPEED * math.sin(speed_angle)

    def set_left_paddle_y(self, left_y):
        self.left_paddle_y = left_y

    def set_right_paddle_y(self, right_y):
        self.right_paddle_y = right_y

    def is_paddle_hit(self, paddle_y, hit_y):
        bottom_edge = paddle_y - PADDLE_EDGE_HEIGHT
        top_edge = bottom_edge + PADDLE_HEIGHT + 2.0 * PADDLE_EDGE_HEIGHT
        return bottom_edge <= hit_y and hit_y <= top_edge

    def get_hit_y(self, hit_delta_x):
        hit_delta_time = hit_delta_x / self.speed_x
        return self.y + hit_delta_time * self.speed_y

    def update_state(self, delta_time):
        delta_x = delta_time * self.speed_x
        delta_y = delta_time * self.speed_y
        
        advance_x = self.x + delta_x
        if advance_x > SCREEN_WIDTH:
            hit_y = self.get_hit_y(SCREEN_WIDTH - self.x)
            
            if not self.is_paddle_hit(self.right_paddle_y, hit_y):
                self.right_missed = True
                self.x = SCREEN_WIDTH
                self.y = hit_y
                return False

            remainder = advance_x - SCREEN_WIDTH
            self.x = SCREEN_WIDTH - remainder
            self.speed_x = -self.speed_x
        elif advance_x < 0.0:
            hit_y = self.get_hit_y(self.x)
            
            if not self.is_paddle_hit(self.left_paddle_y, hit_y):
                self.left_missed = True
                self.x = 0.0
                self.y = hit_y
                return False

            self.x = -advance_x
            self.speed_x = -self.speed_x
        else:
            self.x = advance_x

        advance_y = self.y + delta_y
        if advance_y > SCREEN_HEIGHT:
            # Bounce from top
            remainder = advance_y - SCREEN_HEIGHT
            self.y = SCREEN_HEIGHT - remainder
            self.speed_y = -self.speed_y
        elif advance_y < 0.0:
            # Bounce from bottom
            self.y = -advance_y
            self.speed_y = -self.speed_y
        else:
            self.y = advance_y

        return True
