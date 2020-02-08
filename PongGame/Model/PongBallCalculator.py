from Model.ScreenGeometry import *
import math
#from random import random
import urandom

def randint(min, max):
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val

def randfloat():
    RANGE = 10000
    return randint(0, RANGE) / (1.0 * RANGE)

BALL_SPEED = 8

class PongBallCalculator:
    game_over = False
    speed_x = 1
    speed_y = 2
    speed_angle = math.pi / 4.0

    def reset_random(self, unit_random):
        angle = -math.pi + 2.0 * math.pi * unit_random
        self.reset(angle)

    def reset(self, angle):
        self.speed_angle = angle
        self.x = SCREEN_WIDTH / 2.0
        self.y = SCREEN_HEIGHT / 2.0
        self.speed_x = BALL_SPEED * math.cos(self.speed_angle)
        self.speed_y = BALL_SPEED * math.sin(self.speed_angle)

    def set_left_paddle_y(self, left_y):
        self.left_paddle_y = left_y
        pass

    def set_right_paddle_y(self, right_y):
        pass

    def is_right_paddle_hit(self, paddle_y, hit_y):
        bottom_edge = paddle_y - 0.5
        top_edge = bottom_edge + PADDLE_HEIGHT
        return bottom_edge <= hit_y and hit_y <= top_edge

    

    def update_state(self, delta_time):
        delta_x = delta_time * self.speed_x
        delta_y = delta_time * self.speed_y
        
        advance_x = self.x + delta_x
             # TODO: check for paddle positions on x bounce
        if advance_x > SCREEN_WIDTH:
            hit_delta_x = SCREEN_WIDTH - self.x
            hit_delta_time = hit_delta_x / self.speed_x
            hit_y = self.x + hit_delta_time * self.speed_y

            remainder = advance_x - SCREEN_WIDTH
            self.x = SCREEN_WIDTH - remainder
            self.speed_x = -self.speed_x
        elif advance_x < 0.0:
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