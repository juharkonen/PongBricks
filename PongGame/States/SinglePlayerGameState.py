from States.PongGameState import PongGameState
from Model.ScreenGeometry import AUTOPLAY_PADDLE_SPEED, PADDLE_RANGE_Y, PADDLE_HALF_RANGE_Y, PADDLE_HALF_HEIGHT
from Model.ScreenCalculator import clamp
from pybricks.parameters import Port

class SinglePlayerGameState(PongGameState):
    def on_enter(self):
        self.reset_to_initial_position()
        self.previous_clamped_target_y = PADDLE_HALF_RANGE_Y
        super().on_enter()

        self.input_manager.add_touch_sensor_handler(Port.S1, self.on_left_paddle_down)
        self.input_manager.add_touch_sensor_handler(Port.S2, self.on_left_paddle_up)

    def on_update(self, time, delta_time):
        target_y = clamp(self.pong.y - PADDLE_HALF_HEIGHT, 0, PADDLE_RANGE_Y)
        delta_y = target_y - self.previous_clamped_target_y
        max_delta_y = AUTOPLAY_PADDLE_SPEED * delta_time

        clamped_delta_y = clamp(delta_y, -max_delta_y, max_delta_y)
        clamped_target_y = self.previous_clamped_target_y + clamped_delta_y
        self.previous_clamped_target_y = clamped_target_y

        self.paddle_right_target_y = clamped_target_y

        return super().on_update(time, delta_time)