class AndState:
    def __init__(self, states):
        self.states = states
        self.completed_states = []

    def on_enter(self):
        for state in self.states:
            state.on_enter()

    def on_exit(self):
        pass

    def on_update(self, time, delta_time):
        for state in self.states:
            if state in self.completed_states:
                continue

            if not state.on_update(time, delta_time):
                state.on_exit()
                self.completed_states.append(state)
        
        return len(self.completed_states) < len(self.states)