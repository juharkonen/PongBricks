#!/usr/bin/env pybricks-micropython
from pybricks.parameters import (Port, Stop, Direction, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait
from Model.ScreenCalculator import ScreenCalculator, clamp
from Model.ScreenGeometry import PADDLE_GEAR_RATIO
from MotorTracker import MotorTracker, PaddleMotorTracker
from InputManager import InputManager
from States.StateRunner import StateRunner
from States.StallPaddleState import StallPaddleState
from States.AndState import AndState
from States.BallCalibrationState import BallCalibrationState
from States.GameModeMenuState import GameModeMenuState
from States.PvPGameState import PvPGameState
from States.ExitState import ExitState
from States.NestedState import NestedState

BALL_MOTOR_CALIBRATION_SPEED = 45.0

class MainState(NestedState):
    input_manager = InputManager()
    next_state = None

    def on_update(self, time, delta_time):
        self.input_manager.Update(delta_time)
        return super().on_update(time, delta_time)

    def setup_motors(self):
        # Offset paddle motor angles to y = 0 (bottom)
        paddle_left_offset = ScreenCalculator.calculate_left_paddle_angle(0)
        paddle_right_offset = ScreenCalculator.calculate_right_paddle_angle(0)
        self.paddle_left_motor = PaddleMotorTracker(Port.C, PADDLE_GEAR_RATIO, paddle_left_offset, 1)
        self.paddle_right_motor = PaddleMotorTracker(Port.D, PADDLE_GEAR_RATIO, paddle_right_offset, -1)

    def setup_game_state(self, game_state):
        game_state.set_motors(self.paddle_left_motor, self.paddle_right_motor, self.ball_left_motor, self.ball_right_motor)

    def on_enter(self):
        self.setup_motors()

        # Setup stall paddles
        stall_left_state = StallPaddleState(self.paddle_left_motor.motor, 1)
        stall_right_state = StallPaddleState(self.paddle_right_motor.motor, -1)
        stall_state = AndState([stall_left_state, stall_right_state])

        # Setup ball calibration
        self.ball_left_motor = MotorTracker(Port.A, BALL_MOTOR_CALIBRATION_SPEED, 0)
        self.ball_right_motor = MotorTracker(Port.B, BALL_MOTOR_CALIBRATION_SPEED, 0)
        ball_calibration_state = BallCalibrationState(self.input_manager, self.ball_left_motor, self.ball_right_motor)

        # Setup game modes
        pvp_state = PvPGameState(self.input_manager)
        self.setup_game_state(pvp_state)
        # TODO
        autoplay_state = pvp_state
        single_player_state = pvp_state

        # Setup game mode selection
        exit_state = ExitState()
        self.setup_game_state(exit_state)
        menu_state = GameModeMenuState(self.input_manager, autoplay_state, single_player_state, pvp_state, exit_state)

        # Setup state execution
        self.append_state(stall_state)
        self.append_state(ball_calibration_state)
        self.append_state(menu_state)

        super().on_enter()


runner = StateRunner()
game = MainState()
runner.run_state(game)
