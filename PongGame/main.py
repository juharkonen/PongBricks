#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.parameters import Port, Stop, Direction, Color, Button
from Model.ScreenCalculator import ScreenCalculator, clamp
from Model.ScreenGeometry import *
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
from States.GameState import str

PADDLE_CHANGE_DIRECTION_OFFSET = 4

class MainState(NestedState):
    def try_create_motor(self, port, port_text, gears, angle_offset = 0, direction = Direction.CLOCKWISE, change_direction_offset = 0):
        try:
            return MotorTracker(port, gears, angle_offset, direction, change_direction_offset)
        except OSError:
            brick.display.clear()
            brick.display.text("ERROR:", (10, 30))
            brick.display.text("Motor not found")
            brick.display.text("in Port " + port_text)
            brick.display.text("")
            brick.display.text("CENTER")
            brick.display.text("Exit")

            self.is_error = True
            self.is_running = True
            self.input_manager.add_brick_button_handler(Button.CENTER, self.on_stop)
            return None

    def setup_ball_motor(self, motor):
        #kp, ki, kd, integral_range, integral_rate, feed_forward = motor.control.pid()
        #print("kp " + str(kp) + ", ki " + str(ki) + ", kd " + str(kd) + ", integral_range " + str(integral_range) + ", integral_rate " + str(integral_rate) + ", feed_forward " + str(feed_forward))

        # Tune PID parameters for smoother ball tracking movement
        # defaults kp 400.00, ki 1200.00, kd 5.00, integral_range 23.00, integral_rate 5.00, feed_forward 0.00
        motor.control.pid(200, 1200, 0, 23, 5, 0)

    def setup_motors(self):
        self.ball_left_motor = self.try_create_motor(Port.B, "B", BALL_GEARS)
        if self.is_error:
            return

        self.ball_right_motor = self.try_create_motor(Port.C, "C", BALL_GEARS)
        if self.is_error:
            return

        self.setup_ball_motor(self.ball_left_motor.motor)
        self.setup_ball_motor(self.ball_right_motor.motor)

        # Paddles are at bottom after calibration
        # Increasing angle moves paddles up
        # Offset paddle motor angles to account for paddle pivot half a stud offset at y = PADDLE_PIVOT_OFFSET
        paddle_angle_offset = ScreenCalculator.calculate_paddle_angle(PADDLE_PIVOT_OFFSET)

        self.paddle_left_motor = self.try_create_motor(Port.A, "A", PADDLE_GEARS, paddle_angle_offset, Direction.COUNTERCLOCKWISE, PADDLE_CHANGE_DIRECTION_OFFSET)
        if self.is_error:
            return

        self.paddle_right_motor = self.try_create_motor(Port.D, "D", PADDLE_GEARS, paddle_angle_offset, Direction.COUNTERCLOCKWISE, PADDLE_CHANGE_DIRECTION_OFFSET)
        if self.is_error:
            return

    def on_update(self, time, delta_time):
        if self.is_error:
            return self.is_running
        return super().on_update(time, delta_time)
    
    def on_stop(self, time):
        self.is_running = False

    def setup_game_state(self, game_state):
        game_state.set_motors(self.paddle_left_motor, self.paddle_right_motor, self.ball_left_motor, self.ball_right_motor)

    def on_enter(self):
        self.is_error = False

        self.setup_motors()
        if self.is_error:
            return

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
