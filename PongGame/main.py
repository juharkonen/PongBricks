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
from Model.ScreenCalculator import ScreenCalculator
from Model.ScreenGeometry import *

class ButtonHandler:
    def __init__(self, action, touchSensor):
        self.action = action
        self.touchSensor = touchSensor
    
    def UpdatePressed(self):
        if self.touchSensor.pressed():
            self.action()


class TouchSensorManager:
    handlers = []

    def SetCallback(self, port, action):
        handler = ButtonHandler(action, TouchSensor(port))
        self.handlers.append(handler)
    
    def Update(self):
        for handler in self.handlers:
            handler.UpdatePressed()



PADDLE_CALIBRATION_DUTY_LIMIT = 35.0
PADDLE_CALIBRATION_REVERSE_OFFSET = 6.0
MOTOR_CALIBRATION_STEP = 2.0

class MotorTracker:

    def __init__(self, port, scale, offset, stall_sign):
        self.motor = Motor(port)
        self.scale = scale
        self.offset = offset

    def track_target(self, source):
        target = self.scale * (source - self.offset)
        self.motor.track_target(target)

def PaddleMotorTracker(MotorTracker):
    def __init__(self, port, scale, offset, stall_sign):
        self.stall_sign = stall_sign
        super().__init__(port, scale, offset)

    def run_until_stalled(self, sign):
        self.motor.set_dc_settings(PADDLE_CALIBRATION_DUTY_LIMIT, 0)

        self.motor.run(sign * 150)
        previous_angle = 123.0
        watch = StopWatch()
        t_prev = watch.time() / 1000.0
        stalled_time = 0.0
        while True:
            t = watch.time() / 1000.0
            dt = t - t_prev
            t_prev = t

            motor_angle = self.motor.angle()
            angle_delta = motor_angle - previous_angle
            previous_angle = motor_angle
            
            print("Angle " + str(motor_angle) + " Angle difference " + str(angle_delta)
                 + " dt " + str(dt) + " stalled_time " + str(stalled_time))
            
            if  abs(angle_delta) < 1:
                stalled_time += dt
            else:
                stalled_time = 0.0
            
            if stalled_time > 0.3:
                break

        self.motor.set_dc_settings(100, 0)
        self.motor.run_angle(-sign * 50, PADDLE_CALIBRATION_REVERSE_OFFSET, Stop.COAST, True)
        wait(200)
        self.motor.reset_angle(0)

    

