from States.State import State
from pybricks.tools import print
from pybricks.parameters import Stop
from pybricks.tools import print, wait

STALL_DURATION = 0.3
PADDLE_CALIBRATION_DUTY_LIMIT = 30.0
PADDLE_CALIBRATION_REVERSE_OFFSET = 3.0

class StallPaddleState(State):
    def __init__(self, motor):
        super().__init__()
        self.motor = motor

    def on_enter(self):
        self.motor.set_dc_settings(PADDLE_CALIBRATION_DUTY_LIMIT, 0)
        self.motor.run(150)
        self.stalled_time = 0.0

    def on_exit(self):
        print("paddle stalled")

        # Wait for angle to stabilize before resetting
        wait(500)
        self.motor.reset_angle(0)

        self.motor.run_angle(50, -PADDLE_CALIBRATION_REVERSE_OFFSET, Stop.COAST, True)
        self.motor.set_dc_settings(100, 0)

    def on_update(self, time, delta_time):
        motor_angle = self.motor.angle()
        
        if self.motor.stalled():
            self.stalled_time += delta_time
        else:
            self.stalled_time = 0.0
        
        if self.stalled_time > STALL_DURATION:
            self.motor.stop()
            return False
        
        return True
