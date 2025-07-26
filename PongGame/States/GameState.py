from Model.ScreenCalculator import ScreenCalculator, clamp
from States.State import State
from pybricks.tools import print, wait
from Model.ScreenGeometry import *
from Model.ScreenCalculator import clamp_paddle_y

RESET_PADDLE_POSITION_SPEED = 200 # deg/sec

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
        #self.ball_left_motor.run_target(ball_left_motor_angle, RESET_PADDLE_POSITION_SPEED)
        #self.ball_right_motor.run_target(ball_right_motor_angle, RESET_PADDLE_POSITION_SPEED)

    """ Y in range [0, PADDLE_RANGE_Y] """
    def set_left_paddle_target(self, y):
        #print("set_left_paddle_target y " + str(y) + " scaled_y " + str(scaled_y) + " angle " + str(angle))
        angle = GameState.get_paddle_angle(y)
        self.paddle_left_motor.track_target(angle)

    """ Y in range [0, PADDLE_RANGE_Y] """
    def set_right_paddle_target(self, y):
        angle = GameState.get_paddle_angle(y)
        self.paddle_right_motor.track_target(angle)

    def run_left_paddle_target(self, y, speed, wait = False):
        angle = GameState.get_paddle_angle(y)
        self.paddle_left_motor.run_target(angle, speed, wait)

    def run_right_paddle_target(self, y, speed, wait = False):
        angle = GameState.get_paddle_angle(y)
        self.paddle_right_motor.run_target(angle, speed, wait)

    @staticmethod
    def get_paddle_angle(y):
        clamped_y = clamp_paddle_y(y)
        # Account for paddle pivot offset from screen bottom edge
        return ScreenCalculator.calculate_paddle_angle(clamped_y + PADDLE_PIVOT_OFFSET)

    def stop_ball_motors(self):
        self.ball_left_motor.motor.stop()
        self.ball_right_motor.motor.stop()

    def reset_to_initial_position(self):
        self.set_ball_target(SCREEN_CENTER_X, SCREEN_CENTER_Y)
        self.run_left_paddle_target(PADDLE_CENTER_Y, RESET_PADDLE_POSITION_SPEED)
        self.run_right_paddle_target(PADDLE_CENTER_Y, RESET_PADDLE_POSITION_SPEED)

        wait(500)
        self.stop_ball_motors()

