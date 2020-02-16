from pybricks import ev3brick as brick
from pybricks.parameters import Button, Port
from States.GameState import GameState
from Model.ScreenGeometry import PADDLE_SPEED, PADDLE_RANGE_Y, PADDLE_HALF_RANGE_Y, SCREEN_HEIGHT, SCREEN_WIDTH
from Model.ScreenCalculator import clamp
from Model.PongBallCalculator import PongBallCalculator
from pybricks.tools import print

class PvPGameState(GameState):
    pong = PongBallCalculator()
    
    def __init__(self, input_manager):
        self.input_manager = input_manager

    def on_enter(self):
        self.input_manager.add_touch_sensor_handler(Port.S1, self.left_paddle_down)
        self.input_manager.add_touch_sensor_handler(Port.S2, self.left_paddle_up)
        self.input_manager.add_touch_sensor_handler(Port.S3, self.right_paddle_down)
        self.input_manager.add_touch_sensor_handler(Port.S4, self.right_paddle_up)

        # DEBUG - exit on CENTER
        self.input_manager.add_brick_button_handler(Button.CENTER, self.exit)

        self.paddle_left_target_y = PADDLE_HALF_RANGE_Y
        self.paddle_right_target_y = PADDLE_HALF_RANGE_Y

        self.pong.randomize_speed_angle()

        self.reset_to_initial_position()

        self.is_running = True

    def on_exit(self):
        self.input_manager.clear_handlers()
        x = SCREEN_WIDTH / 2.0
        y = SCREEN_HEIGHT
        self.set_ball_target(x, y)

    def on_update(self, time, delta_time):
        self.pong.update_state(delta_time)
        self.set_ball_target(self.pong.x, self.pong.y)

        self.set_left_paddle_target(self.paddle_left_target_y)
        self.set_right_paddle_target(self.paddle_right_target_y)
        return self.is_running

    def exit(self, delta_time):
        self.is_running = False

    def left_paddle_up(self, delta_time):
        delta = PADDLE_SPEED * delta_time
        self.paddle_left_target_y = clamp(self.paddle_left_target_y + delta, 0, PADDLE_RANGE_Y)
        print("left target " + str(self.paddle_left_target_y))

        self.set_left_paddle_target(self.paddle_left_target_y)

    def left_paddle_down(self, delta_time):
        delta = -PADDLE_SPEED * delta_time
        self.paddle_left_target_y = clamp(self.paddle_left_target_y + delta, 0, PADDLE_RANGE_Y)
        print("left target " + str(self.paddle_left_target_y))

        self.set_left_paddle_target(self.paddle_left_target_y)

    def right_paddle_up(self, delta_time):
        delta = PADDLE_SPEED * delta_time
        self.paddle_right_target_y = clamp(self.paddle_right_target_y + delta, 0, PADDLE_RANGE_Y)
        print("right target " + str(self.paddle_right_target_y))

        self.set_right_paddle_target(self.paddle_right_target_y)

    def right_paddle_down(self, delta_time):
        delta = -PADDLE_SPEED * delta_time
        self.paddle_right_target_y = clamp(self.paddle_right_target_y + delta, 0, PADDLE_RANGE_Y)
        print("right target " + str(self.paddle_right_target_y))

        self.set_right_paddle_target(self.paddle_right_target_y)
