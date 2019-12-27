#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

motor1 = Motor(Port.C)
motor2 = Motor(Port.A)

motor1Up = TouchSensor(Port.S1)
motor1Down = TouchSensor(Port.S2)
motor2tUp = TouchSensor(Port.S3)
motor2Down = TouchSensor(Port.S4)

class GameState
    motor1Speed = 0

class BallMotor
    relativeSpeed = 0
    speedScale = 10
    def __init__(self, port):
        self.motor = Motor(port)
    
    # speed in [-1,1]
    def runMotor1(self, speed):
        if motor1.stalled():
            return
        
        print("runMotor1 " + str(speed))
        motor1.run(speedScale * speed)


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

motor1.run_until_stalled(60, Stop.COAST)
    if motor1.stalled():
        print("Motor1 Stalled")


    wait(10)

print("smoke weed every day")
