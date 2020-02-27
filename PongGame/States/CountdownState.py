from pybricks import ev3brick as brick
from pybricks.parameters import Button, Port, Color
from pybricks.tools import print, wait
from States.State import State

class CountdownState(State):
    def on_enter(self):
        brick.light(Color.RED)
        self.set_text("Get Ready")
        wait(500)
        brick.light(Color.BLACK)
        wait(500)

        brick.light(Color.YELLOW)
        self.set_text("Soon")
        wait(500)
        brick.light(Color.BLACK)
        wait(500)

        brick.light(Color.GREEN)
        self.set_text("Fight!")
        wait(500)
        brick.light(Color.BLACK)
        brick.display.clear()

    def set_text(self, text):
        brick.display.clear()
        brick.display.text(text, (20, 20))

    def on_update(self, time, delta_time):
        return False
