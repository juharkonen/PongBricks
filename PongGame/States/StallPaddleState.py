from States.State import State
from pybricks.tools import print
from pybricks.parameters import Stop

STALL_DURATION = 0.3
PADDLE_CALIBRATION_DUTY_LIMIT = 30.0
PADDLE_CALIBRATION_REVERSE_OFFSET = 26.0

class StallPaddleState(State):
    def __init__(self, motor, stall_sign):
        super().__init__()
        self.motor = motor
        self.stall_sign = stall_sign

    def on_enter(self):

        self.motor.set_dc_settings(PADDLE_CALIBRATION_DUTY_LIMIT, 0)
        self.motor.run(self.stall_sign * 150)

        self.previous_angle = 0.0
        self.stalled_time = 0.0

    def on_exit(self):
        self.motor.set_dc_settings(100, 0)
        self.motor.run_angle(-self.stall_sign * 50, PADDLE_CALIBRATION_REVERSE_OFFSET, Stop.COAST, True)
        self.motor.reset_angle(0)
        print("paddle stalled")

    def on_update(self, time, delta_time):
        motor_angle = self.motor.angle()
        angle_delta = motor_angle - self.previous_angle
        self.previous_angle = motor_angle
        
        #print("Angle " + str(motor_angle) + " Angle difference " + str(angle_delta)
        #    + " dt " + str(dt) + " stalled_time " + str(self.stalled_time))
        
        if  abs(angle_delta) < 1:
            self.stalled_time += delta_time
        else:
            self.stalled_time = 0.0
        
        if self.stalled_time > STALL_DURATION:
            self.motor.stop()
            return False
        
        return True
