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
        self.x = SCREEN_CENTER_X
        self.y = SCREEN_CENTER_Y

        self.left_paddle_y = PADDLE_CENTER_Y
        self.right_paddle_y = PADDLE_CENTER_Y
        self.left_paddle_speed = 0.0
        self.right_paddle_speed = 0.0

    def randomize_speed_angle(self):
        # Limit angle to +-INITIAL_ANGLE_RANGE and either right or left side
        side = 0.0 if rand_float() < 0.5 else 1.0
        angle = -INITIAL_ANGLE_RANGE + 2.0 * INITIAL_ANGLE_RANGE * rand_float()
        speed_angle = angle + side * math.pi

        self.speed_x = BALL_SPEED * math.cos(speed_angle)
        self.speed_y = BALL_SPEED * math.sin(speed_angle)

    def set_left_paddle_y(self, left_y, delta_time):
        self.previous_left_paddle_y = self.left_paddle_y
        self.left_paddle_y = left_y
        if delta_time > 0:
            self.left_paddle_speed = (self.left_paddle_y - self.previous_left_paddle_y) / delta_time
        else:
            self.left_paddle_speed = 0.0

    def set_right_paddle_y(self, right_y, delta_time):
        self.previous_right_paddle_y = self.right_paddle_y
        self.right_paddle_y = right_y
        if delta_time > 0:
            self.right_paddle_speed = (self.right_paddle_y - self.previous_right_paddle_y) / delta_time
        else:
            self.right_paddle_speed = 0.0

    def is_paddle_hit(self, paddle_y, hit_y):
        # paddle_y and hit_y are in screen coordinates - account for offset between paddle y and screen y
        bottom_edge = paddle_y
        top_edge = bottom_edge + PADDLE_HEIGHT

        # Add ball radius as tolerance on both sides
        return bottom_edge - BALL_RADIUS <= hit_y and hit_y <= top_edge + BALL_RADIUS

    def get_hit_y(self, hit_delta_x):
        hit_delta_time = hit_delta_x / self.speed_x
        return self.y + hit_delta_time * self.speed_y

    def add_ball_hit_speed_increment(self):
        speed_angle = math.atan2(self.speed_y, self.speed_x)
        self.speed_x += BALL_SPEED_HIT_INCREMENT * math.cos(speed_angle)
        self.speed_y += BALL_SPEED_HIT_INCREMENT * math.sin(speed_angle)

    def update_state(self, delta_time):
        delta_x = delta_time * self.speed_x
        delta_y = delta_time * self.speed_y
        
        advance_x = self.x + delta_x
        if advance_x > SCREEN_MOVABLE_RIGHT:
            hit_y = self.get_hit_y(SCREEN_MOVABLE_RIGHT - self.x)
            
            if not self.is_paddle_hit(self.right_paddle_y, hit_y):
                self.right_missed = True
                self.x = SCREEN_MOVABLE_RIGHT
                self.y = hit_y
                return False

            remainder = advance_x - SCREEN_MOVABLE_RIGHT
            self.x = SCREEN_MOVABLE_RIGHT - remainder
            self.speed_x = -self.speed_x
            self.add_ball_hit_speed_increment()
            speed_y_hit_increment = self.right_paddle_speed * PADDLE_BALL_SPEED_IMPULSE
            self.speed_y += speed_y_hit_increment
        elif advance_x < SCREEN_MOVABLE_LEFT:
            hit_y = self.get_hit_y(self.x - SCREEN_MOVABLE_LEFT)
            
            if not self.is_paddle_hit(self.left_paddle_y, hit_y):
                self.left_missed = True
                self.x = SCREEN_MOVABLE_LEFT
                self.y = hit_y
                return False

            remainder = advance_x - SCREEN_MOVABLE_LEFT
            self.x = SCREEN_MOVABLE_LEFT - remainder
            self.speed_x = -self.speed_x
            self.add_ball_hit_speed_increment()
            speed_y_hit_increment = self.left_paddle_speed * PADDLE_BALL_SPEED_IMPULSE
            self.speed_y += speed_y_hit_increment
        else:
            self.x = advance_x

        advance_y = self.y + delta_y
        if advance_y > SCREEN_MOVABLE_TOP:
            # Bounce from top
            remainder = advance_y - SCREEN_MOVABLE_TOP
            self.y = SCREEN_MOVABLE_TOP - remainder
            self.speed_y = -self.speed_y
        elif advance_y < SCREEN_MOVABLE_BOTTOM:
            # Bounce from bottom
            remainder = advance_y - SCREEN_MOVABLE_BOTTOM
            self.y = SCREEN_MOVABLE_BOTTOM - remainder
            self.speed_y = -self.speed_y
        else:
            self.y = advance_y

        return True
