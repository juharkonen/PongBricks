
from pybricks.ev3devices import Motor
from pybricks.parameters import Button
from pybricks import ev3brick as brick
from States.GameState import GameState
from Model.ScreenCalculator import clamp, clamp_paddle_y, ScreenCalculator
from Model.ScreenGeometry import *
from pybricks.tools import print, wait

class DebugState(GameState):

    def on_enter(self):
        brick.display.clear()
        brick.display.text("DEBUG", (50, 50))

        self.input_manager.add_brick_button_handler(Button.CENTER, self.on_stop)

        self.input_manager.add_brick_button_handler(Button.LEFT, self.decrement_x, False)
        self.input_manager.add_brick_button_handler(Button.RIGHT, self.increment_x, False)
        self.input_manager.add_brick_button_handler(Button.UP, self.increment_y, False)
        self.input_manager.add_brick_button_handler(Button.DOWN, self.decrement_y, False)

        self.ball_left_target_x = SCREEN_CENTER_X
        self.ball_left_target_y = SCREEN_MOVABLE_TOP
        self.is_running = True

    def on_update(self, time, delta_time):
        self.set_ball_target(self.ball_left_target_x, self.ball_left_target_y)
        return self.is_running


    def on_stop(self, delta_time):
        self.is_running = False

    def increment_x(self, delta_time):
        delta = MOVE_SPEED * delta_time
        self.ball_left_target_x = clamp(self.ball_left_target_x + delta, SCREEN_MOVABLE_LEFT, SCREEN_MOVABLE_RIGHT)
        print("x " + str(self.ball_left_target_x) + " y " + str(self.ball_left_target_y))

    def decrement_x(self, delta_time):
        delta = -MOVE_SPEED * delta_time
        self.ball_left_target_x = clamp(self.ball_left_target_x + delta, SCREEN_MOVABLE_LEFT, SCREEN_MOVABLE_RIGHT)
        print("x " + str(self.ball_left_target_x) + " y " + str(self.ball_left_target_y))

    def increment_y(self, delta_time):
        delta = MOVE_SPEED * delta_time
        self.ball_left_target_y = clamp(self.ball_left_target_y + delta, SCREEN_MOVABLE_BOTTOM, SCREEN_MOVABLE_TOP)
        print("x " + str(self.ball_left_target_x) + " y " + str(self.ball_left_target_y))

    def decrement_y(self, delta_time):
        delta = -MOVE_SPEED * delta_time
        self.ball_left_target_y = clamp(self.ball_left_target_y + delta, SCREEN_MOVABLE_BOTTOM, SCREEN_MOVABLE_TOP)
        print("x " + str(self.ball_left_target_x) + " y " + str(self.ball_left_target_y))

