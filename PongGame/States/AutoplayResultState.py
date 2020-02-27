from pybricks import ev3brick as brick
from pybricks.parameters import Button
from pybricks.tools import print, wait
from States.PongGameState import PongGameState

class AutoplayResultState(PongGameState):
    def __init__(self):
        super().__init__(None)
        self.winner_number = -1

    def set_winner_number(self, winner_number):
        self.winner_number = winner_number

    def on_enter(self):
        brick.display.clear()
        brick.display.text("Player " + str(self.winner_number) + " Wins", (40, 20))
        wait(1000)
        self.reset_to_initial_position()

    def on_update(self, time, delta_time):
        return False
