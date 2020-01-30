
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

    def run_until_stalled(self):
        self.motor.set_dc_settings(PADDLE_CALIBRATION_DUTY_LIMIT, 0)

        self.motor.run(self.stall_sign * 150)
        previous_angle = 123.0
        watch = StopWatch()
        t_prev = watch.time() / 1000.0
        stalled_time = 0.0
        while True:
            t = watch.time() / 1000.0
            dt = t - t_prev
            t_prev = t

            motor_angle = self.motor.angle()
            angle_delta = motor_angle - previous_angle
            previous_angle = motor_angle
            
            print("Angle " + str(motor_angle) + " Angle difference " + str(angle_delta)
                + " dt " + str(dt) + " stalled_time " + str(stalled_time))
            
            if  abs(angle_delta) < 1:
                stalled_time += dt
            else:
                stalled_time = 0.0
            
            if stalled_time > STALL_DURATION:
                break

        self.motor.set_dc_settings(100, 0)
        self.motor.run_angle(-self.stall_sign * 50, PADDLE_CALIBRATION_REVERSE_OFFSET, Stop.COAST, True)
        wait(200)
        self.motor.reset_angle(0)

