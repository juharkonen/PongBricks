from pybricks.parameters import Port
from States.PongGameState import PongGameState

class PvPGameState(PongGameState):

    def on_enter(self):
        super().on_enter()

        self.input_manager.add_touch_sensor_handler(Port.S2, self.on_left_paddle_down)
        self.input_manager.add_touch_sensor_handler(Port.S1, self.on_left_paddle_up)
        self.input_manager.add_touch_sensor_handler(Port.S3, self.on_right_paddle_down)
        self.input_manager.add_touch_sensor_handler(Port.S4, self.on_right_paddle_up)



