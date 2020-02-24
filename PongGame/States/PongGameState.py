from States.GameState import GameState
from Model.PongBallCalculator import PongBallCalculator
from Model.ScreenGeometry import PADDLE_SPEED, PADDLE_RANGE_Y, PADDLE_HALF_RANGE_Y, SCREEN_HEIGHT, SCREEN_WIDTH
from Model.ScreenCalculator import clamp

class PongGameState(GameState):
    def __init__(self, result_state):
        super().__init__()
        self.result_state = result_state
        self.pong = PongBallCalculator()

    def on_enter(self):
        self.paddle_left_target_y = PADDLE_HALF_RANGE_Y
        self.paddle_right_target_y = PADDLE_HALF_RANGE_Y

        self.pong.reset()

    def on_exit(self):
        winner_number = 2 if self.pong.left_missed else 1
        self.result_state.set_winner_number(winner_number)

    def on_left_paddle_up(self, delta_time):
        delta = PADDLE_SPEED * delta_time
        self.paddle_left_target_y = clamp(self.paddle_left_target_y + delta, 0, PADDLE_RANGE_Y)
        #print("left target " + str(self.paddle_left_target_y))

        self.set_left_paddle_target(self.paddle_left_target_y)

    def on_left_paddle_down(self, delta_time):
        delta = -PADDLE_SPEED * delta_time
        self.paddle_left_target_y = clamp(self.paddle_left_target_y + delta, 0, PADDLE_RANGE_Y)
        #print("left target " + str(self.paddle_left_target_y))

        self.set_left_paddle_target(self.paddle_left_target_y)

    def on_right_paddle_up(self, delta_time):
        delta = PADDLE_SPEED * delta_time
        self.paddle_right_target_y = clamp(self.paddle_right_target_y + delta, 0, PADDLE_RANGE_Y)
        #print("right target " + str(self.paddle_right_target_y))

        self.set_right_paddle_target(self.paddle_right_target_y)

    def on_right_paddle_down(self, delta_time):
        delta = -PADDLE_SPEED * delta_time
        self.paddle_right_target_y = clamp(self.paddle_right_target_y + delta, 0, PADDLE_RANGE_Y)
        #print("right target " + str(self.paddle_right_target_y))

        self.set_right_paddle_target(self.paddle_right_target_y)