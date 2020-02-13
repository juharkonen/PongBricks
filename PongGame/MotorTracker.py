
from Model.ScreenGeometry import *
from pybricks.ev3devices import Motor
from pybricks.tools import print, wait, StopWatch
from pybricks.parameters import Stop

PADDLE_CALIBRATION_DUTY_LIMIT = 30.0
PADDLE_CALIBRATION_REVERSE_OFFSET = 8.0
STALL_DURATION = 0.3

class MotorTracker:
    def __init__(self, port, scale, offset):
        self.motor = Motor(port)
        self.target = 0
        self.set_transform(scale, offset)

    def set_transform(self, scale, offset):
        self.scale = scale
        self.offset = offset

    def track_target_step(self, step):
        self.track_target(self.target + step)

    def track_target(self, target):
        self.target = target
        angle = self.scale * (self.target - self.offset)
        self.motor.track_target(angle)

    def reset_angle(self):
        self.motor.reset_angle(0)

class PaddleMotorTracker(MotorTracker):
    def __init__(self, port, scale, offset, stall_sign):
        self.stall_sign = stall_sign
        super().__init__(port, scale, offset)

