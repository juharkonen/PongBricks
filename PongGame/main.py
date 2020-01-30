#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from Model.ScreenCalculator import ScreenCalculator
from Model.EdgeBallPositionSource import EdgeBallPositionSource
import math
from Model.ScreenCalculator import ScreenCalculator, clamp
from Model.ScreenGeometry import *
from MotorTracker import MotorTracker, PaddleMotorTracker
from InputManager import InputManager
from Model.PongBallCalculator import PongBallCalculator

BALL_MOTOR_CALIBRATION_SPEED = 45.0
BALL_DEBUG_MOVE_SPEED = 4.0

def str(number):
    return "{:.2f}".format(number)

game_over_sounds = [
    SoundFile.GAME_OVER,
    SoundFile.CRYING,
    SoundFile.OUCH,
    SoundFile.KUNG_FU,
    SoundFile.FANFARE]

ball_hit_sound = SoundFile.SONAR

class GameState:
    input_manager = InputManager()
    watch = StopWatch()
    
    is_calibrating = True
    exit_game = False

    def play_sound(self, sound):
        print("playing " + sound)
        brick.sound.file(sound)
        wait(300)

    def Start(self):
        
        #self.play_sound(game_over_sounds[0])
        #self.play_sound(ball_hit_sound)
        # Audio must be mono. 8bit unsigned and 16bit signed confirmed to play
        ##brick.sound.file('Audio/dundundunnn_16bit.wav')

        # Offset paddle motor angles to y = 0 (bottom)
        paddle_left_offset = ScreenCalculator.calculate_left_paddle_angle(0)
        paddle_right_offset = ScreenCalculator.calculate_right_paddle_angle(0)
        self.paddle_left_motor = PaddleMotorTracker(Port.C, PADDLE_GEAR_RATIO, paddle_left_offset, 1)
        self.paddle_right_motor = PaddleMotorTracker(Port.D, PADDLE_GEAR_RATIO, paddle_right_offset, -1)
        
        print("Calibrate left paddle")
        self.paddle_left_motor.run_until_stalled()
        #self.run_until_stalled(self.motor_paddle_left, 1)
        print("left paddle stalled")

        print("Calibrate right paddle")
        self.paddle_right_motor.run_until_stalled()
        #self.run_until_stalled(self.motor_paddle_right, -1)
        print("right paddle stalled")
        self.paddle_left_target_y = 0.0
        self.paddle_right_target_y = 0.0

        # Create ball motors
        self.ball_left_motor = MotorTracker(Port.A, BALL_MOTOR_CALIBRATION_SPEED, 0)
        self.ball_right_motor = MotorTracker(Port.B, BALL_MOTOR_CALIBRATION_SPEED, 0)
        
        print("Ball calibration: press CENTER complete")
        self.input_manager.add_brick_button_handler(Button.LEFT, self.left_ball_motor_up)
        self.input_manager.add_brick_button_handler(Button.RIGHT, self.left_ball_motor_down)
        self.input_manager.add_brick_button_handler(Button.UP, self.right_ball_motor_up)
        self.input_manager.add_brick_button_handler(Button.DOWN, self.right_ball_motor_down)

        # Run motor controls until player stops calibration with CENTER button
        self.input_manager.add_brick_button_handler(Button.CENTER, self.stop_ball_calibration)
        self.is_calibrating = True
        self.iterate(lambda:self.is_calibrating, None)

        self.ball_left_motor.reset_angle()
        self.ball_right_motor.reset_angle()

        self.input_manager.clear_handlers()
        print("Finished ball calibration")

        wait(500)

        # Start game
        print("starting game")

        ball_motor_scale = BALL_GEAR_SIGN * BALL_GEAR_RATIO
        ball_start_x = SCREEN_WIDTH / 2.0
        ball_start_y = SCREEN_HEIGHT
        ball_left_motor_start_angle, ball_right_motor_start_angle = ScreenCalculator.get_motor_angles(ball_start_x, ball_start_y)
        print("ball start angle left " + str(ball_left_motor_start_angle) + " right " + str(ball_right_motor_start_angle))
        self.ball_left_motor.set_transform(ball_motor_scale, ball_left_motor_start_angle)
        self.ball_right_motor.set_transform(ball_motor_scale, ball_right_motor_start_angle)

        self.positionSource = EdgeBallPositionSource()
        self.positionSource.set_start_position(ball_start_x, ball_start_y)

        # Button callbacks
        self.input_manager.add_touch_sensor_handler(Port.S1, self.left_paddle_down)
        self.input_manager.add_touch_sensor_handler(Port.S2, self.left_paddle_up)
        self.input_manager.add_touch_sensor_handler(Port.S3, self.right_paddle_down)
        self.input_manager.add_touch_sensor_handler(Port.S4, self.right_paddle_up)

        # Iterate until player exits with CENTER button
        self.input_manager.add_brick_button_handler(Button.CENTER, self.quit)

        self.input_manager.add_brick_button_handler(Button.LEFT, self.ball_x_left)
        self.input_manager.add_brick_button_handler(Button.RIGHT, self.ball_x_right)
        self.input_manager.add_brick_button_handler(Button.UP, self.ball_y_up)
        self.input_manager.add_brick_button_handler(Button.DOWN, self.ball_y_down)

        #self.x = SCREEN_WIDTH / 2.0
        #self.y = SCREEN_HEIGHT
        self.print_time = 0

        
        self.pong = PongBallCalculator()
        rand = (self.watch.time() % 0.45) / 0.45
        self.pong.reset_random(rand)

        self.iterate(lambda: not self.exit_game, self.update_game)

        # return to start position
        print("returning ball to calibration position")


        self.x = SCREEN_WIDTH / 2.0
        self.y = SCREEN_HEIGHT
        self.update_ball_position()

        wait(500)

    def update_game(self, delta_time):
        # Update target angles for ball x and y
        self.pong.update_state(delta_time)
        self.x = self.pong.x
        self.y = self.pong.y
        #self.x, self.y = self.positionSource.get_screen_position(delta_time)
        
        self.update_ball_position()

        # Update paddle angles for paddle y
        paddle_left_angle = ScreenCalculator.calculate_left_paddle_angle(self.paddle_left_target_y)
        self.paddle_left_motor.track_target(paddle_left_angle)

        paddle_right_angle = ScreenCalculator.calculate_right_paddle_angle(self.paddle_right_target_y)
        self.paddle_right_motor.track_target(paddle_right_angle)

        self.print_time += delta_time
        """
        if self.print_time > 1.0:
            self.print_time -= 1
            print("time " + str(self.time)
             + " delta_time " + str(delta_time)
             + " x " + str(self.x)
             + " y " + str(self.y)
             + " paddle_left_angle " + str(paddle_left_angle)
             + " paddle_right_angle " + str(paddle_right_angle))
        """

    def update_ball_position(self):
        print("x y " + str(self.x) + "   " + str(self.y))
        ball_left_motor_angle, ball_right_motor_angle = ScreenCalculator.get_motor_angles(self.x, self.y)
        self.ball_left_motor.track_target(ball_left_motor_angle)
        self.ball_right_motor.track_target(ball_right_motor_angle)

    def left_ball_motor_up(self, delta_time):
        self.ball_left_motor.track_target_step(delta_time)
        print("ball_left_motor target " + str(self.ball_left_motor.target))

    def left_ball_motor_down(self, delta_time):
        self.ball_left_motor.track_target_step(-delta_time)
        print("ball_left_motor target " + str(self.ball_left_motor.target))

    def right_ball_motor_up(self, delta_time):
        self.ball_right_motor.track_target_step(delta_time)
        print("ball_right_motor target " + str(self.ball_right_motor.target))

    def right_ball_motor_down(self, delta_time):
        self.ball_right_motor.track_target_step(-delta_time)
        print("ball_right_motor target " + str(self.ball_right_motor.target))

    def stop_ball_calibration(self, _):
        self.is_calibrating = False
        print("finish ball calibration")

    def ball_x_right(self, delta_time):
        self.x = clamp(self.x + BALL_DEBUG_MOVE_SPEED * delta_time, 0, SCREEN_WIDTH)
        print("x target " + str(self.x))

    def ball_x_left(self, delta_time):
        self.x = clamp(self.x - BALL_DEBUG_MOVE_SPEED * delta_time, 0, SCREEN_WIDTH)
        print("x target " + str(self.x))

    def ball_y_up(self, delta_time):
        self.y = clamp(self.y + BALL_DEBUG_MOVE_SPEED * delta_time, 0, SCREEN_HEIGHT)
        print("y target " + str(self.y))

    def ball_y_down(self, delta_time):
        self.y = clamp(self.y - BALL_DEBUG_MOVE_SPEED * delta_time, 0, SCREEN_HEIGHT)
        print("y target " + str(self.y))

    def quit(self, _):
        print("quit")
        self.exit_game = True

    def iterate(self, condition, action):
        previous_time = self.watch.time() / 1000
        delta_time = 0.0
        self.time = 0
        while condition():
            self.input_manager.Update(delta_time)
            if not (action is None):
                action(delta_time)

            self.time = self.watch.time() / 1000
            delta_time = self.time - previous_time
            previous_time = self.time

            wait(10)

    def left_paddle_up(self, delta_time):
        delta = PADDLE_SPEED * delta_time
        self.paddle_left_target_y = clamp(self.paddle_left_target_y + delta, 0, PADDLE_RANGE_Y)
        print("left target " + str(self.paddle_left_target_y))

    def left_paddle_down(self, delta_time):
        delta = -PADDLE_SPEED * delta_time
        self.paddle_left_target_y = clamp(self.paddle_left_target_y + delta, 0, PADDLE_RANGE_Y)
        print("left target " + str(self.paddle_left_target_y))

    def right_paddle_up(self, delta_time):
        delta = PADDLE_SPEED * delta_time
        self.paddle_right_target_y = clamp(self.paddle_right_target_y + delta, 0, PADDLE_RANGE_Y)
        print("right target " + str(self.paddle_right_target_y))

    def right_paddle_down(self, delta_time):
        delta = -PADDLE_SPEED * delta_time
        self.paddle_right_target_y = clamp(self.paddle_right_target_y + delta, 0, PADDLE_RANGE_Y)
        print("right target " + str(self.paddle_right_target_y))


game = GameState()
game.Start()
