from pybricks import ev3brick as brick
from pybricks.parameters import Button, Port, Color
from pybricks.tools import print, wait
from States.GameState import GameState

class CountdownState(GameState):
    def on_enter(self):
        brick.light(Color.RED)
        wait(500)
        brick.light(Color.BLACK)
        wait(500)
        brick.light(Color.YELLOW)
        wait(500)
        brick.light(Color.BLACK)
        wait(500)
        brick.light(Color.GREEN)
        wait(500)
        brick.light(Color.BLACK)

    def on_update(self, time, delta_time):
        return False
