from Model.ScreenGeometry import *
import math

"""
Paddle coordinates: origin half a stud above screen bottom where the arm is attached
"""

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def clamp_paddle_y(target_y):
    return clamp(target_y, 0, PADDLE_RANGE_Y)

"""
screen coordinates: origin in bottom left, one unit is one stud (20 LDU)
motor coordinates: origin on motor 1 axle

Movable ball coordinates are offset from the edges by ball radius.
"""
class ScreenCalculator:

    @staticmethod
    def screen_to_motor_coordinates(x_screen, y_screen):
        return x_screen + SCREEN_TO_MOTOR1_OFFSET_X, y_screen + SCREEN_TO_MOTOR1_OFFSET_Y

    @staticmethod
    def distance(x, y, a, b):
        dx = x - a
        dy = y - b
        return math.sqrt(dx*dx + dy*dy)

    @staticmethod
    def calculate_right_paddle_angle(y):
        delta_y = y - PADDLE_MOTOR_Y
        r1 = PADDLE_ARM1
        r2 = PADDLE_ARM2
        r = r1 + r2

        r3 = math.sqrt(PADDLE_MOTOR_X*PADDLE_MOTOR_X + delta_y*delta_y)
        if r3 >= r:
            # outside range - reach to max height
            gamma = 0
        else:
            denominator = r1*r1 + r3*r3 - r2*r2
            nominator = 2 * r1 * r3
            gamma = math.acos(denominator / nominator)

        beta = math.acos(PADDLE_MOTOR_X / r3)

        return -math.degrees(gamma - beta)

    @staticmethod
    def calculate_left_paddle_angle(y):
        return 180 - ScreenCalculator.calculate_right_paddle_angle(y)

    @staticmethod
    def calculate_motor_angle(x, y, a, b):
        r1 = BALL_ARM_R1
        r2 = BALL_ARM_R2
        r3 = ScreenCalculator.distance(x, y, a, b)
        denominator = r1*r1 + r3*r3 - r2*r2
        nominator = 2 * r1 * r3
        gamma_ratio = clamp(denominator / nominator, -1.0, 1.0)
        gamma = math.acos(gamma_ratio)
        beta_ratio = clamp((x - a) / r3, -1.0, 1.0)
        beta = math.acos(beta_ratio)
        return beta, gamma
    
    @staticmethod
    def get_motor_angles(x_screen, y_screen):
        # Get motor coordinates
        x, y = ScreenCalculator.screen_to_motor_coordinates(x_screen, y_screen)
        m1_beta, m1_gamma = ScreenCalculator.calculate_motor_angle(x, y, 0, 0)
        m2_beta, m2_gamma = ScreenCalculator.calculate_motor_angle(x, y, BALL_MOTOR2_X, 0)
        return math.degrees(m1_beta + m1_gamma), math.degrees(m2_beta - m2_gamma)


    
