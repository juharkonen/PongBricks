from States.StateRunner import StateRunner
from States.State import State

class NestedState(State):
    runner = StateRunner()

    def append_state(self, state):
        self.runner.append_state(state)

    def on_enter(self):
        self.runner.setup_first_state()

    def on_update(self, time, delta_time):
        return self.runner.update_state()
