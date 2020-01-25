from pybricks import ev3brick as brick
from pybricks.ev3devices import TouchSensor

class TouchSensorHandler:
    def __init__(self, port, action):
        self.touch_sensor = TouchSensor(port)
        self.action = action
    
    def Update(self, delta_tme):
        if self.touch_sensor.pressed():
            self.action(delta_tme)

class BrickButtonHandler:
    def __init__(self, button, action):
        self.button = button
        self.action = action

    def Update(self, delta_tme):
        if self.button in brick.buttons():
            self.action(delta_tme)        

class InputManager:
    handlers = []

    def add_brick_button_handler(self, button, action):
        handler = BrickButtonHandler(button, action)
        self.handlers.append(handler)

    def add_touch_sensor_handler(self, port, action):
        handler = TouchSensorHandler(port, action)
        self.handlers.append(handler)
    
    def clear_handlers(self):
        self.handlers = []

    def Update(self, delta_tme):
        for handler in self.handlers:
            handler.Update(delta_tme)
