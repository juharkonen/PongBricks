
from Model.ScreenGeometry import *
from pybricks.ev3devices import Motor
from pybricks.tools import print, wait, StopWatch
from pybricks.parameters import Stop, Direction

PADDLE_CALIBRATION_DUTY_LIMIT = 30.0
PADDLE_CALIBRATION_REVERSE_OFFSET = 8.0
STALL_DURATION = 0.3

class MotorTracker:
    def __init__(self, port, gears, angle_offset = 0, direction = Direction.CLOCKWISE, change_direction_offset = 0):
        self.motor = Motor(port, direction, gears)
        self.target_angle = 0
        self.angle_offset = angle_offset

        self.change_direction_offset = change_direction_offset
        self.direction_offset = 0
        self.previous_angle = 0

    def set_offset(self, angle_offset):
        self.angle_offset = angle_offset

    def track_target(self, target_angle):
        angle = self.set_target_angle(target_angle)
        self.motor.track_target(angle + self.direction_offset)

    def track_target_step(self, step):
        self.track_target(self.target_angle + step)

    def run_target(self, target_angle, speed, wait = False):
        angle = self.set_target_angle(target_angle)
        self.motor.run_target(speed, angle, Stop.BRAKE, wait)

    def set_target_angle(self, target_angle):
        self.target_angle = target_angle
        angle = self.target_angle - self.angle_offset
        
        if angle > self.previous_angle:
            # Incrementing target, use zero offset
            self.direction_offset = 0
        elif angle < self.previous_angle:
            # Decrementing target, use negative offset
            self.direction_offset = -self.change_direction_offset
        # Else keep previous offset if angle unchanged
            



        self.previous_angle = angle
        return angle

    def reset_angle(self):
        self.motor.reset_angle(0)