class GameState:
    motor1Speed = 0
    touchSensors = TouchSensorManager()
    
    is_calibrating = True
    motor1_target = 0
    motor2_target = 0

    motor_paddle_left2 = MotorTracker(Port.C)
    motor_ball1 = Motor(Port.A)
    motor_ball2 = Motor(Port.B)
    motor_paddle_left = Motor(Port.C)
    motor_paddle_right = Motor(Port.D)

    selected_motor = motor_ball1
    x = 10.5
    y = 14.0

    def set_paddle_target(self, motor, y):
        paddle_left_ref_angle = ScreenCalculator.calculate_left_paddle_angle(PADDLE_RANGE_Y / 2.0)
        paddle_left_angle = PADDLE_GEAR_RATIO * (paddle_left_ref_angle - paddle_left_offset)
        motor.track_target(paddle_left_angle)

    def Start(self):
        # Button callbacks
        self.touchSensors.SetCallback(Port.S1, self.Button1Callback)
        self.touchSensors.SetCallback(Port.S2, self.Button2Callback)
        self.touchSensors.SetCallback(Port.S3, self.Button3Callback)
        self.touchSensors.SetCallback(Port.S4, self.Button4Callback)

        
        print("Starting paddle calibration")
        self.run_until_stalled(self.motor_paddle_left, 1)
        print("left paddle stalled")
        
        
        paddle_left_offset = ScreenCalculator.calculate_left_paddle_angle(0)
        paddle_left_ref_angle = ScreenCalculator.calculate_left_paddle_angle(PADDLE_RANGE_Y / 2.0)
        paddle_left_angle = PADDLE_GEAR_RATIO * (paddle_left_ref_angle - paddle_left_offset)
        print("left paddle offset " + str(paddle_left_offset) + " ref angle " + str(paddle_left_ref_angle)
             + " target " + str(paddle_left_angle))
        self.motor_paddle_left.track_target(paddle_left_angle)
        wait(2000)
        return

        wait(300)

        self.run_until_stalled(self.motor_paddle_right, -1)
        print("right paddle stalled")


        print("Starting ball calibration")
        while self.is_calibrating:
            self.touchSensors.Update()
            self.motor_ball1.track_target(self.motor1_target)
            self.motor_ball2.track_target(self.motor2_target)
            wait(10)

        print("Finished ball calibration")

        wait(300)

        self.motor_ball1.reset_angle(0)
        self.motor_ball2.reset_angle(0)



        watch = StopWatch()

        wait(300)
        print("starting ")

        motor1_offset, motor2_offset = ScreenCalculator.get_motor_angles(self.x, self.y)
        #motor1_offset = MOTOR1_CALIBRATION_ANGLE_DEGREES
        #motor2_offset = MOTOR2_CALIBRATION_ANGLE_DEGREES

        positionSource = EdgeBallPositionSource()
        positionSource.set_start_position(3, 10)

        previousTime = watch.time() / 1000
        printTime = 0
        while True:
            self.touchSensors.Update()
            time = watch.time() / 1000
            deltaTime = time - previousTime
            previousTime = time

            #x = 11
            #y = 10
            motor1_ref_angle, motor2_ref_angle = ScreenCalculator.get_motor_angles(self.x, self.y)

            #motor1_ref_angle, motor2_ref_angle = positionSource.get_ball_motor_angles(deltaTime)
            #x, y = positionSource.get_screen_position(0)
            #motor1_angle = GEAR_SIGN * GEAR_RATIO * (MOTOR1_CALIBRATION_ANGLE_DEGREES - motor1_ref_angle)
            #motor2_angle = GEAR_SIGN * GEAR_RATIO * (MOTOR2_CALIBRATION_ANGLE_DEGREES - motor2_ref_angle)
            motor1_angle = BALL_GEAR_SIGN * BALL_GEAR_RATIO * (motor1_offset - motor1_ref_angle)
            motor2_angle = BALL_GEAR_SIGN * BALL_GEAR_RATIO * (motor2_offset - motor2_ref_angle)

            self.motor_ball1.track_target(motor1_angle)
            self.motor_ball2.track_target(motor2_angle)

            printTime += deltaTime
            if printTime > 0.5:
                printTime -= 0.5
                print("time " + str(time) + " deltaTime " + str(deltaTime)
                + " x " + str(self.x) + " y " + str(self.y)
                + " m1 ref " + str(motor1_ref_angle) + " m2 ref " + str(motor2_ref_angle)
                + " m1 target " + str(motor1_angle) + " actual " + str(self.motor_ball1.angle())
                + " m2 target " + str(motor2_angle) + " actual " + str(self.motor_ball2.angle()))

            #wait(10)

    def run_until_stalled(self, motor, sign):
        motor.set_dc_settings(PADDLE_CALIBRATION_DUTY_LIMIT, 0)

        motor.run(sign * 150)
        previous_angle = 123.0
        watch = StopWatch()
        t_prev = watch.time() / 1000.0
        stalled_time = 0.0
        while True:
            t = watch.time() / 1000.0
            dt = t - t_prev
            t_prev = t

            motor_angle = motor.angle()
            angle_delta = motor_angle - previous_angle
            previous_angle = motor_angle
            
            print("Angle " + str(motor_angle) + " Angle difference " + str(angle_delta)
                 + " dt " + str(dt) + " stalled_time " + str(stalled_time))
            
            if  abs(angle_delta) < 1:
                stalled_time += dt
            else:
                stalled_time = 0.0
            
            if stalled_time > 0.3:
                break

        motor.set_dc_settings(100, 0)
        motor.run_angle(-sign * 50, PADDLE_CALIBRATION_REVERSE_OFFSET, Stop.COAST, True)
        wait(200)
        motor.reset_angle(0)




    def Button1Callback(self):
        print("button1")
        if self.is_calibrating:
            self.offset_selected_motor_target(MOTOR_CALIBRATION_STEP)
        else:
            self.x = 0
            self.y = 0

    def Button2Callback(self):
        print("button2")
        if self.is_calibrating:
            self.offset_selected_motor_target(-MOTOR_CALIBRATION_STEP)
        else:
            self.x = 0
            self.y = SCREEN_HEIGHT

    def Button3Callback(self):
        print("button3")
        if self.is_calibrating:
            if self.selected_motor == self.motor_ball1:
                print("motor2 selected")
                self.selected_motor = self.motor_ball2
            else:
                self.selected_motor = self.motor_ball1
                print("motor1 selected")
        else:
            self.x = SCREEN_WIDTH
            self.y = SCREEN_HEIGHT

    def Button4Callback(self):
        print("button4")
        if self.is_calibrating:
            self.is_calibrating = False
        else:
            self.x = SCREEN_WIDTH
            self.y = 0

    def offset_selected_motor_target(self, step):
        if self.selected_motor == self.motor_ball1:
            self.motor1_target += step
            print("motor 1 target " + str(self.motor1_target))
        else:
            self.motor2_target += step
            print("motor 2 target " + str(self.motor2_target))

def number_to_string(number):
    return "{:.2f}".format(number)


game = GameState()
game.Start()


print("smoke weed every day")
