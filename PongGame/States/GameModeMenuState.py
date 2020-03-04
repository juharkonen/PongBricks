from pybricks import ev3brick as brick
from pybricks.parameters import Button
from pybricks.tools import print
from States.GameState import GameState

class GameModeMenuState(GameState):
    def __init__(self, autoplay_state, single_player_state, pvp_state, exit_state):
        super().__init__()
        self.states = [autoplay_state, single_player_state, pvp_state, exit_state]
        self.state_names = ["Autoplay", "Single Player", "PvP", "Exit"]
        self.state_index = 0

        autoplay_state.next_state = self
        single_player_state.next_state = self
        pvp_state.next_state = self
        exit_state.next_state = None

    def on_enter(self):
        self.reset_to_initial_position()

        self.input_manager.add_brick_button_handler(Button.UP, self.select_previous)
        self.input_manager.add_brick_button_handler(Button.DOWN, self.select_next)
        self.input_manager.add_brick_button_handler(Button.CENTER, self.apply)
        self.update_display()
        self.is_running = True

    def on_update(self, time, delta_time):
        return self.is_running

    def update_display(self):
        brick.display.clear()
        brick.display.text("MENU", (20, 20))
        brick.display.text("")

        for state_index in range(len(self.state_names)):
            state_name = self.state_names[state_index]
            prefix = "* " if state_index == self.state_index else "  "
            brick.display.text(prefix + state_name)

        brick.display.text("")
        brick.display.text("CENTER = select")

    def on_exit(self):
        self.next_state = self.states[self.state_index]

    def select_previous(self, delta_time):
        self.state_index = (self.state_index - 1) % len(self.states)
        #print("state index " + str(self.state_index))
        self.update_display()
    
    def select_next(self, delta_time):
        self.state_index = (self.state_index + 1) % len(self.states)
        #print("state index " + str(self.state_index))
        self.update_display()
    
    def apply(self, delta_time):
        self.is_running = False
