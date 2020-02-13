from Model.ScreenCalculator import ScreenCalculator, clamp
from Model.ScreenGeometry import PADDLE_RANGE_Y
from States.State import State
from pybricks.tools import print

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
        print("set_left_paddle_target y " + str(y) + " angle " + str(angle))
        self.paddle_left_motor.track_target(angle)

    def set_right_paddle_target(self, y):
        angle = ScreenCalculator.calculate_right_paddle_angle(y)
        print("set_right_paddle_target y " + str(y) + " angle " + str(angle))
        self.paddle_right_motor.track_target(angle)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_update(self, time, delta_time):
        return True
