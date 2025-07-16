from pybricks.parameters import Port
from States.PongGameState import PongGameState

class PvPGameState(PongGameState):

    def on_enter(self):
        super().on_enter()

        if not self.try_add_touch_sensor(Port.S1, "S1", self.on_left_paddle_up):
            return

        if not self.try_add_touch_sensor(Port.S2, "S2", self.on_left_paddle_down):
            return

        if not self.try_add_touch_sensor(Port.S3, "S3", self.on_right_paddle_down):
            return

        if not self.try_add_touch_sensor(Port.S4, "S4", self.on_right_paddle_up):
            return
