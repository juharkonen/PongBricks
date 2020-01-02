#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

#motor1 = Motor(Port.C)
#motor2 = Motor(Port.A)

#motor1Up = TouchSensor(Port.S1)
#motor1Down = TouchSensor(Port.S2)
#motor2tUp = TouchSensor(Port.S3)
#motor2Down = TouchSensor(Port.S4)

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
    motor2 = Motor(Port.C)

    def Start(self):
        # set up callbacks
        self.touchSensors.SetCallback(Port.S1, self.Button1Callback)
        self.touchSensors.SetCallback(Port.S2, self.Button2Callback)
        self.touchSensors.SetCallback(Port.S3, self.Button3Callback)
        self.touchSensors.SetCallback(Port.S4, self.Button4Callback)

        print("motor1 angle " + str(self.motor1.angle()) + " motor2 angle " + str(self.motor2.angle()))

        self.motor1.set_dc_settings(self.dutyLimit, 0)

        self.motor1.run_angle(-70, 60, Stop.COAST, False)
        self.motor2.run_angle(-70, 60, Stop.COAST, True)

        print("run motor 1 at 50")
        self.motor1.run_angle(70, 180, Stop.COAST, False)
        print("run motor 2 at 50")
        self.motor2.run_angle(70, 180, Stop.COAST, False)
        #self.motor2.run(70)
        print("calibration done")

        while True:
            self.touchSensors.Update()
            wait(10)

    def Button1Callback(self):
        """ Test function comment """
        self.motor1.run(50)
        self.motor1Speed = 50;
        #self.dutyLimit = max(0, self.dutyLimit - 10)
        #print("Decrement duty limit: " + str(self.dutyLimit))

    def Button2Callback(self):
        self.motor1.run(-50)
        self.motor1Speed = -50;
        #self.dutyLimit = min(100, self.dutyLimit + 10)
        #print("Inrement duty limit: " + str(self.dutyLimit))

    def Button3Callback(self):
        self.motor1.set_dc_settings(self.dutyLimit, 0)
        self.motor1.run_until_stalled(self.motor1Speed, Stop.COAST)
        print("Run until stalled")

    def Button4Callback(self):
        self.motor1.stop()
        print("Stop")

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
