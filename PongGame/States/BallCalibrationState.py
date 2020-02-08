from pybricks.tools import print
from Model.ScreenCalculator import ScreenCalculator
from pybricks.parameters import (Button)
CALIBRATION_DUTY_LIMIT = 40.0

class BallCalibrationState:
    def __init__(self, input_manager, left_motor, right_motor):
        self.input_manager = input_manager
        self.left_motor = left_motor
        self.right_motor = right_motor

    def on_enter(self):
        self.input_manager.add_brick_button_handler(Button.LEFT, self.left_motor_up)
        self.input_manager.add_brick_button_handler(Button.RIGHT, self.left_motor_down)
        self.input_manager.add_brick_button_handler(Button.UP, self.right_motor_up)
        self.input_manager.add_brick_button_handler(Button.DOWN, self.right_motor_down)

        self.input_manager.add_brick_button_handler(Button.CENTER, self.stop_calibration)

        self.is_calibrating = True
        print("Ball calibration: press CENTER complete")

    def on_update(self, time, delta_time):
        return self.is_calibrating

    def on_exit(self):
        self.left_motor.reset_angle()
        self.right_motor.reset_angle()

        self.input_manager.clear_handlers()
        #print("Ball calibration completed")

    def left_motor_up(self, delta_time):
        self.left_motor.track_target_step(delta_time)
        print("left_motor target " + str(self.left_motor.target))

    def left_motor_down(self, delta_time):
        self.left_motor.track_target_step(-delta_time)
        print("left_motor target " + str(self.left_motor.target))

    def right_motor_up(self, delta_time):
        self.right_motor.track_target_step(delta_time)
        print("right_motor target " + str(self.right_motor.target))

    def right_motor_down(self, delta_time):
        self.right_motor.track_target_step(-delta_time)
        print("right_motor target " + str(self.right_motor.target))

    def stop_calibration(self, _):
        self.is_calibrating = False

