from pybricks import ev3brick as brick
from pybricks.parameters import Button
from pybricks.tools import print
from States.State import State

class GameModeMenuState(State):
    def __init__(self, input_manager, autoplay_state, single_player_state, pvp_state, exit_state):
        self.input_manager = input_manager
        self.states = [autoplay_state, single_player_state, pvp_state, exit_state]
        self.state_names = ["Autoplay", "Single Player", "PvP", "Exit"]
        self.state_index = 0

        autoplay_state.next_state = self
        single_player_state.next_state = self
        pvp_state.next_state = self
        exit_state.next_state = None

    def on_enter(self):
        self.input_manager.add_brick_button_handler(Button.LEFT, self.select_previous)
        self.input_manager.add_brick_button_handler(Button.RIGHT, self.select_next)
        self.input_manager.add_brick_button_handler(Button.CENTER, self.apply)
        self.update_display()
        self.running = True

    def on_update(self, time, delta_time):
        return self.running

    def update_display(self):
        brick.display.clear()
        brick.display.text("< >", (60, 20))
        brick.display.text("change mode")
        brick.display.text("CENTER")
        brick.display.text("select")
        brick.display.text(self.state_names[self.state_index])

    def on_exit(self):
        self.next_state = self.states[self.state_index]
        self.input_manager.clear_handlers()

    def select_previous(self, delta_time):
        self.state_index = (self.state_index - 1) % len(self.states)
        print("state index " + str(self.state_index))
        self.update_display()
    
    def select_next(self, delta_time):
        self.state_index = (self.state_index + 1) % len(self.states)
        print("state index " + str(self.state_index))
        self.update_display()
    
    def apply(self, delta_time):
        self.running = False
