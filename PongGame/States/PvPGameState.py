from States.State import State
from pybricks import ev3brick as brick
from pybricks.parameters import Button

class PvPGameState(State):
    def __init__(self, input_manager):
        self.input_manager = input_manager

    def on_enter(self):
        self.input_manager.add_brick_button_handler(Button.CENTER, self.exit)
        brick.display.clear()
        brick.display.text("CENTER", (60, 50))
        brick.display.text(" menu")
        self.is_running = True

    def on_exit(self):
        self.input_manager.clear_handlers()
        ## TODO: move ball to center

    def on_update(self, time, delta_time):
        return self.is_running

    def exit(self):
        self.is_running = False
