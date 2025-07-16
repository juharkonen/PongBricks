from States.PongGameState import PongGameState
from States.GameState import GameState
from Model.ScreenGeometry import AUTOPLAY_PADDLE_SPEED, PADDLE_CENTER_Y, PADDLE_HALF_HEIGHT
from Model.ScreenCalculator import clamp, clamp_paddle_y
from pybricks.parameters import Port

class SinglePlayerGameState(PongGameState):
    def on_enter(self):
        self.reset_to_initial_position()
        self.previous_clamped_target_y = PADDLE_CENTER_Y
        super().on_enter()

        if not self.try_add_touch_sensor(Port.S1, "S1", self.on_left_paddle_up):
            return

        if not self.try_add_touch_sensor(Port.S2, "S2", self.on_left_paddle_down):
            return

    def on_update(self, time, delta_time):
        target_y = clamp_paddle_y(self.pong.y - PADDLE_HALF_HEIGHT)
        delta_y = target_y - self.previous_clamped_target_y
        max_delta_y = AUTOPLAY_PADDLE_SPEED * delta_time

        clamped_delta_y = clamp(delta_y, -max_delta_y, max_delta_y)
        clamped_target_y = self.previous_clamped_target_y + clamped_delta_y
        self.previous_clamped_target_y = clamped_target_y

        self.paddle_right_target_y = clamped_target_y

        return super().on_update(time, delta_time)