from Model.ScreenCalculator import ScreenCalculator, clamp
from Model.ScreenGeometry import PADDLE_RANGE_Y
from States.State import State
from pybricks.tools import print
from Model.ScreenGeometry import PADDLE_HALF_RANGE_Y, SCREEN_HEIGHT, SCREEN_WIDTH

def str(number):
    return "{:.2f}".format(number)

class GameState(State):
    def set_motors(self, paddle_left_motor, paddle_right_motor, ball_left_motor, ball_right_motor):
        self.paddle_left_motor = paddle_left_motor
        self.paddle_right_motor = paddle_right_motor
        self.ball_left_motor = ball_left_motor
        self.ball_right_motor = ball_right_motor

    def set_ball_target(self, x, y):
        ball_left_motor_angle, ball_right_motor_angle = ScreenCalculator.get_motor_angles(x, y)
        self.ball_left_motor.track_target(ball_left_motor_angle)
        self.ball_right_motor.track_target(ball_right_motor_angle)

    def set_left_paddle_target(self, y):
        angle = ScreenCalculator.calculate_left_paddle_angle(y)
        #print("set_left_paddle_target y " + str(y) + " angle " + str(angle))
        self.paddle_left_motor.track_target(angle)

    def set_right_paddle_target(self, y):
        angle = ScreenCalculator.calculate_right_paddle_angle(y)
        #print("set_right_paddle_target y " + str(y) + " angle " + str(angle))
        self.paddle_right_motor.track_target(angle)

    def reset_to_initial_position(self):
        self.set_ball_target(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0)
        self.set_left_paddle_target(PADDLE_HALF_RANGE_Y)
        self.set_right_paddle_target(PADDLE_HALF_RANGE_Y)

