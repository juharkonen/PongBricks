from pybricks import ev3brick as brick
from pybricks.ev3devices import TouchSensor

class TouchSensorHandler:
    def __init__(self, port, action):
        self.touch_sensor = TouchSensor(port)
        self.action = action
    
    def Update(self, delta_tme):
        if self.touch_sensor.pressed():
            self.action(delta_tme)

class BrickButtonPressHandler:
    def __init__(self, button, action, track_state_change):
        self.button = button
        self.action = action
        self.track_state_change = track_state_change
        self.previous_buttons = brick.buttons()

    def Update(self, delta_tme):
        current_buttons = brick.buttons()
        if self.track_state_change:
            if self.button in current_buttons and not self.button in self.previous_buttons:
                self.action(delta_tme)        
            self.previous_buttons = current_buttons
            pass
        else:
            if self.button in current_buttons:
                self.action(delta_tme)        

class InputManager:
    def __init__(self):
        self.handlers = []

    def add_brick_button_handler(self, button, action, track_state_change = True):
        handler = BrickButtonPressHandler(button, action, track_state_change)
        self.handlers.append(handler)

    def add_touch_sensor_handler(self, port, action):
        handler = TouchSensorHandler(port, action)
        self.handlers.append(handler)
    
    def clear_handlers(self):
        self.handlers = []

    def update(self, delta_tme):
        for handler in self.handlers:
            handler.Update(delta_tme)
