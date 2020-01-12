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

class GameState:
    motor1Speed = 0
    touchSensors = TouchSensorManager()
    dutyLimit = 35# 50
    
    motor1 = Motor(Port.A)
    motor2 = Motor(Port.B)
    x = 10.5
    y = 10.0

    def Start(self):
        # set up callbacks
        self.touchSensors.SetCallback(Port.S1, self.Button1Callback)
        self.touchSensors.SetCallback(Port.S2, self.Button2Callback)
        self.touchSensors.SetCallback(Port.S3, self.Button3Callback)
        self.touchSensors.SetCallback(Port.S4, self.Button4Callback)


        # Run until motors stall
        self.motor1.set_dc_settings(self.dutyLimit, 0)
        self.motor2.set_dc_settings(self.dutyLimit, 0)


        """
        self.motor2.run_angle(70, -60, Stop.COAST, True)
        self.motor1.run_angle(70, -60, Stop.COAST, False)
        self.motor2.run_angle(70, -60, Stop.COAST, True)
        self.motor1.run_angle(70, -60, Stop.COAST, False)
        
        self.motor2.run_angle(70, -60, Stop.COAST, True)
        self.motor1.run_angle(70, -60, Stop.COAST, False)
        """
        self.run_until_stalled(self.motor1)
        print("Motor 1 stalled")

        wait(300)

        self.run_until_stalled(self.motor2)
        print("Motor 2 stalled")

        wait(300)

        # Back off a bit
        """
        reverse_offset = -5
        print("Backing off " + str(reverse_offset) + " degrees")
        self.motor1.run_angle(50, reverse_offset, Stop.COAST, False)
        self.motor2.run_angle(50, reverse_offset, Stop.COAST, True)
        """

        wait(300)

        print("before reset motor1 angle " + str(self.motor1.angle()) + " motor2 angle " + str(self.motor2.angle()))
        self.motor1.reset_angle(0)
        self.motor2.reset_angle(0)
        print("after reset motor1 angle " + str(self.motor1.angle()) + " motor2 angle " + str(self.motor2.angle()))

        self.motor1.set_dc_settings(100, 0)
        self.motor2.set_dc_settings(100, 0)


        watch = StopWatch()

        """
        while True:
            angle = 360 * math.sin(3.0 * watch.time() / 1000)
            self.motor1.track_target(angle)
            self.motor2.track_target(angle)
        """

        """
        print("run motor 2 to 90 degrees")
        self.motor2.run_target(70, 90, Stop.COAST, True)
        print("run motor 1 to 90 degrees")
        self.motor1.run_target(70, 90, Stop.COAST, True)
        print("finished motor1 angle " + str(self.motor1.angle()) + " motor2 angle " + str(self.motor2.angle()))
        """

        """
        # This should tilt both arms upwards but looks like error is up to 15 degrees
        self.motor2.run_target(100, -90, Stop.COAST, True)
        self.motor1.run_target(100, -90, Stop.COAST, True)
        print("after move motor1 angle " + str(self.motor1.angle()) + " motor2 angle " + str(self.motor2.angle()))
        """

        wait(300)
        print("starting ")

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
            motor1_angle = GEAR_SIGN * GEAR_RATIO * (MOTOR1_CALIBRATION_ANGLE_DEGREES - motor1_ref_angle)
            motor2_angle = GEAR_SIGN * GEAR_RATIO * (MOTOR2_CALIBRATION_ANGLE_DEGREES - motor2_ref_angle)

            self.motor1.track_target(motor1_angle)
            self.motor2.track_target(motor2_angle)

            printTime += deltaTime
            if printTime > 0.5:
                printTime -= 0.5
                print("time " + str(time) + " deltaTime " + str(deltaTime)
                + " x " + str(self.x) + " y " + str(self.y)
                + " m1 ref " + str(motor1_ref_angle) + " m2 ref " + str(motor2_ref_angle)
                + " m1 target " + str(motor1_angle) + " actual " + str(self.motor1.angle())
                + " m2 target " + str(motor2_angle) + " actual " + str(self.motor2.angle()))

            #wait(10)

    def run_until_stalled(self, motor):
        motor.run(-GEAR_SIGN * 150)
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

        motor.run_angle(GEAR_SIGN * 50, CALIBRATION_REVERSE_OFFSET, Stop.COAST, False)



    def Button1Callback(self):
        """ Test function comment """
        self.x = 0
        self.y = 0
        #self.motor1.run(50)
        #self.motor1Speed = 50;
        #self.dutyLimit = max(0, self.dutyLimit - 10)
        #print("Decrement duty limit: " + str(self.dutyLimit))

    def Button2Callback(self):
        self.x = 0
        self.y = SCREEN_HEIGHT
        #self.motor1.run(-50)
        #self.motor1Speed = -50;
        #self.dutyLimit = min(100, self.dutyLimit + 10)
        #print("Inrement duty limit: " + str(self.dutyLimit))

    def Button3Callback(self):
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT
        #self.motor1.set_dc_settings(self.dutyLimit, 0)
        #self.motor1.run_until_stalled(self.motor1Speed, Stop.COAST)
        #print("Run until stalled")

    def Button4Callback(self):
        self.x = SCREEN_WIDTH
        self.y = 0
        #self.motor1.stop()
        #print("Stop")

