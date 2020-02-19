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
from States.PvpGameNestedState import PvpGameNestedState
from States.ExitState import ExitState
from States.NestedState import NestedState
from States.PvPGameState import PvPGameState
from States.CountdownState import CountdownState
from States.GameResultState import GameResultState

BALL_MOTOR_CALIBRATION_SPEED = 45.0

class MainState(NestedState):
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
        ball_calibration_state = BallCalibrationState(self.ball_left_motor, self.ball_right_motor)

        # Setup pvp game mode
        countdown_state = CountdownState()
        result_state = GameResultState()

        pvp_game_state = PvPGameState(result_state)
        self.setup_game_state(pvp_game_state)
        
        pvp_state = NestedState()
        pvp_state.append_states(countdown_state, pvp_game_state, result_state)

        # TODO implement autoplay and single player
        autoplay_state = pvp_state
        single_player_state = pvp_state

        # Setup game mode selection
        exit_state = ExitState()
        self.setup_game_state(exit_state)
        menu_state = GameModeMenuState(autoplay_state, single_player_state, pvp_state, exit_state)
        self.setup_game_state(menu_state)

        # Setup state execution
        self.append_states(stall_state, ball_calibration_state, menu_state)

        super().on_enter()


StateRunner().run_state(MainState())
