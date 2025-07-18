from States.State import State
from pybricks import ev3brick as brick
from pybricks.tools import print, StopWatch
from Model.ScreenCalculator import ScreenCalculator
from pybricks.parameters import Button
from Model.ScreenCalculator import ScreenCalculator, clamp
from Model.ScreenGeometry import *
import urandom

CALIBRATION_DUTY_LIMIT = 40.0
BALL_MOTOR_CALIBRATION_SPEED = 15.0

class BallCalibrationState(State):

    def __init__(self, ball_left_motor, ball_right_motor):
        super().__init__()
        self.ball_left_motor = ball_left_motor
        self.ball_right_motor = ball_right_motor
        self.watch = StopWatch()

    def on_enter(self):
        self.ball_left_motor.reset_angle()
        self.ball_right_motor.reset_angle()
        self.input_manager.add_brick_button_handler(Button.LEFT, self.left_motor_up, False)
        self.input_manager.add_brick_button_handler(Button.RIGHT, self.left_motor_down, False)
        self.input_manager.add_brick_button_handler(Button.UP, self.right_motor_up, False)
        self.input_manager.add_brick_button_handler(Button.DOWN, self.right_motor_down, False)

        self.input_manager.add_brick_button_handler(Button.CENTER, self.stop_calibration)

        self.is_running = True

        brick.display.clear()
        brick.display.text("ARROWS", (10, 40))
        brick.display.text("move ball to top center")
        brick.display.text("")
        brick.display.text("CENTER")
        brick.display.text("ready")

    def on_update(self, time, delta_time):
        return self.is_running

    def on_exit(self):
        # Ball is at top center after calibration
        ball_left_motor_start_angle, ball_right_motor_start_angle = ScreenCalculator.get_motor_angles(SCREEN_CENTER_X, SCREEN_MOVABLE_TOP)
        self.ball_left_motor.set_offset(ball_left_motor_start_angle)
        self.ball_right_motor.set_offset(ball_right_motor_start_angle)

        self.ball_left_motor.reset_angle()
        self.ball_right_motor.reset_angle()

        #print("ball start angle left " + str(ball_left_motor_start_angle) + " right " + str(ball_right_motor_start_angle))

        # Seed urandom
        seed = self.watch.time()
        urandom.seed(seed)
        #print("set urandom seed " + str(seed))


    def left_motor_up(self, delta_time):
        self.ball_left_motor.track_target_step(BALL_MOTOR_CALIBRATION_SPEED * delta_time)
        #print("left_motor target " + str(self.ball_left_motor.target))

    def left_motor_down(self, delta_time):
        self.ball_left_motor.track_target_step(-BALL_MOTOR_CALIBRATION_SPEED * delta_time)
        #print("left_motor target " + str(self.ball_left_motor.target))

    def right_motor_up(self, delta_time):
        self.ball_right_motor.track_target_step(BALL_MOTOR_CALIBRATION_SPEED * delta_time)
        #print("right_motor target " + str(self.ball_right_motor.target))

    def right_motor_down(self, delta_time):
        self.ball_right_motor.track_target_step(-BALL_MOTOR_CALIBRATION_SPEED * delta_time)
        #print("right_motor target " + str(self.ball_right_motor.target))

    def stop_calibration(self, _):
        self.is_running = False

