from pybricks import ev3brick as brick
from pybricks.parameters import Button
from pybricks.tools import print
from States.State import State

class GameResultState(State):
    def __init__(self):
        super().__init__()
        self.winner_number = -1
        self.is_running = False

    def set_winner_number(self, winner_number):
        self.winner_number = winner_number

    def on_enter(self):
        brick.display.clear()
        brick.display.text("Player " + str(self.winner_number) + " Wins", (40, 20))
        self.input_manager.add_brick_button_handler(Button.CENTER, self.on_stop)

        # Skip result state if error is set
        self.is_running = not self.is_error

    def on_exit(self):
        self.is_running = False

    def on_update(self, time, delta_time):
        return self.is_running
    
    def on_stop(self, delta_time):
        self.is_running = False
        self.is_error = False
    
    def set_error(self):
        self.is_error = True