def number_to_string(number):
    return "{:.2f}".format(number)

class GameState2:
    dutyLimit = 30# 50
    deltaTime = 0
    speed_step = 0.2
    touchSensors = TouchSensorManager()
    
    motor1 = Motor(Port.A)
    motor2 = Motor(Port.B)

    def Start(self):
        # set up callbacks
        self.touchSensors.SetCallback(Port.S1, self.Button1Callback)
        self.touchSensors.SetCallback(Port.S2, self.Button2Callback)
        self.touchSensors.SetCallback(Port.S3, self.Button3Callback)
        self.touchSensors.SetCallback(Port.S4, self.Button4Callback)


        self.motor1.set_dc_settings(self.dutyLimit, 0)
        self.motor2.set_dc_settings(self.dutyLimit, 0)

        self.motor1.reset_angle(0)
        self.motor2.reset_angle(0)

        self.motor1.set_dc_settings(100, 0)
        self.motor2.set_dc_settings(100, 0)


        watch = StopWatch()

        frequency = 2.0
        period = 1 / frequency

        previousTime = watch.time() / 1000
        printTime = 0
        previous_motor1_actual = self.motor1.angle()
        while True:
            self.touchSensors.Update()
            time = watch.time() / 1000
            self.deltaTime = time - previousTime
            previousTime = time
            printTime += self.deltaTime
            motor1_actual = self.motor1.angle()

            if motor1_actual != previous_motor1_actual:
                printTime -= period
                print("t " + number_to_string(time) #+ " dt " + number_to_string(self.deltaTime)
                + " motor1 t " + number_to_string(self.motor1_target) + " a " + number_to_string(motor1_actual) + " s " + str(self.motor1.stalled())
                + " motor2 t " + number_to_string(self.motor2_target) + " a " + number_to_string(self.motor2.angle()) + " s " + str(self.motor2.stalled()))

            previous_motor1_actual = motor1_actual
            self.motor1.track_target(self.motor1_target)
            self.motor2.track_target(self.motor2_target)

        """

            motor1_angle, motor2_angle = positionSource.get_ball_motor_angles(deltaTime)
            self.motor1.track_target(-motor1_angle)
            self.motor2.track_target(-motor2_angle)


        """
            #wait(10)

    motor1_target = 0
    motor2_target = 0

    

    def Button1Callback(self):
        self.motor1_target += self.speed_step

    def Button2Callback(self):
        self.motor1_target -= self.speed_step

    def Button3Callback(self):
        self.motor2_target += self.speed_step

    def Button4Callback(self):
        self.motor2_target -= self.speed_step



game = GameState()
game.Start()

"""
class BallMotor:
    relativeSpeed = 0
    speedScale = 10
    def __init__(self, port):
        self.motor = Motor(port)
    
    # speed in [-1,1]
    def runMotor1(self, speed):
        if motor1.stalled():
            return
        
        print("runMotor1 " + str(speed))
        motor1.run(self.speedScale * speed)


motorSpeed = 10

# speed in [-1,1]
def runMotor1(speed):
    if motor1.stalled():
        return
    
    print("runMotor1 " + str(speed))
    motor1.run(speed * motorSpeed)


print("starting")
previousTime = 0
previousRoundedTime = 0
previousAngle = 0

speed = 0


watch = StopWatch()

while True:
    time = watch.time() / 1000
    roundedTime = round(time)
    deltaTime = time - previousTime
    previousTime = time

    angle = motor1.angle()
    angularSpeed = 0 if deltaTime == 0 else (angle - previousAngle) / deltaTime
    previousAngle = angle

    if previousRoundedTime < roundedTime:
        previousRoundedTime = roundedTime
        print("motor1 angle " + str(motor1.angle()) + " angular speed " + str(angularSpeed) + " angular speed param " + str(speed) + " motor speed " + str(motor1.speed()) + " time " + str(time))

    if motor1Up.pressed():
        speed += 90 * deltaTime
        #runMotor1(0.5)
        motor1.run(speed)
    elif motor1Down.pressed():
        speed = 0
        motor1.stop()
        #runMotor1(-0.5)

    if Button.LEFT in brick.buttons():
        print("LEFT pressed - exiting")
        break

    #motor1.run_until_stalled(60, Stop.COAST)
    if motor1.stalled():
        print("Motor1 Stalled")


    wait(10)
"""
print("smoke weed every day")
