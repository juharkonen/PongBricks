from States.PongGameState import PongGameState
from Model.ScreenGeometry import AUTOPLAY_PADDLE_SPEED, PADDLE_RANGE_Y, PADDLE_HALF_RANGE_Y, PADDLE_HALF_HEIGHT
from Model.ScreenCalculator import clamp

class AutoplayGameState(PongGameState):
    def on_enter(self):
        self.reset_to_initial_position()
        self.previous_limited_target_y = PADDLE_HALF_RANGE_Y
        super().on_enter()

    def on_update(self, time, delta_time):
        target_y = clamp(self.pong.y - PADDLE_HALF_HEIGHT, 0, PADDLE_RANGE_Y)
        delta_y = target_y - self.previous_limited_target_y
        max_delta_y = AUTOPLAY_PADDLE_SPEED * delta_time

        # Limit paddle movement speed
        limited_delta_y = delta_y
        if delta_y > max_delta_y:
            limited_delta_y = max_delta_y
        elif delta_y < -max_delta_y:
            limited_delta_y = -max_delta_y

        limited_target_y = self.previous_limited_target_y + limited_delta_y
        self.previous_limited_target_y = limited_target_y

        self.paddle_left_target_y = limited_target_y
        self.paddle_right_target_y = limited_target_y

        return super().on_update(time, delta_time)