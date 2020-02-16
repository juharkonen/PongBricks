class State:
    def __init__(self):
        self.next_state = None
        # input_manager assigned from state runner before on_enter
        self.input_manager = None

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_update(self, time, delta_time):
        return True
