from Model.ScreenCalculator import ScreenCalculator, clamp
from States.State import State
from pybricks.tools import print
from Model.ScreenGeometry import *

PADDLE_SCALE_FACTOR = 1.08

def str(number):
    return "{:.2f}".format(number)

class GameState(State):
    def set_motors(self, paddle_left_motor, paddle_right_motor, ball_left_motor, ball_right_motor):
        self.paddle_left_motor = paddle_left_motor
        self.paddle_right_motor = paddle_right_motor
        self.ball_left_motor = ball_left_motor
        self.ball_right_motor = ball_right_motor

    def set_ball_target(self, x, y):
        #print("set_ball_target " + str(x) + " " + str(y))
        ball_left_motor_angle, ball_right_motor_angle = ScreenCalculator.get_motor_angles(x, y)
        self.ball_left_motor.track_target(ball_left_motor_angle)
        self.ball_right_motor.track_target(ball_right_motor_angle)

    def set_left_paddle_target(self, y):
        scaled_y = PADDLE_SCALE_FACTOR * y
        angle = ScreenCalculator.calculate_left_paddle_angle(scaled_y)
        #print("set_left_paddle_target y " + str(y) + " scaled_y " + str(scaled_y) + " angle " + str(angle))
        self.paddle_left_motor.track_target(angle)

    def set_right_paddle_target(self, y):
        scaled_y = PADDLE_SCALE_FACTOR * y
        angle = ScreenCalculator.calculate_right_paddle_angle(scaled_y)
        #print("set_right_paddle_target y " + str(y) + " scaled_y " + str(scaled_y) + " angle " + str(angle))
        self.paddle_right_motor.track_target(angle)

    def reset_to_initial_position(self):
        self.set_ball_target(SCREEN_CENTER_X, SCREEN_CENTER_Y)
        self.set_left_paddle_target(PADDLE_CENTER_Y)
        self.set_right_paddle_target(PADDLE_CENTER_Y)
