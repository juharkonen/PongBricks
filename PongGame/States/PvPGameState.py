from pybricks import ev3brick as brick
from pybricks.parameters import Button, Port
from pybricks.tools import print
from Model.ScreenGeometry import PADDLE_SPEED, PADDLE_RANGE_Y, PADDLE_HALF_RANGE_Y, SCREEN_HEIGHT, SCREEN_WIDTH
from Model.PongBallCalculator import PongBallCalculator
from States.PongGameState import PongGameState

class PvPGameState(PongGameState):

    def on_enter(self):
        super().on_enter()

        self.input_manager.add_touch_sensor_handler(Port.S1, self.on_left_paddle_down)
        self.input_manager.add_touch_sensor_handler(Port.S2, self.on_left_paddle_up)
        self.input_manager.add_touch_sensor_handler(Port.S3, self.on_right_paddle_down)
        self.input_manager.add_touch_sensor_handler(Port.S4, self.on_right_paddle_up)

        # DEBUG - exit on CENTER
        self.input_manager.add_brick_button_handler(Button.CENTER, self.on_stop)

        self.paddle_left_target_y = PADDLE_HALF_RANGE_Y
        self.paddle_right_target_y = PADDLE_HALF_RANGE_Y

        self.pong.reset()

        self.is_running = True

    def on_update(self, time, delta_time):
        self.pong.set_left_paddle_y(self.paddle_left_target_y)
        self.pong.set_right_paddle_y(self.paddle_right_target_y)

        continue_game = self.pong.update_state(delta_time)
        
        self.set_ball_target(self.pong.x, self.pong.y)
        self.set_left_paddle_target(self.paddle_left_target_y)
        self.set_right_paddle_target(self.paddle_right_target_y)

        return self.is_running and continue_game

    def on_stop(self, delta_time):
        self.is_running = False

