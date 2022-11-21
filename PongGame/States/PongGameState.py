from pybricks.parameters import Button
from States.GameState import GameState
from Model.PongBallCalculator import PongBallCalculator
from Model.ScreenGeometry import PADDLE_SPEED, PADDLE_CENTER_Y
from Model.ScreenCalculator import clamp_paddle_y
from pybricks.tools import print

class PongGameState(GameState):
    def __init__(self, result_state):
        super().__init__()
        self.result_state = result_state
        self.pong = PongBallCalculator()

    def on_enter(self):
        self.paddle_left_target_y = PADDLE_CENTER_Y
        self.paddle_right_target_y = PADDLE_CENTER_Y

        self.pong.reset()

        # DEBUG - exit on CENTER
        self.input_manager.add_brick_button_handler(Button.CENTER, self.on_stop)

        self.is_running = True

    def on_update(self, time, delta_time):
        # Update pong state
        self.pong.set_left_paddle_y(self.paddle_left_target_y, delta_time)
        self.pong.set_right_paddle_y(self.paddle_right_target_y, delta_time)
        continue_game = self.pong.update_state(delta_time)

        # Update graphics
        self.set_ball_target(self.pong.x, self.pong.y)
        self.set_left_paddle_target(self.paddle_left_target_y)
        self.set_right_paddle_target(self.paddle_right_target_y)

        return self.is_running and continue_game

    def on_exit(self):
        if self.result_state != None:
            winner_number = 2 if self.pong.left_missed else 1
            self.result_state.set_winner_number(winner_number)

    def on_stop(self, delta_time):
        self.is_running = False

    def on_left_paddle_up(self, delta_time):
        delta = PADDLE_SPEED * delta_time
        self.paddle_left_target_y = clamp_paddle_y(self.paddle_left_target_y + delta)
        #print("left target " + str(self.paddle_left_target_y))

        self.set_left_paddle_target(self.paddle_left_target_y)

    def on_left_paddle_down(self, delta_time):
        delta = -PADDLE_SPEED * delta_time
        self.paddle_left_target_y = clamp_paddle_y(self.paddle_left_target_y + delta)
        #print("left target " + str(self.paddle_left_target_y))

        self.set_left_paddle_target(self.paddle_left_target_y)

    def on_right_paddle_up(self, delta_time):
        delta = PADDLE_SPEED * delta_time
        self.paddle_right_target_y = clamp_paddle_y(self.paddle_right_target_y + delta)
        #print("right target " + str(self.paddle_right_target_y))

        self.set_right_paddle_target(self.paddle_right_target_y)

    def on_right_paddle_down(self, delta_time):
        delta = -PADDLE_SPEED * delta_time
        self.paddle_right_target_y = clamp_paddle_y(self.paddle_right_target_y + delta)
        #print("right target " + str(self.paddle_right_target_y))

        self.set_right_paddle_target(self.paddle_right_target_y)