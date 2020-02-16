from States.State import State

class AndState(State):
    def __init__(self, states):
        super().__init__()
        self.states = states
        self.completed_states = []

    def on_enter(self):
        for state in self.states:
            state.on_enter()

    def on_update(self, time, delta_time):
        for state in self.states:
            if state in self.completed_states:
                continue

            if not state.on_update(time, delta_time):
                state.on_exit()
                self.completed_states.append(state)
        
        return len(self.completed_states) < len(self.states)