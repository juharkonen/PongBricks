#!/usr/bin/env pybricks-micropython
from pybricks.parameters import (Port, Stop, Direction, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait
from Model.ScreenCalculator import ScreenCalculator, clamp
from Model.ScreenGeometry import PADDLE_GEAR_RATIO, PADDLE_EDGE_THICKNESS
from MotorTracker import MotorTracker
from States.StateRunner import StateRunner
from States.StallPaddleState import StallPaddleState
from States.AndState import AndState
from States.BallCalibrationState import BallCalibrationState
from States.GameModeMenuState import GameModeMenuState
from States.ExitState import ExitState
from States.NestedState import NestedState
from States.PvPGameState import PvPGameState
from States.CountdownState import CountdownState
from States.AutoplayResultState import AutoplayResultState
from States.GameResultState import GameResultState
from States.AutoplayGameState import AutoplayGameState
from States.SinglePlayerGameState import SinglePlayerGameState
from States.DebugState import DebugState

class MainState(NestedState):
    BALL_MOTOR_CALIBRATION_SPEED = 45.0
    
    def setup_motors(self):
        self.ball_left_motor = MotorTracker(Port.B, self.BALL_MOTOR_CALIBRATION_SPEED, 0)
        self.ball_right_motor = MotorTracker(Port.C, self.BALL_MOTOR_CALIBRATION_SPEED, 0)

        # Offset paddle motor angles to account for paddle pivot half a stud offset at y = PADDLE_EDGE_THICKNESS
        paddle_angle_offset = ScreenCalculator.calculate_paddle_angle(PADDLE_EDGE_THICKNESS)
        self.paddle_left_motor = MotorTracker(Port.A, PADDLE_GEAR_RATIO, paddle_angle_offset)
        self.paddle_right_motor = MotorTracker(Port.D, PADDLE_GEAR_RATIO, paddle_angle_offset)

    def setup_game_state(self, game_state):
        game_state.set_motors(self.paddle_left_motor, self.paddle_right_motor, self.ball_left_motor, self.ball_right_motor)

    def on_enter(self):
        self.setup_motors()

        # Setup stall paddles
        stall_left_state = StallPaddleState(self.paddle_left_motor.motor)
        stall_right_state = StallPaddleState(self.paddle_right_motor.motor)
        stall_state = AndState([stall_left_state, stall_right_state])

        # Setup ball calibration
        ball_calibration_state = BallCalibrationState(self.ball_left_motor, self.ball_right_motor)

        # Setup pvp game mode
        pvp_result_state = GameResultState()
        pvp_game_state = PvPGameState(pvp_result_state)
        self.setup_game_state(pvp_game_state)
        pvp_state = NestedState()
        pvp_state.append_states(CountdownState(), pvp_game_state, pvp_result_state)

        # Setup autoplay game mode
        autoplay_countdown_state = CountdownState()
        autoplay_result_state = AutoplayResultState()
        self.setup_game_state(autoplay_result_state)
        autoplay_game_state = AutoplayGameState(autoplay_result_state)
        self.setup_game_state(autoplay_game_state)
        autoplay_state = NestedState()
        autoplay_state.append_states(autoplay_countdown_state, autoplay_game_state, autoplay_result_state)
        autoplay_result_state.next_state = autoplay_countdown_state

        # Setup single player game mode
        single_player_result_state = GameResultState()
        single_player_game_state = SinglePlayerGameState(single_player_result_state)
        self.setup_game_state(single_player_game_state)
        single_player_state = NestedState()
        single_player_state.append_states(CountdownState(), single_player_game_state, single_player_result_state)

        # Debug
        debug_state = DebugState()
        self.setup_game_state(debug_state)

        # Setup game mode selection
        exit_state = ExitState()
        self.setup_game_state(exit_state)
        menu_state = GameModeMenuState(autoplay_state, single_player_state, pvp_state, exit_state)
        self.setup_game_state(menu_state)

        # Setup state execution
        self.append_states(stall_state, ball_calibration_state, menu_state)
        #self.append_states(stall_state, ball_calibration_state, debug_state, exit_state)

        super().on_enter()


StateRunner().run_state(MainState())
