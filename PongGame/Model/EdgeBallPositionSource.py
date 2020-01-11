#from enum import Enum
from Model.ScreenCalculator import ScreenCalculator
"""
class MoveState(Enum):
    STARTING = ()
    LEFT = ()
    TOP = ()
    RIGHT = ()
    BOTTOM = ()
"""
TIME_PER_EDGE = 5
TIME_PERIOD = 4 * TIME_PER_EDGE # seconds
HALF_TIME_PERIOD = TIME_PERIOD / 2.0
SCREEN_WIDTH = 22.0
SCREEN_HEIGHT = 12.0
SPEED = 2.0 * (SCREEN_HEIGHT + SCREEN_WIDTH) / TIME_PERIOD # units/second
HEIGHT_DURATION = SCREEN_HEIGHT / SPEED
WIDTH_DURATION = SCREEN_WIDTH / SPEED
START_DURATION = 2.0

class EdgeBallPositionSource:
    time = 0
    #state = MoveState.STARTING

    # x and y in screen coordinates
    source_x = 0
    source_y = 0
    target_x = 0
    target_y = 0

    def reset_time(self):
        self.time = 0

    def set_start_position(self, start_x, start_y):
        # Todo: calculate inverse position from angles?
        self.source_x = start_x
        self.source_y = start_y

    def get_screen_position(self, deltaTime):
        self.time += deltaTime

        wrapped_time = (self.time - START_DURATION) % TIME_PERIOD
        progress = 0
        if self.time <= START_DURATION:
            # Move to bottom left
            self.target_x = 0
            self.target_y = 0
            progress = self.time / START_DURATION
        elif wrapped_time < TIME_PER_EDGE:
            # bottom left to top left
            self.set_source_and_target(0,0, 0, SCREEN_HEIGHT)
            progress = wrapped_time / TIME_PER_EDGE
        elif wrapped_time < 2*TIME_PER_EDGE:
            # top left to top right
            self.set_source_and_target(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
            progress = wrapped_time / TIME_PER_EDGE - 1
        elif wrapped_time < 3*TIME_PER_EDGE:
            # top right to bottom right
            self.set_source_and_target(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0)
            progress = wrapped_time / TIME_PER_EDGE - 2
        else: #if wrapped_time < 4*TIME_PER_EDGE:
            # bottom right to bottom left
            self.set_source_and_target(SCREEN_WIDTH, 0, 0, 0)
            progress = wrapped_time / TIME_PER_EDGE - 3

        # interpolate
        x = self.source_x + progress * (self.target_x - self.source_x)
        y = self.source_y + progress * (self.target_y - self.source_y)
        return x, y

    def set_source_and_target(self, source_x, source_y, target_x, target_y):
        self.source_x = source_x
        self.source_y = source_y
        self.target_x = target_x
        self.target_y = target_y

    def get_ball_motor_angles(self, deltaTime):
        x, y = self.get_screen_position(deltaTime)
        print("screen position x,y " + str(x) + ", " + str(y))
        return ScreenCalculator.get_motor_angles(x, y)
        
 
