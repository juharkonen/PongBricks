from pybricks.tools import print, wait
from States.GameState import GameState
from Model.ScreenGeometry import SCREEN_MOVABLE_TOP, SCREEN_CENTER_X

class ExitState(GameState):
    def on_enter(self):
        print("Restoring calibration position")
        self.set_ball_target(SCREEN_CENTER_X, SCREEN_MOVABLE_TOP)
        self.set_left_paddle_target(0.0)
        self.set_right_paddle_target(0.0)
        wait(1000)
        print("Over and out")
    
    def on_update(self, time, delta_time):
        return False
