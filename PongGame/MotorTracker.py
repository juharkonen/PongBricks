
from Model.ScreenGeometry import *
from pybricks.ev3devices import Motor, Direction
from pybricks.tools import print, wait, StopWatch
from pybricks.parameters import Stop

PADDLE_CALIBRATION_DUTY_LIMIT = 30.0
PADDLE_CALIBRATION_REVERSE_OFFSET = 8.0
STALL_DURATION = 0.3

class MotorTracker:
    def __init__(self, port, gears, angle_offset):
        self.motor = Motor(port, Direction.CLOCKWISE, gears)
        self.target_angle = 0
        self.angle_offset = angle_offset

        

    def track_target_step(self, step):
        self.track_target(self.target + step)

    def track_target(self, target_angle):
        self.target_angle = target_angle
        angle = self.target_angle - self.angle_offset
        self.motor.track_target(angle)

    def reset_angle(self):
        self.motor.reset_angle(0)
