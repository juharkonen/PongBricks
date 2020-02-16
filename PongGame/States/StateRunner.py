from pybricks.tools import print, wait, StopWatch
from InputManager import InputManager

class StateRunner:

    def __init__(self):
        self.watch = StopWatch()
        self.input_manager = InputManager()
        self.first_state = None
        self.state = None
        self.last_state = None
        
    def append_state(self, state):
        print("Appending state " + type(state).__name__)
        state.next_state = None
        if self.state == None:
            self.first_state = state
            self.state = state
            self.last_state = state
        else:
            self.last_state.next_state = state
            self.last_state = state

    def setup_state(self, state):
        print("Entering state " + type(state).__name__)

        self.state = state
        state.input_manager = self.input_manager
        state.on_enter()

        self.watch.reset()
        self.previous_time = 0.0
        self.time = 0.0

    def setup_first_state(self):
        self.setup_state(self.first_state)

    def update_state(self):
        self.time = self.watch.time() / 1000.0
        delta_time = self.time - self.previous_time
        self.previous_time = self.time
        
        self.input_manager.update(delta_time)

        if not self.state.on_update(self.time, delta_time):
            print("Exiting state " + type(self.state).__name__)
            self.state.on_exit()
            self.input_manager.clear_handlers()
            if self.state.next_state != None:
                self.setup_state(self.state.next_state)
            else:
                return False

        return True

    def run_state(self, state):
        self.setup_state(state)
        
        while self.update_state():
            continue
